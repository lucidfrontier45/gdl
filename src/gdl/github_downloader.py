"""GitHub Binary Downloader CLI Tool."""

import contextlib
import dataclasses
import platform
import shutil
import stat
import sys
import tarfile
import tempfile
import zipfile
from collections.abc import Sequence
from pathlib import Path
from typing import Annotated, TypedDict

import httpx
import tqdm
import tyro
from tyro.conf import Positional, arg


class Asset(TypedDict):
    name: str
    browser_download_url: str


def get_host_os() -> str:
    """Get the host operating system in normalized form."""
    system = platform.system().lower()
    if system == "darwin":
        return "macos"
    elif system in ("windows", "linux"):
        return system
    else:
        raise ValueError(f"Unsupported OS: {system}")


def get_host_arch() -> str:
    """Get the host architecture in normalized form."""
    machine = platform.machine().lower()
    arch_map = {
        "amd64": "x86_64",
        "x86_64": "x86_64",
        "x64": "x86_64",
        "aarch64": "aarch64",
        "arm64": "aarch64",
    }
    if machine in arch_map:
        return arch_map[machine]
    else:
        raise ValueError(f"Unsupported architecture: {machine}")


def get_release_assets(repo: str, tag: str | None = None) -> list[Asset]:
    """Fetch assets from GitHub release."""
    owner, repo_name = repo.split("/", 1)
    url = f"https://api.github.com/repos/{owner}/{repo_name}/releases"
    url = f"{url}/tags/{tag}" if tag else f"{url}/latest"

    response = httpx.get(url)
    response.raise_for_status()
    release = response.json()
    return release.get("assets", [])


def match_assets(
    assets: Sequence[Asset], os: str, arch: str, blacklist: list[str]
) -> list[Asset]:
    """Filter assets matching OS, arch, and not containing blacklist words."""
    os_synonyms = {
        "windows": ["windows", "win32"],
        "linux": ["linux"],
        "macos": ["macos", "mac", "darwin"],
    }
    arch_synonyms = {
        "x86_64": ["x86_64", "x64", "amd64"],
        "aarch64": ["aarch64", "arm64"],
    }

    os_terms = os_synonyms.get(os, [os])
    arch_terms = arch_synonyms.get(arch, [arch])

    matches = []
    for asset in assets:
        name = asset["name"].lower()
        if not any(term in name for term in os_terms) or not any(
            term in name for term in arch_terms
        ):
            continue
        if any(word.lower() in name for word in blacklist):
            continue
        matches.append(asset)
    return matches


def choose_asset(assets: Sequence[Asset]) -> Asset | None:
    """Prompt user to choose an asset if multiple matches."""
    if not assets:
        return None
    if len(assets) == 1:
        return assets[0]

    print("Multiple assets found:")
    for i, asset in enumerate(assets):
        print(f"{i + 1}: {asset['name']}")

    while True:
        try:
            choice = int(input("Choose an asset (number): ")) - 1
            if 0 <= choice < len(assets):
                return assets[choice]
            else:
                print("Invalid choice.")
        except ValueError:
            print("Please enter a number.")


def download_asset(asset: Asset, dest: Path) -> None:
    """Download the asset to the destination path."""
    url = asset["browser_download_url"]
    with httpx.stream("GET", url, follow_redirects=True) as response:
        response.raise_for_status()
        total_size = int(response.headers.get("content-length", 0))
        with (
            dest.open("wb") as f,
            tqdm.tqdm(
                total=total_size,
                unit="B",
                unit_scale=True,
                desc=asset["name"],
            ) as pbar,
        ):
            for chunk in response.iter_bytes():
                f.write(chunk)
                pbar.update(len(chunk))


