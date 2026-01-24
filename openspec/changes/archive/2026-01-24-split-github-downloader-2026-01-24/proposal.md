Goal

Split the single `github_downloader.py` implementation into five focused modules:

- `platform.py` — determine host OS/arch and provide canonical synonyms
- `github.py` — list, match, choose and download release assets from GitHub
- `archive.py` — unpack downloaded archives and extract binary file(s)
- `logic.py` — orchestrate platform detection, asset selection, download and unpack steps
- `cli.py` — command-line interface and argument parsing, delegates to `logic.py`

Motivation

Smaller, well-scoped modules improve testability, make responsibilities explicit, and simplify future enhancements such as adding more archive formats, better asset matching heuristics, or richer CLI flags.

Scope

- Create design and specs for the split.
- Add tasks to implement modules and tests.
- This change is a refactor only — no behaviour change is intended beyond keeping existing functionality.

Non-goals

- Adding new public features (progress bars, auto-updates) — those belong to separate proposals.

Acceptance criteria

- New modules with clear exported functions and documented expectations exist in `src/` (implementation step).
- Unit tests cover platform detection synonyms, asset selection heuristics, archive extraction of a single binary, and CLI wiring.
- Existing end-to-end behaviour remains unchanged (download chosen asset and extract binary to destination).

Risks

- Slight behaviour drift if asset-matching heuristics change; mitigated by tests that mirror current behaviour.

Migration

- Implement adapters to keep the previous import path (if necessary) for backward compatibility or update internal callers.
