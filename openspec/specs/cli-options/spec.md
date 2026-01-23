# cli-options Specification

## Purpose
TBD - created by archiving change 2026-01-23-enhance-cli-options. Update Purpose after archive.
## Requirements
### Requirement: --no-decompress flag
The tool SHALL support a `--no-decompress` flag that, when provided, saves the downloaded asset exactly as-is and does not attempt to decompress, extract, or rename any contained executable.

#### Scenario: Preserve archive when requested
Given a repository asset `app.tar.gz`
When a user runs the tool with `--no-decompress` and a matching asset is selected
Then the tool saves `app.tar.gz` to the destination directory without extracting its contents

### Requirement: --bin-name / -b option
The tool SHALL support a `--bin-name` (short `-b`) option allowing the caller to specify the final executable filename. When not provided the tool SHALL default to using the repository name (adding `.exe` on Windows when appropriate).

#### Scenario: Custom binary name
Given an extracted executable `mybinary`
When the user passes `-b custom-name`
Then the saved executable is named `custom-name` (or `custom-name.exe` on Windows)

### Requirement: --dest / -d option
The tool SHALL support a `--dest` (short `-d`) option that specifies the destination directory where the downloaded file or extracted binary will be saved. If not provided the default destination SHALL be the current working directory (`.`).

#### Scenario: Custom destination
Given the user passes `-d /tmp/artifacts`
When a file is saved
Then it is placed under `/tmp/artifacts` and the directory is created if it does not exist

### Requirement: --list / -l option
The tool SHALL support a `--list` (short `-l`) flag which lists available release versions for the specified repository and exits without downloading assets.

#### Scenario: List releases
Given a repository with releases `v1.0`, `v1.1`, `v2.0`
When the user runs the tool with `--list`
Then the tool outputs a newline-separated list of release tags to stdout and exits with status 0

