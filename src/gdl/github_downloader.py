"""GitHub Binary Downloader CLI Tool."""

import dataclasses
import platform
import shutil
import tarfile
import tempfile
import zipfile
from collections.abc import Sequence
from pathlib import Path
from typing import TypedDict

import httpx
import tyro
from tyro.conf import Positional


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
        with dest.open("wb") as f:
            for chunk in response.iter_bytes():
                f.write(chunk)


def unpack_asset(
    asset_path: Path, extract_dir: Path, repo_name: str, host_os: str
) -> Path | None:
    """Unpack compressed asset and return path to the renamed executable binary."""
    if asset_path.suffix == ".zip":
        with zipfile.ZipFile(asset_path, "r") as zf:
            zf.extractall(extract_dir)
    elif asset_path.suffixes == [".tar", ".gz"]:
        with tarfile.open(asset_path, "r:gz") as tf:
            tf.extractall(extract_dir, filter="data")
    else:
        # Not compressed, assume it's the binary
        binary_path = asset_path
        new_name = f"{repo_name}.exe" if host_os == "windows" else repo_name
        new_path = asset_path.with_name(new_name)
        binary_path.rename(new_path)
        return new_path

    # Find the executable binary
    for file_path in extract_dir.rglob("*"):
        if file_path.is_file() and (
            file_path.stat().st_mode & 0o111 or file_path.suffix == ".exe"
        ):
            new_name = f"{repo_name}.exe" if host_os == "windows" else repo_name
            new_path = file_path.with_name(new_name)
            file_path.rename(new_path)
            return new_path
    return None


@dataclasses.dataclass
class Args:
    repo: Positional[str]
    tag: str | None = None
    os: str | None = None
    arch: str | None = None
    blacklist: list[str] = dataclasses.field(default_factory=list)


def main() -> None:
    """Main entry point for the CLI tool."""
    args = tyro.cli(Args)

    # Defaults
    host_os = args.os or get_host_os()
    host_arch = args.arch or get_host_arch()

    # Get repo name
    _, repo_name = args.repo.split("/", 1)

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

        # Unpack and rename
        extract_dir = Path(temp_dir) / "extract"
        extract_dir.mkdir()
        binary_path = unpack_asset(temp_path, extract_dir, repo_name, host_os)

        if not binary_path:
            print("Failed to extract binary.")
            return

        # Install to current directory
        install_dir = Path.cwd()
        final_path = install_dir / binary_path.name
        shutil.copy2(binary_path, final_path)
        print(f"Installed {final_path}")


if __name__ == "__main__":
    main()
