# windows-asset-matching Specification

## Purpose
TBD - created by syncing change `improve-windows-asset-matching`. Refine Purpose after implementation is complete.

## Requirements

### Requirement: Match Windows OS indicators in asset filenames
The system SHALL match asset filenames containing "windows", "win", "win32", or "win64" (case-insensitive) to OS=windows.

#### Scenario: Asset filename with "windows"
- **WHEN** asset filename contains "windows" (any case)
- **THEN** system sets OS=windows

#### Scenario: Asset filename with "win"
- **WHEN** asset filename contains "win" (any case)
- **THEN** system sets OS=windows

#### Scenario: Asset filename with "win32"
- **WHEN** asset filename contains "win32" (any case)
- **THEN** system sets OS=windows

#### Scenario: Asset filename with "win64"
- **WHEN** asset filename contains "win64" (any case)
- **THEN** system sets OS=windows

### Requirement: Map win32/win64 to x86_64 architecture
The system SHALL map asset filenames containing "win32" or "win64" (case-insensitive) to Arch=x86_64.

#### Scenario: Asset filename with "win32"
- **WHEN** asset filename contains "win32" (any case)
- **THEN** system sets Arch=x86_64

#### Scenario: Asset filename with "win64"
- **WHEN** asset filename contains "win64" (any case)
- **THEN** system sets Arch=x86_64

### Requirement: Case-insensitive pattern matching
All Windows OS and architecture pattern matching SHALL be case-insensitive.

#### Scenario: Mixed case "Windows"
- **WHEN** asset filename contains "Windows"
- **THEN** system sets OS=windows

#### Scenario: Uppercase "WIN64"
- **WHEN** asset filename contains "WIN64"
- **THEN** system sets OS=windows AND Arch=x86_64
