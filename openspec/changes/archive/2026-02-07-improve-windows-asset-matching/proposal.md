## Why

Windows asset matching is incomplete. Asset files containing OS indicators like "windows", "win", "win32", or "win64" are not consistently matched to OS=windows. Additionally, win32/win64 variants should be recognized as x86_64 architecture.

## What Changes

- Add OS=windows matching for assets containing: "windows", "win", "win32", "win64"
- Map win32/win64 indicators to Arch=x86_64
- Ensure case-insensitive pattern matching

## Capabilities

### New Capabilities
- `windows-asset-matching`: Enhanced pattern matching for Windows OS and x86_64 architecture detection in asset filenames

### Modified Capabilities
- None (implementation enhancement, no spec-level requirement changes)

## Impact

- Affected code: Asset matching/filename parsing logic
- No breaking changes - purely additive pattern matching
- Improves Windows platform asset detection accuracy
