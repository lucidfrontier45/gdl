# gdl

Download Asset Files from GitHub Release Pages

`gdl` is a command-line tool that downloads prebuilt executable binaries from GitHub release pages, automatically matching the host platform (OS and architecture). It supports filtering, unpacking compressed archives, and installing the binary to the current directory.

## Features

- Automatic platform detection (OS: Windows, Linux, macOS; Arch: x86_64, aarch64)
- Flexible asset matching with synonyms (e.g., "win" for Windows, "amd64" for x86_64)
- Blacklist filtering to exclude unwanted assets
- Unpacking of ZIP and TAR.GZ archives
- Secure extraction with filters to prevent malicious archive issues
- HTTP redirect handling

## Installation

Clone the repository and install dependencies:

```bash
uv sync
```

## Usage

```bash
uv run python -m gdl [OPTIONS] REPO
```

### Arguments

- `REPO`: GitHub repository in the format `owner/repo` (e.g., `microsoft/vscode`)

### Options

- `--tag TEXT`: Specific release tag (defaults to latest)
- `--os TEXT`: Override host OS (windows, linux, macos)
- `--arch TEXT`: Override host architecture (x86_64, aarch64)
 - `--stop-words TEXT`: Words to exclude from asset names (can be specified multiple times)
- `--help`: Show help message
 - `--no-decompress`: Save downloaded file without extracting/decompressing it
 - `-b, --bin-name TEXT`: Specify the final executable filename (defaults to repository name; `.exe` is added on Windows when appropriate)
 - `-d, --dest PATH`: Destination directory for saved file or extracted binary (defaults to `.`). Directory is created if needed.
 - `-l, --list`: List available release versions for the specified repository and exit (exposed as `list_version` in the CLI data model)

### Examples

Download the latest release binary for the host platform:

```bash
uv run python -m gdl microsoft/vscode
```

Download a specific tag:

```bash
uv run python -m gdl microsoft/vscode --tag 1.80.0
```

Override platform:

```bash
uv run python -m gdl microsoft/vscode --os linux --arch x86_64
```

Exclude debug builds:

```bash
uv run python -m gdl microsoft/vscode --stop-words debug --stop-words test
```

## Platform Support

- **OS**: windows (synonyms: win32), linux, macos (synonyms: mac, darwin)
- **Arch**: x86_64 (synonyms: x64, amd64), aarch64 (synonyms: arm64)

## Requirements

- Python 3.13+
- httpx
- tyro
