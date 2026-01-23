# Add GitHub Binary Downloader

## Summary
Add a new CLI tool that downloads prebuilt executable binaries from GitHub release pages, matching the host platform, and places them in a PATH directory.

## Why
Users need an easy way to download and install binaries from GitHub releases without manual selection and extraction.

## Motivation
Users need an easy way to download and install binaries from GitHub releases without manual selection and extraction.

## Impact
- New core functionality: CLI tool for downloading platform-specific binaries
- Adds dependencies: httpx, tyro
- No breaking changes to existing code

## Implementation Approach
Create a new Python module with CLI interface using tyro, HTTP client with httpx, automatic platform detection, asset matching, user choice for multiples, blacklist filtering, and unpacking.

## Risk Assessment
Low risk: New standalone tool, no impact on existing code.