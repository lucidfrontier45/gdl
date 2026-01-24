# choose-largest-and-perm Specification

## Purpose
TBD - created by archiving change improve-bin-file-selection. Update Purpose after archive.
## Requirements
### Requirement: Select final binary by priority
The tool SHALL choose the final binary among extracted candidate files using this priority order:

1. Files with a `.exe` suffix (case-insensitive).
2. Files with Unix execute permission set in the extracted metadata or filesystem.
3. The largest file by byte size.

#### Scenario: .exe preferred
Given extraction results include `run.sh` (5KB) and `program.exe` (4KB)
When selecting the final binary and `--choose-bin-file` is not provided
Then the tool selects `program.exe` because `.exe` suffix has highest priority

#### Scenario: Exec-permission preferred
Given extraction results include `run.sh` (5KB, exec bit set) and `program` (10KB, no exec bit)
When selecting the final binary
Then the tool selects `run.sh` because it has the Unix execute permission

#### Scenario: Fallback to largest
Given extraction results include `a` (10 bytes), `b` (50 bytes), and `c` (20 bytes) and none have `.exe` or exec bit
When selecting the final binary
Then the tool selects `b` (50 bytes) as the final binary

#### Scenario: Tie on size
Given extraction results include `a` (100 bytes) and `b` (100 bytes)
When choosing by size
Then the tool selects the file that is first in lexical order to ensure deterministic selection

### Requirement: Set Execute Permission on Unix-like Systems
When the final binary is saved on a host where the platform is Linux or macOS, the tool SHALL set POSIX execute permission bits for owner, group and others on the final binary file.

#### Scenario: Linux host
Given selected binary `repo-name` saved to destination
When host is Linux
Then the tool sets the file mode to include execute bits (owner/group/other)

#### Scenario: Windows host
Given selected binary saved on Windows
When saving completes
Then no attempt is made to change POSIX permissions

