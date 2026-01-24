Add `--choose-asset-file` CLI option

What: introduce a boolean CLI option `--choose-asset-file` that, when provided, lists all release asset files and prompts the user to choose one. While this flag is active the normal asset candidate filters (OS, architecture and configured stop-words) are ignored.

Why: users sometimes need to select an asset that does not match inferred platform metadata or is intentionally excluded by stop-words. An explicit choice mode makes the tool useful for manual recovery, testing, or when platform metadata is missing/incorrect.

Scope: small CLI and selection-behaviour change. No new external dependencies. Interaction is identical to `--choose-bin-file` but operates on release assets (before any filtering) and overrides stop-words and platform matching.

Non-goals: adding a short alias, changing default auto-selection rules, or introducing programmatic APIs for machine-driven selection.

Owner: engineering

Acceptance criteria:
- The CLI accepts `--choose-asset-file` and is documented in CLI options spec
- When provided in a TTY, the tool lists every asset file for the chosen release and prompts the user to enter a selection; the chosen asset is downloaded and processing continues as usual
- While `--choose-asset-file` is active, OS/arch inferred filters and stop-words are not applied to the list of candidates
- In non-TTY environments the tool fails with a clear error explaining the flag requires interactive TTY and suggesting removal to use normal filtering
