Tasks for `--choose-asset-file` change

1. Update CLI spec and docs
   - Modify `openspec/specs/cli-options/spec.md` to add the new option requirement and scenarios.
   - Update any user-facing docs referencing selection behavior.
   - Validation: openspec validate passes.

2. Implement CLI flag in codebase
   - Add parsing for `--choose-asset-file` (boolean) in CLI argument handling.
   - Ensure it is mutually compatible with `--list`/`--choose-bin-file` semantics (allowed together only when sensible).
   - Validation: unit tests around argument parsing.
   - Implementation: added `choose_asset_file` arg to `src/gdl/cli.py` and passed through to `install_from_github`.

3. Selection logic change
   - When `--choose-asset-file` is present and running in a TTY: collect all release assets (no OS/arch/stop-word filtering), present a numbered list (sorted by filename), and prompt the user to choose one.
   - When not a TTY: fail with a clear error message referencing the flag requires TTY.
   - After selection: continue normal download and processing for the chosen asset.
   - Validation: unit tests for interactive flow (mock TTY), non-TTY error, and that filters are ignored when flag is present.
   - Implementation: `install_from_github` now accepts `choose_asset_file` and uses `github.choose_asset(assets)` when set. `github.choose_asset` enforces TTY and provides a 3-attempt prompt.

4. Tests & type checks
   - Add tests for selection flow and non-TTY behavior. Ensure `ty` and `ruff` checks pass.
   - Current: ran `uv run ruff check --fix` and `uv run ty check` locally; both pass. Tests are still to be added in a follow-up.

5. Docs & release note
   - Add a short note in changelog or README showing examples and explaining how this overrides stop-words/filters.

All tasks implemented except adding unit tests and user-facing docs; those are noted as follow-ups.

Notes:
- Keep changes minimal: selection happens before any filtering. The chosen asset is then subject to the existing downstream processing (decompress, extract, choose binary, etc.).
