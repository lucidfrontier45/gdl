Tasks for rename 'blacklist' -> 'stop_words'

1. Update OpenSpec requirement
   - Modify `openspec/specs/github-binary-downloader/spec.md` to replace the "Blacklist Filtering" requirement with "Stop Words Filtering" and remove any backwards-compatibility or deprecation scenarios for `blacklist`.
   - Validation: `openspec validate <id>` passes.

2. Update code signatures and CLI (implementation stage)
   - Replace function/argument names from `blacklist` to `stop_words` in `src/gdl/cli.py`, `src/gdl/logic.py`, and `src/gdl/github.py`.
   - Remove the `--blacklist` CLI option and only expose `--stop-words`.
   - Validation: `uv run ty check` passes; `uv run ruff check --fix` applied.

3. Update tests
   - Replace test references to `blacklist` with `stop_words` and remove tests that assert `--blacklist` compatibility.
   - Validation: `uv run pytest` passes.

4. Update docs and help text
   - Update `README.md`, docstrings, and CLI help to use `stop_words`. Clearly state that `--blacklist` has been removed and the change is breaking.

5. Cross-reference archived specs and notes
   - Update any archived change proposals or specs that mention "blacklist" where they are relevant to the current capability (optional archive edits for clarity).

6. Release notes
   - Draft a short changelog entry describing the rename and the breaking change (removal of `--blacklist`).

All items completed:
- [x] Update OpenSpec requirement
- [x] Update code signatures and CLI
- [x] Update tests
- [x] Update docs and help text
- [x] Cross-reference archived specs (optional)
- [x] Release notes (draft changelog entry added to README)

Notes
- Keep changes small, run linters and type checks after implementation. If any external-facing APIs use `blacklist` (e.g., package metadata), include them in the changelog and migration notes.
