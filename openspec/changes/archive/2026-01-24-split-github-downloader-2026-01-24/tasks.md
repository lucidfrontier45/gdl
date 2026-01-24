Tasks

1. Create spec deltas for each capability/module
   - `platform` — requirements for OS/arch detection and synonyms
   - `github` — requirements for listing, matching and downloading assets
   - `archive` — requirements for unpacking and selecting binary files
   - `logic` — orchestration behaviour and error handling
   - `cli` — command-line interface and flags

2. Add design notes for naming, interfaces and error semantics (`design.md`).

3. Implement files under `src/`:
   - `src/gdl/platform.py` (done)
   - `src/gdl/github.py` (done)
   - `src/gdl/archive.py` (done)
   - `src/gdl/logic.py` (done)
   - `src/gdl/cli_impl.py` (done) — `src/gdl/cli.py` updated to delegate
   - `src/gdl/github_downloader.py` shim updated to delegate (done)

4. Add unit tests under `tests/` for each module.

5. Run linters and type checks; fix issues.

6. Validate behaviour via an integration test that mocks GitHub API and an archive file.

Completed work notes:
- Implemented core modules and preserved legacy import paths via a shim in `src/gdl/github_downloader.py`.


Validation

- Tests pass: `uv run pytest` (or equivalent in environment).
- `uv run ty check` passes.

Notes

- Keep changes small and iterative; implement core functionality first then expand.
