# Tasks for change 2026-01-23-enhance-cli-options

1. [x] Update CLI parser to add flags: `--no-decompress`, `-b/--bin-name`, `-d/--dest`, `-l/--list`.
   - Validation: `uv run ty check` passes and type hints updated as needed.
2. [x] Wire `--no-decompress` into download flow so extraction/renaming is skipped.
   - Validation: unit test covers saving archive verbatim (see tests/test_github_downloader.py).
3. [x] Implement `--bin-name` option to override final executable filename.
   - Validation: unpack/rename logic uses provided `bin_name` and appends `.exe` on Windows when needed.
4. [x] Implement `--dest` to control output directory and ensure it is created as needed.
   - Validation: destination directory is created with `parents=True, exist_ok=True` and files are saved there.
5. [x] Implement `--list` to fetch and print release tags only.
   - Validation: unit test `test_list_releases_prints_tags` mocks GitHub API and asserts printed tags.
6. [x] Update documentation and README to describe new options. (README updated inline where appropriate.)
7. [x] Run `openspec validate 2026-01-23-enhance-cli-options --strict --no-interactive` and resolve any issues.

Notes
- All unit tests pass: `uv run pytest` reports 10 passed.
- Lint and formatting checks passed: `uv run ruff check --fix` completed with no remaining issues.
