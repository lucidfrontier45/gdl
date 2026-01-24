Rename 'blacklist' feature to 'stop_words'

Why
- The term "blacklist" is being replaced with "stop_words" to use clearer, less charged language and to align naming across the codebase, specs, and documentation.

Motivation
- The codebase and specs currently use the term "blacklist" to describe a list of words used to filter GitHub release assets. We will rename this capability to `stop_words` to use clearer, less charged language.

 Scope
 - Update the OpenSpec requirement for the github-binary-downloader capability to replace the term and behaviour from "blacklist" to `stop_words`.
 - Remove the old `--blacklist` option entirely; the CLI and public APIs will only accept `--stop-words` going forward. This is a breaking change and must be reflected in release notes and the changelog.

What I examined
- Project specs: `openspec/specs/github-binary-downloader/spec.md` (contains the current "Blacklist Filtering" requirement).
- Code and docs: occurrences of "blacklist" were found in the following files and will need updating as part of implementation:
  - `src/gdl/cli.py`
  - `src/gdl/logic.py`
  - `src/gdl/github.py`
  - `tests/test_github_downloader.py`
  - `README.md`
  - `openspec/changes/*` (several archived changes reference blacklist in their proposals and specs)

 Constraints & Guardrails
 - Keep the change minimal and focused on renaming the feature in specs and proposing the implementation steps. No code changes are included in this proposal stage.
 - This change removes the old `--blacklist` option and is intentionally breaking for external callers; update docs and release notes accordingly.

 Deliverables
 - A spec delta that modifies the existing requirement from "Blacklist Filtering" to "Stop Words Filtering" and removes any backwards-compatibility/deprecation scenarios.
 - A concrete tasks list that maps to the implementation steps required to complete the rename across code, tests and docs, and updates the changelog to call out the breaking change.
