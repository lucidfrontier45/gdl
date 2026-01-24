# choose-bin-file-cli Specification

## Purpose
TBD - created by archiving change improve-bin-file-selection. Update Purpose after archive.
## Requirements
### Requirement: --choose-bin-file CLI option
The tool SHALL provide a boolean CLI flag `--choose-bin-file`. When present, the tool SHALL prompt the user to select which of the extracted candidate files should be treated as the final binary instead of automatically selecting by the default priority rules.

#### Scenario: User chooses file
Given extraction yields files `x` (5KB), `y` (8KB), `z` (1KB)
When user runs with `--choose-bin-file`
Then the tool prompts (candidates presented in descending size order):
1) `y` 8192 bytes
2) `x` 5120 bytes
3) `z` 1024 bytes
And accepts user input `1` to select `y` as the final binary

#### Scenario: Non-interactive environment
Given `--choose-bin-file` is provided in a non-TTY environment
When the tool starts interactive selection
Then it exits with a clear error indicating the flag requires a TTY and suggests removing the flag to auto-select using the default priority rules

