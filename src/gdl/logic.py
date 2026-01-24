"""Orchestration of the download and install flow."""

import contextlib
import platform
import shutil
import stat
import tempfile
from pathlib import Path

from . import archive, github
from . import platform as platform_mod


def install_from_github(
    repo: str,
    tag: str | None = None,
    os_name: str | None = None,
    arch: str | None = None,
    stop_words: list[str] | None = None,
    dest: Path = Path("."),
    no_decompress: bool = False,
    bin_name: str | None = None,
    choose_bin_file: bool = False,
):
    host_os = os_name or platform_mod.get_host_os()
    host_arch = arch or platform_mod.get_host_arch()

    _, repo_name = repo.split("/", 1)

    assets = github.list_release_assets(repo, tag)
    if stop_words is None:
        stop_words = []
    matches = github.match_assets(
        assets,
        host_os,
        host_arch,
        stop_words,
        platform_mod.os_synonyms,
        platform_mod.arch_synonyms,
    )
    asset = github.choose_asset(matches)
    if not asset:
        raise FileNotFoundError("No matching asset found")

    dest.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        temp_file = td_path / asset["name"]
        github.download_asset(asset, temp_file)

        if no_decompress:
            final_path = dest / temp_file.name
            shutil.copy2(temp_file, final_path)
            return final_path

        extract_dir = td_path / "extract"
        extract_dir.mkdir()
        extracted_files = archive.unpack_archive(temp_file, extract_dir)
        binary = archive.choose_binary(extracted_files, extract_dir)
        if not binary:
            raise RuntimeError("No binary found in archive")

        final_name = (bin_name or repo_name) + (
            ".exe"
            if host_os == "windows" and not (bin_name or repo_name).endswith(".exe")
            else ""
        )
        final_path = dest / final_name
        shutil.copy2(binary, final_path)

        # Ensure exec permissions on Unix-like
        if platform.system().lower() in ("linux", "darwin"):
            mode = final_path.stat().st_mode
            with contextlib.suppress(OSError):
                final_path.chmod(mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

        return final_path
