# Enhance CLI Options

Change-id: 2026-01-23-enhance-cli-options

This proposal adds new CLI options to the github-binary-downloader tooling to make downloads more flexible and discoverable:

- `--no-decompress` — Save downloaded file verbatim, do not extract or rename
- `-b, --bin-name` — Explicit executable filename (defaults to repository name when unspecified)
- `-d, --dest` — Destination directory for saved file(s) (default: `.`)
- `--list, -l` — List available release versions for a repository and exit (CLI name: `list_version` with aliases `-l/--list`)

Motivation
- Users need more control over how release assets are saved and named.
- Allow quickly listing available release versions without performing downloads.

Scope
- Add CLI flags as described above and update the specification for behavior.
- Keep current defaults and unpacking behavior unless `--no-decompress` is given.
- Ensure `--list` is non-destructive and returns machine-friendly output.

Non-goals
- Implementing advanced heuristics for asset selection beyond existing blacklist and platform matching.

Acceptance criteria
- New flags are specified in the OpenSpec delta for `github-binary-downloader`.
- Each flag has at least one scenario in the spec demonstrating expected behavior.
- `openspec validate <id> --strict --no-interactive` passes with no errors.
