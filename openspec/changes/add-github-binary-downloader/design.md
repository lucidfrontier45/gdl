# Design for GitHub Binary Downloader

## Architecture Overview
The tool will be a new Python script/module in the src/ directory, following the project's structure. It will be a CLI application using tyro for argument parsing.

## Key Components
- Platform detection: Use platform module to detect OS and architecture
- GitHub API interaction: Use httpx to fetch release data and download assets
- Asset matching: Filter assets based on OS, arch, tag, and blacklist
- Unpacking: Use standard libraries (zipfile, tarfile) for extraction
- Installation: Place binary in a PATH directory (e.g., ~/.local/bin)

## Trade-offs
- Using httpx instead of requests: httpx is async-capable, better for modern Python, aligns with project's use of modern libs
- Tyro for CLI: Simple, type-safe CLI parsing
- No GUI: CLI-only for simplicity
- Single binary extraction: Assumes one executable per archive

## Dependencies
- httpx: HTTP client
- tyro: CLI parser
- Standard libs: platform, zipfile, tarfile, pathlib

No new architectural patterns introduced.