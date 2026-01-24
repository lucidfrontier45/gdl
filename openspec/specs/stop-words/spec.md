# stop-words Specification

## Purpose
TBD - created by archiving change 2026-01-24-rename-blacklist-to-stop-words. Update Purpose after archive.
## Requirements
### Requirement: Stop Words Filtering
The tool SHALL support stop words to exclude assets by name.

#### Scenario: Stop words filter
Given stop_words ["debug", "test"]
When assets include "binary-debug.zip"
Then excludes it from selection

#### Scenario: Remove blacklist option
Given command-line uses `--blacklist debug`
When processing arguments
Then the tool rejects the option and returns an error indicating the flag has been removed; documentation points users to use `--stop-words` instead

