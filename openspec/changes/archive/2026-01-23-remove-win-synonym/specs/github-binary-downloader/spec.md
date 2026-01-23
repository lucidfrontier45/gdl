## MODIFIED Requirements

### Requirement: OS and Arch Options
The tool SHALL support the following OS and arch options: windows (accepts win32), linux, macos (accepts mac, darwin) for OS; x86_64 (accepts amd64, x64), aarch64 (accepts arm64) for arch.

#### Scenario: Alternative OS names
Given os "win32"
When processing
Then treats as "windows"

#### Scenario: Alternative arch names
Given arch "amd64"
When processing
Then treats as "x86_64"</content>
<parameter name="filePath">D:\workspace\gdl\openspec\changes\remove-win-synonym\specs\github-binary-downloader\spec.md