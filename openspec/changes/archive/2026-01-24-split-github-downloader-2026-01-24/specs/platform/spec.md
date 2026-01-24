# Platform detection and synonyms

## ADDED Requirements

### Requirement: Canonical host OS and architecture
The system SHALL expose a function to determine the host's operating system and architecture and return canonical names.

#### Scenario: Host defaults
Given the host is Windows on AMD64
When the function is called without overrides
Then it returns `("windows", "x86_64")`

### Requirement: Synonym mappings
The system SHALL provide synonym mappings for OS and architectures so user input or asset names can be normalized.

#### Scenario: OS synonyms
Given the OS synonym map contains `{"windows": ("win32", "win", "windows"), "macos": ("mac", "darwin", "macos")}`
When input `win32` is normalized
Then it maps to `windows`

#### Scenario: Arch synonyms
Given the arch synonym map contains `{"x86_64": ("amd64", "x64", "x86_64"), "aarch64": ("arm64", "aarch64")}`
When input `amd64` is normalized
Then it maps to `x86_64`
