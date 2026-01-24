"""Archive unpacking and binary selection."""

import shutil
import tarfile
import zipfile
from pathlib import Path


def unpack_archive(asset_path: Path, extract_dir: Path) -> list[Path]:
    """Unpack supported archives to extract_dir and return list of extracted files."""
    if asset_path.suffix == ".zip":
        _unpack_zip(asset_path, extract_dir)
    elif asset_path.suffixes == [".tar", ".gz"]:
        _unpack_tar_gz(asset_path, extract_dir)
    else:
        # Not an archive; treat as single binary
        return [asset_path]

    return [p for p in extract_dir.rglob("*") if p.is_file()]


def _unpack_zip(asset_path: Path, extract_dir: Path) -> None:
    """Extract zip archive safely into extract_dir."""
    with zipfile.ZipFile(asset_path, "r") as zf:
        for member in zf.namelist():
            member_path = extract_dir / member
            # Prevent path traversal
            if not str(member_path.resolve()).startswith(str(extract_dir.resolve())):
                continue
            if member.endswith("/"):
                member_path.mkdir(parents=True, exist_ok=True)
            else:
                member_path.parent.mkdir(parents=True, exist_ok=True)
                with zf.open(member) as src, member_path.open("wb") as dst:
                    shutil.copyfileobj(src, dst)


def _unpack_tar_gz(asset_path: Path, extract_dir: Path) -> None:
    """Extract tar.gz archive safely into extract_dir."""
    with tarfile.open(asset_path, "r:gz") as tf:
        for member in tf.getmembers():
            if not member.isreg():
                continue
            member_path = extract_dir / member.name
            # Prevent path traversal
            if not str(member_path.resolve()).startswith(str(extract_dir.resolve())):
                continue
            member_path.parent.mkdir(parents=True, exist_ok=True)
            src = tf.extractfile(member)
            if src is None:
                continue
            with src as src_file, member_path.open("wb") as dst:
                shutil.copyfileobj(src_file, dst)


def choose_binary(files: list[Path], extract_dir: Path) -> Path | None:
    """Choose the binary from extracted files using heuristics."""
    if not files:
        return None

    # 1) .exe candidates
    exe_candidates = [p for p in files if p.suffix.lower() == ".exe"]

    def pick_largest_with_tiebreak(candidates: list[Path]) -> Path:
        return sorted(
            candidates,
            key=lambda p: (-p.stat().st_size, str(p.relative_to(extract_dir))),
        )[0]

    if exe_candidates:
        return pick_largest_with_tiebreak(exe_candidates)

    # 2) executable bit
    exec_candidates = [p for p in files if p.stat().st_mode & 0o111]
    if exec_candidates:
        return pick_largest_with_tiebreak(exec_candidates)

    # 3) fallback to largest
    return pick_largest_with_tiebreak(files)
