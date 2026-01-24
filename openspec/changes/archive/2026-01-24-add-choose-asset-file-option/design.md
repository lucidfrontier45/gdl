Design notes for `--choose-asset-file`

Overview
--------
The feature is intentionally minimal: it bypasses pre-selection filters (OS, arch, stop-words) and asks the user to pick one of the release assets. It reuses the interactive prompting pattern used by `--choose-bin-file` to remain consistent.

Where to hook
--------------
- CLI parsing: add the boolean flag in the existing CLI options parsing module.
- Selection phase: during the asset candidate discovery step, if `--choose-asset-file` is set, present all assets instead of applying filters. This should happen before constructing candidate binary lists or applying stop-words.

TTY behaviour
-----------
- If stdout/stderr are connected to a TTY, present a numbered list sorted by filename (stable and predictable) and accept numeric selection.
- If not a TTY, reject with an error: "--choose-asset-file requires an interactive terminal; remove the flag to let the tool auto-select assets."

Interaction specifics
--------------------
- Display format: numbered, filename and size when available. Example:
  1) foo-1.0.0-linux-amd64.tar.gz (12345 bytes)
  2) foo-1.0.0-windows-x64.zip (23456 bytes)
- Accept only valid integers within range; on invalid input re-prompt (3 attempts) then fail with an explanatory message to keep implementation simple.

Edge cases
----------
- No assets: fall back to the existing error for missing assets.
- Single asset: still present it and allow confirmation or accept it automatically (implementation chooses to present it; simpler UX).
- Concurrent flags: If `--choose-asset-file` and `--list` are both present, prefer `--list` semantics and return early (documented). If `--choose-bin-file` is also present, allow both: user first chooses asset, then if the asset is an archive `--choose-bin-file` can be used later for selecting the extracted binary.

Why not filter in prompt
------------------------
Requirement explicitly asks for listing all assets without filtering by stop-words, OS, arch. We keep downstream processing unchanged so the selected asset still flows through existing validation and decompression.

Testing
-------
- Add unit tests mocking asset list, TTY and non-TTY environments. Test that stop-words/filters are ignored and selection returns expected asset index.
