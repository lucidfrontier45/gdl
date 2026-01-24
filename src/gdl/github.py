"""GitHub asset listing, matching and downloading."""

import sys
from collections.abc import Sequence
from pathlib import Path
from typing import TypedDict

import httpx
import tqdm


class Asset(TypedDict):
    name: str
    browser_download_url: str


def list_release_assets(repo: str, tag: str | None = None) -> list[Asset]:
    owner, repo_name = repo.split("/", 1)
    url = f"https://api.github.com/repos/{owner}/{repo_name}/releases"
    url = f"{url}/tags/{tag}" if tag else f"{url}/latest"
    response = httpx.get(url)
    response.raise_for_status()
    release = response.json()
    return release.get("assets", [])


def match_assets(
    assets: Sequence[Asset],
    os: str,
    arch: str,
    stop_words: list[str],
    os_synonyms: dict[str, tuple[str, ...]],
    arch_synonyms: dict[str, tuple[str, ...]],
) -> list[Asset]:
    os_terms = os_synonyms.get(os, (os,))
    arch_terms = arch_synonyms.get(arch, (arch,))

    matches: list[Asset] = []
    for asset in assets:
        name = asset["name"].lower()
        if not any(term in name for term in os_terms) or not any(
            term in name for term in arch_terms
        ):
            continue
        if any(word.lower() in name for word in stop_words):
            continue
        matches.append(asset)
    return matches


def choose_asset(assets: Sequence[Asset]) -> Asset | None:
    if not assets:
        return None
    if len(assets) == 1:
        return assets[0]
    # Interactive selection: require TTY for user prompts

    if not sys.stdin.isatty() or not sys.stdout.isatty():
        raise RuntimeError(
            "--choose-asset-file requires an interactive terminal (TTY); "
            "remove the flag to use automatic filtering."
        )

    print("Multiple assets found:")
    for i, asset in enumerate(assets):
        print(f"{i + 1}: {asset['name']}")

    attempts = 0
    while attempts < 3:
        attempts += 1
        try:
            choice = int(input("Choose an asset (number): ")) - 1
            if 0 <= choice < len(assets):
                return assets[choice]
            else:
                print("Invalid choice.")
        except ValueError:
            print("Please enter a number.")
    raise RuntimeError("Too many invalid attempts selecting asset; aborting.")


def download_asset(asset: Asset, dest: Path) -> None:
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
