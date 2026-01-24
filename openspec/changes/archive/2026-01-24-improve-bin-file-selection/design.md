Design notes: improve-bin-file-selection

Candidate enumeration
---------------------
After decompression, the current code enumerates entries in the extracted directory and filters by a small heuristics set (e.g., executable bit present in archive metadata, filename not matching blacklist, file size > 0). We will reuse that enumeration and treat all non-directory entries that are not filtered by blacklist as candidates.

Selection algorithm
-------------------
Default behavior (no user flag):
- From the candidate list choose the final file using the following prioritised rules applied in order:
  1. Prefer files whose filename ends with `.exe` (case-insensitive).
  2. If none, prefer files that have Unix execute permissions set in the extracted metadata or on the filesystem.
  3. If none match the above, choose the largest file by byte size. If multiple files share the largest size, pick the first encountered in sorted lexical order to keep determinism across runs.

Interactive behavior (`--choose-bin-file`):
- Present candidates in descending size order with index numbers, sizes, and relative paths. Prompt for a number. Accept Enter as selecting the default (index 1).
- If running in a non-interactive environment (no TTY), error with message: "--choose-bin-file requires a TTY; run without this flag to auto-select the largest file or run interactively." This avoids ambiguous behavior in scripts/CI.

POSIX permission handling
------------------------
After selecting the final file, if the host OS is posix-like (platform.system() in {"Linux","Darwin"}):
- Call os.chmod(path, current_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH) to ensure the owner/group/other execute bits are set.
- Skip on Windows.

Testing approach
----------------
- Unit tests for selection: create tempdirs with files of specific sizes; call the selection function and assert the chosen path.
- Tests for interactive prompt: monkeypatch stdin to simulate user entering a number, and simulate absence of TTY for error path.
- Permission tests: monkeypatch platform.system() and os.chmod to observe expected calls.

Backward compatibility and UX
----------------------------
- Default behavior remains automatic, but more deterministic.
- The new flag is additive and does not change existing flags/options.
