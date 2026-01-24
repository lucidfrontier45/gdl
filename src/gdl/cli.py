"""Main entry point for gdl CLI."""

import dataclasses
from pathlib import Path
from typing import Annotated

import tyro
from tyro.conf import Positional, arg

from .logic import install_from_github


@dataclasses.dataclass
class Args:
    repo: Positional[str]
    tag: str | None = None
    os: str | None = None
    arch: str | None = None
    stop_words: list[str] = dataclasses.field(default_factory=list)
    no_decompress: bool = False
    bin_name: Annotated[str | None, arg(name="bin-name", aliases=["-b"])] = None
    dest: Annotated[Path, arg(name="dest", aliases=["-d"])] = Path(".")
    list_version: Annotated[bool, arg(name="list", aliases=["-l"])] = False
    choose_bin_file: Annotated[bool, arg(name="choose-bin-file")] = False
    choose_asset_file: Annotated[bool, arg(name="choose-asset-file")] = False


def main() -> None:
    args = tyro.cli(Args)

    if args.list_version:
        owner, repo_only = args.repo.split("/", 1)
        url = f"https://api.github.com/repos/{owner}/{repo_only}/releases"
        import httpx

        response = httpx.get(url)
        response.raise_for_status()
        releases = response.json()
        for rel in releases:
            tag = rel.get("tag_name")
            if tag:
                print(tag)
        return

    install_from_github(
        args.repo,
        tag=args.tag,
        os_name=args.os,
        arch=args.arch,
        stop_words=args.stop_words,
        dest=args.dest,
        no_decompress=args.no_decompress,
        bin_name=args.bin_name,
        choose_bin_file=args.choose_bin_file,
        choose_asset_file=args.choose_asset_file,
    )


if __name__ == "__main__":
    main()
