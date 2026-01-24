Improve bin file selection

Purpose
-------
Make the logic that selects the final extracted binary more deterministic and user-friendly by:

- Choosing the final binary among extracted candidate files using the following priority:
  1. files with a `.exe` suffix
  2. files with a Unix execute permission set in the extracted metadata or filesystem
  3. the largest file (by byte size)
- Ensuring the final binary is executable on Unix-like platforms (Linux, macOS) by setting the POSIX execute permission bit.
- Adding a CLI option `--choose-bin-file` that, when provided, prompts the user to choose which extracted file should be treated as the final binary instead of automatically selecting the largest one.

Rationale
---------
When packages contain multiple files after extraction (for example several executables, helper binaries, or metadata files), current heuristics may pick a file that is not the intended runnable binary. Choosing the largest file is a pragmatic, low-friction default that works for the common case where the main executable is larger than helpers. However, some repositories ship multiple similar-sized binaries and users may want to pick explicitly; `--choose-bin-file` addresses that.

Scope
-----
- Change the selection behavior used after decompressing release assets (zip, tar.gz) and inspecting extracted file entries.
- Apply a POSIX `chmod +x` (or equivalent) when saving the final binary on Linux or macOS hosts.
- Add CLI plumbing and interactive prompt for `--choose-bin-file`.

Out of scope
------------
- Any changes to how assets are downloaded or filtered upstream (blacklist/additional heuristics) beyond selecting among already-extracted files.
- Windows-specific execute-permission handling (Windows uses file extensions and does not need chmod).
