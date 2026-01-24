# Add Progress Bar for Asset Downloads

## Summary
Enhance the user experience by displaying a progress bar during asset file downloads using the `tqdm` library. This provides visual feedback on download progress, improving usability for larger files.

## Motivation
Currently, downloads happen silently without any indication of progress, which can be frustrating for users downloading large assets. Adding a progress bar will make the tool more user-friendly and provide transparency into the download process.

## Scope
- Modify the `download_asset` function in `src/gdl/github_downloader.py` to integrate `tqdm` for progress tracking.
- Add `tqdm` as a dependency in `pyproject.toml`.
- Ensure progress bar displays bytes downloaded with appropriate scaling.

## Impact
- Minimal code changes focused on the download logic.
- Adds a new dependency (`tqdm`), which is lightweight and widely used.
- No breaking changes to existing functionality or CLI interface.