# GitHub asset selection and download

## ADDED Requirements

### Requirement: List release assets
The system SHALL list assets for a given repository and release tag (or latest if tag omitted).

#### Scenario: List latest release
Given a repo with a latest release containing assets
When requested without tag
Then returns the assets from the latest release

### Requirement: Asset matching
The system SHALL match assets to OS and arch using synonyms and best-effort substring matching.

#### Scenario: Exact match
Given assets named `tool-linux-x86_64.tar.gz` and `tool-linux-aarch64.tar.gz`
When matching for `linux` and `x86_64`
Then selects `tool-linux-x86_64.tar.gz`

#### Scenario: Multiple matches
Given multiple assets match
When matching returns more than one candidate
Then the chooser raises an `AmbiguousAssetError` (or returns multiple candidates for CLI to prompt)

### Requirement: Download asset
The system SHALL download a chosen asset to a destination path and return the path to the saved file.

#### Scenario: Successful download
Given a valid asset URL
When download completes
Then the file exists at the provided destination
