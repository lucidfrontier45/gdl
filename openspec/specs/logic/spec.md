# logic Specification

## Purpose
TBD - created by archiving change split-github-downloader-2026-01-24. Update Purpose after archive.
## Requirements
### Requirement: Orchestrate install flow
The system SHALL combine platform detection, GitHub asset discovery, download, extraction and final install into a single `install_from_github` operation.

#### Scenario: Full install
Given repo `owner/repo`, tag omitted, default host OS/arch
When `install_from_github` is invoked
Then it detects host platform, lists assets, chooses a matching asset, downloads it, extracts the binary and saves it under destination

### Requirement: Error propagation
The system SHALL return meaningful errors on failures (e.g., no asset found, ambiguous assets, download failure, extraction failure).

#### Scenario: No assets found
Given repo has no releases with matching assets
When attempted
Then returns `NotFoundError` and exits gracefully

