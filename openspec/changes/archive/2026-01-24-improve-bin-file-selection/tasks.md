Tasks for improve-bin-file-selection

1. Inspect current extraction code paths to identify where candidate files are enumerated (non-coding research task).
   - Validation: list of code locations and brief notes in a single markdown bullet list.

2. Add selection logic that picks the largest file among extracted candidates when multiple candidates exist.
   - Unit tests: add tests that simulate extraction output with multiple files and assert the largest is chosen.

3. Add platform detection and set POSIX execute permission on Linux/macOS for the final chosen binary.
   - Unit/Integration tests: verify execute bit set when running on a Linux-like environment; for CI, mock os detection or use monkeypatch to simulate.

4. Add CLI option `--choose-bin-file` (boolean flag) that triggers an interactive prompt listing candidate files and asking the user to choose one.
   - UX notes: use a simple numbered prompt (e.g., "Choose file [1..N]:") and validate numeric input. Default to 1 (first) if user just presses Enter.
   - Tests: coverage for the prompt logic by mocking stdin responses.

5. Wire the flag into the main flow: when `--choose-bin-file` is present, skip automatic largest-file selection and prompt the user.
   - Ensure non-interactive CI usage is documented: if `--choose-bin-file` is used in a non-TTY environment, fail with a clear error suggesting using the default selection or avoid the flag.

6. Update relevant specs and CLI documentation to include the new behavior and option.
   - Add changelog/usage examples.

7. Run linters, type checks, and unit tests; fix issues until green.

Notes and dependencies
- Task 1 must be completed before changing selection logic to ensure correct integration points are modified.
- Tests requiring POSIX execute bit should be written to mock platform behavior for reliability on CI/Windows.
