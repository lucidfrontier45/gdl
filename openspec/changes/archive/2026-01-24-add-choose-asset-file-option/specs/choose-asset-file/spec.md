# choose-asset-file Specification

## Purpose
Allow users to manually select a release asset file when automatic filtering would otherwise exclude or hide it.

## ADDED Requirements

### Requirement: --choose-asset-file CLI option
The tool SHALL provide a boolean CLI flag `--choose-asset-file`. When present, the tool SHALL list all release asset files for the chosen release and prompt the user to select one. While this flag is present, the tool SHALL NOT apply OS, architecture, or stop-words filters to the list presented to the user.

#### Scenario: User selects from all assets
Given a release with assets `a.tar.gz`, `b-linux-amd64`, `c-windows.zip` and stop-words that would normally exclude `c`,
When the user runs the tool with `--choose-asset-file` in a TTY,
Then the tool presents all three assets to the user and accepts a numeric selection; the chosen asset is downloaded and processing continues.

#### Scenario: Non-interactive environment
Given `--choose-asset-file` is provided in a non-TTY environment,
When the tool attempts to prompt,
Then it exits with a clear error indicating the flag requires a TTY and suggests removing it to use normal filtered selection.

#### Scenario: Interaction format
Given the user runs in a TTY,
When assets are presented,
Then they appear as a numbered list sorted by filename with sizes where available, the tool accepts a valid number and re-prompts up to 3 times for invalid input before failing.

#### Scenario: --list interaction
Given the user provides both `--list` and `--choose-asset-file`,
When the tool begins execution,
Then it performs `--list` behaviour (list releases) and exits early; `--choose-asset-file` is ignored and documented as not compatible with `--list`.
