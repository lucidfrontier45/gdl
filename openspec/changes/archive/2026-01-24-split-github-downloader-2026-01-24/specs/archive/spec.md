# Archive extraction and binary selection

## ADDED Requirements

### Requirement: Unpack compressed assets
The system SHALL unpack common archive formats (zip, tar.gz) to a destination directory.

#### Scenario: Unpack zip
Given a zip archive containing `bin/tool` and `README.md`
When unpacked
Then both files are extracted preserving relative paths

### Requirement: Select binary file
The system SHALL choose an executable/binary file from the extracted files using heuristics: executable permission, location in `bin/`, exact name match, or largest file as fallback.

#### Scenario: Choose executable
Given extracted files include `bin/tool` (executable) and `lib/lib.so`
When choosing binary
Then returns `bin/tool`

#### Scenario: No executable
Given extracted files contain only data files
When choosing binary
Then raises `ExtractionError` indicating no suitable binary found
