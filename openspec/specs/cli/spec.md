# cli Specification

## Purpose
TBD - created by archiving change split-github-downloader-2026-01-24. Update Purpose after archive.
## Requirements
### Requirement: CLI flags
The CLI SHALL accept repository (`owner/repo`), optional `--tag`, optional `--os`, `--arch`, `--dest`, and flags to list assets or skip extraction.

#### Scenario: List assets
Given `--list` flag
When invoked for a repo
Then prints available assets and exits

#### Scenario: Skip extraction
Given `--no-decompress` flag
When download completes
Then the raw archive is saved to destination and no extraction occurs

