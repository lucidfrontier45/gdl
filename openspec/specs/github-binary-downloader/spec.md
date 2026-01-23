# github-binary-downloader Specification

## Purpose
TBD - created by archiving change add-github-binary-downloader. Update Purpose after archive.
## Requirements
### Requirement: Download Asset by Repo, Tag, OS, Arch
The tool SHALL allow downloading a GitHub release asset specified by repository, tag, operating system, and architecture.

#### Scenario: User specifies all parameters
Given a repo "owner/repo", tag "v1.0", os "linux", arch "x86_64"
When the tool is run with these parameters
Then it downloads the matching asset

#### Scenario: Tag defaults to latest
Given a repo "owner/repo", no tag specified
When the tool is run
Then it uses the latest release tag

### Requirement: Platform Defaults
The tool SHALL use the host's OS and architecture as defaults if not specified.

#### Scenario: Default OS and arch
Given host is Windows x86_64
When no os or arch specified
Then uses "windows" and "x86_64"

### Requirement: OS and Arch Options
The tool SHALL support the following OS and arch options: windows, linux, macos for OS; x86_64 (accepts amd64, x64), aarch64 (accepts arm64) for arch.

#### Scenario: Alternative arch names
Given arch "amd64"
When processing
Then treats as "x86_64"

### Requirement: Multiple Assets Handling
If multiple assets match, the tool SHALL prompt user to choose.

#### Scenario: Multiple matches
Given repo has assets for linux-x86_64 and linux-aarch64
When os="linux", no arch specified (host is x86_64)
Then prompts user to choose between the two

### Requirement: Blacklist Filtering
The tool SHALL support blacklist words to exclude assets.

#### Scenario: Blacklist words
Given blacklist ["debug", "test"]
When assets include "binary-debug.zip"
Then excludes it from selection

### Requirement: Unpacking and Renaming
The tool SHALL unpack compressed assets (zip, tar.gz), extract the executable, and rename to the repo name with .exe on Windows.

#### Scenario: Unpack zip
Given asset is "binary.zip" containing "binary"
When downloaded and host is Linux
Then extracts "binary" and renames to "repo-name"

### Requirement: Dependencies
The tool SHALL use httpx for HTTP requests and tyro for CLI parsing.

#### Scenario: CLI parsing
Given arguments parsed by tyro
When tool runs
Then uses tyro for argument handling

