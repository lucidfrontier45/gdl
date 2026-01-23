# Tasks for Adding GitHub Binary Downloader

1. [x] Add dependencies: httpx and tyro to pyproject.toml
2. [x] Create new module src/github_downloader.py with basic structure
3. [x] Implement platform detection functions (OS and arch)
4. [x] Add GitHub API functions to fetch releases and assets
5. [x] Implement asset matching logic (repo, tag, os, arch, blacklist)
6. [x] Add user choice prompt for multiple matches
7. [x] Implement download function using httpx
8. [x] Add unpacking logic for zip and tar.gz
9. [x] Implement binary extraction and renaming
10. [x] Add CLI interface with tyro
11. [x] Write unit tests for platform detection and matching
12. [x] Write integration tests for download and unpack
13. [x] Run ruff check --fix and ruff format
14. [x] Run ty check to ensure type safety
15. [x] Run pytest to validate tests
16. [x] Update AGENTS.md if needed (add new commands)
17. [x] Test manually on different platforms (if possible)