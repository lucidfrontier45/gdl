Design

High level

Split responsibilities into five modules. Keep public function surfaces small and typed. The existing `github_downloader.py` will be removed after refactor; for migration add a small shim if callers still import it.

Interfaces

- platform.py
  - get_host() -> tuple[str, str]  # (os, arch)
  - os_synonyms: dict[str, tuple[str,...]]
  - arch_synonyms: dict[str, tuple[str,...]]

- github.py
  - list_release_assets(owner: str, repo: str, tag: str | None) -> list[Asset]
  - choose_asset(assets, os: str, arch: str) -> Asset | None
  - download_asset(asset: Asset, dest: Path) -> Path

- archive.py
  - unpack_archive(path: Path, dest: Path) -> list[Path]  # extracted files
  - choose_binary(files: list[Path]) -> Path  # pick bin file (largest or executable)

- logic.py
  - install_from_github(owner, repo, tag, dest, prefer_asset_name: str | None)

- cli.py
  - parse args and call logic.install_from_github

Error handling

- Return or raise clear exceptions: NotFoundError, AmbiguousAssetError, ExtractionError, DownloadError.

Testing

- Unit tests for synonym mappings, matching rules (e.g., windows -> win/Windows), asset selection when multiple assets match, and archive extraction edge cases (multiple executables, no executables).

Notes on heuristics

- Asset matching: prefer exact os+arch matches, then synonyms, then best-effort contains checks. If multiple assets tie, choose the largest.
- Binary selection: prefer files with executable bit set or files under `bin/` or a top-level file matching repo name; fallback to largest file.