def unpack_asset(
    asset_path: Path,
    extract_dir: Path,
    final_name: str,
    host_os: str,
    choose_bin_file: bool = False,
) -> Path | None:
    """Unpack compressed asset and return path to the renamed executable binary."""
    if asset_path.suffix == ".zip":
        with zipfile.ZipFile(asset_path, "r") as zf:
            # Use a safe extraction: iterate members and write files to target
            for member in zf.namelist():
                member_path = extract_dir / member
                # Prevent path traversal
                if not str(member_path.resolve()).startswith(
                    str(extract_dir.resolve())
                ):
                    continue
                if member.endswith("/"):
                    member_path.mkdir(parents=True, exist_ok=True)
                else:
                    member_path.parent.mkdir(parents=True, exist_ok=True)
                    with zf.open(member) as src, member_path.open("wb") as dst:
                        shutil.copyfileobj(src, dst)
    elif asset_path.suffixes == [".tar", ".gz"]:
        with tarfile.open(asset_path, "r:gz") as tf:
            # Safe extraction: only extract regular files and avoid path traversal
            for member in tf.getmembers():
                if not member.isreg():
                    continue
                member_path = extract_dir / member.name
                if not str(member_path.resolve()).startswith(
                    str(extract_dir.resolve())
                ):
                    continue
                member_path.parent.mkdir(parents=True, exist_ok=True)
                src = tf.extractfile(member)
                if src is None:
                    continue
                with src as src_file, member_path.open("wb") as dst:
                    shutil.copyfileobj(src_file, dst)
    else:
        # Not compressed, assume it's the binary
        binary_path = asset_path
        new_name = final_name + (
            ".exe" if host_os == "windows" and not final_name.endswith(".exe") else ""
        )
        new_path = asset_path.with_name(new_name)
        binary_path.rename(new_path)
        return new_path

    # Collect candidate files
    candidates: list[Path] = [p for p in extract_dir.rglob("*") if p.is_file()]
    if not candidates:
        return None

    # If interactive choice requested, present choices in descending size order
    if choose_bin_file:
        # This check will also be enforced in main, but double-check here
        if not sys.stdin.isatty():
            print(
                "Error: --choose-bin-file requires an interactive TTY."
                " Run without this flag to auto-select the binary."
            )
            return None

        # Sort by size desc
        candidates_sorted = sorted(
            candidates, key=lambda p: p.stat().st_size, reverse=True
        )
        print(
            "Multiple candidate files found. Choose which to use as the final binary:"
        )
        for i, p in enumerate(candidates_sorted, start=1):
            print(f"{i}) {p.relative_to(extract_dir)} {p.stat().st_size} bytes")
        while True:
            choice = input(
                f"Choose file [1-{len(candidates_sorted)}] (default 1): "
            ).strip()
            if choice == "":
                chosen = candidates_sorted[0]
                break
            try:
                idx = int(choice)
                if 1 <= idx <= len(candidates_sorted):
                    chosen = candidates_sorted[idx - 1]
                    break
            except ValueError:
                pass
            print("Invalid choice, please enter a number from the list.")

    else:
        # Apply prioritized selection:
        # 1) files with .exe suffix (case-insensitive)
        exe_candidates = [p for p in candidates if p.suffix.lower() == ".exe"]

        def pick_largest_with_tiebreak(files: list[Path]) -> Path:
            # pick by largest size, tie-break by lexical order of relative path
            files_sorted = sorted(
                files,
                key=lambda p: (-p.stat().st_size, str(p.relative_to(extract_dir))),
            )
            return files_sorted[0]

        if exe_candidates:
            chosen = pick_largest_with_tiebreak(exe_candidates)
        else:
            # 2) files with unix exec permission
            exec_candidates = [p for p in candidates if p.stat().st_mode & 0o111]
            if exec_candidates:
                chosen = pick_largest_with_tiebreak(exec_candidates)
            else:
                # 3) fallback to largest file
                chosen = pick_largest_with_tiebreak(candidates)

    # Rename chosen file to final name (add .exe on Windows if needed)
    new_name = final_name + (
        ".exe" if host_os == "windows" and not final_name.endswith(".exe") else ""
    )
    new_path = chosen.with_name(new_name)
    chosen.rename(new_path)
    return new_path


@dataclasses.dataclass
class Args:
    repo: Positional[str]
    tag: str | None = None
    os: str | None = None
    arch: str | None = None
    blacklist: list[str] = dataclasses.field(default_factory=list)
    no_decompress: bool = False
    bin_name: Annotated[str | None, arg(name="bin-name", aliases=["-b"])] = None
    dest: Annotated[Path, arg(name="dest", aliases=["-d"])] = Path(".")
    list_version: Annotated[bool, arg(name="list", aliases=["-l"])] = False
    choose_bin_file: Annotated[bool, arg(name="choose-bin-file")] = False


def main() -> None:
    """Main entry point for the CLI tool."""
    args = tyro.cli(Args)

    # Defaults
    host_os = args.os or get_host_os()
    host_arch = args.arch or get_host_arch()

    # Get repo name
    _, repo_name = args.repo.split("/", 1)

    # If listing releases, print tags and exit
    if getattr(args, "list_version", False):
        owner, repo_only = args.repo.split("/", 1)
        url = f"https://api.github.com/repos/{owner}/{repo_only}/releases"
        response = httpx.get(url)
        response.raise_for_status()
        releases = response.json()
        for rel in releases:
            tag = rel.get("tag_name")
            if tag:
                print(tag)
        return

    # Fetch assets
    assets = get_release_assets(args.repo, args.tag)

    # Match
    matches = match_assets(assets, host_os, host_arch, args.blacklist)

    # Choose
    asset: Asset | None = choose_asset(matches)
    if not asset:
        print("No matching asset found.")
        return

    # Download
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir) / asset["name"]
        download_asset(asset, temp_path)

        # Handle no-decompress: copy archive as-is to destination
        install_dir = Path(args.dest)
        install_dir.mkdir(parents=True, exist_ok=True)
        if args.no_decompress:
            final_path = install_dir / temp_path.name
            shutil.copy2(temp_path, final_path)
            print(f"Saved {final_path}")
            return

        # Unpack and rename
        extract_dir = Path(temp_dir) / "extract"
        extract_dir.mkdir()
        final_name = args.bin_name or repo_name
        binary_path = unpack_asset(
            temp_path,
            extract_dir,
            final_name,
            host_os,
            choose_bin_file=args.choose_bin_file,
        )

        if not binary_path:
            print("Failed to extract binary.")
            return

        # Install to destination directory
        final_path = install_dir / binary_path.name
        shutil.copy2(binary_path, final_path)

        # Ensure POSIX execute permission on Unix-like systems for the installed binary
        if platform.system().lower() in ("linux", "darwin"):
            mode = final_path.stat().st_mode
            with contextlib.suppress(OSError):
                final_path.chmod(mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

        print(f"Installed {final_path}")


if __name__ == "__main__":
    main()
