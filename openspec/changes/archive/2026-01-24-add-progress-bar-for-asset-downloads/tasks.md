# Tasks for Adding Progress Bar

1. Add `tqdm` to the dependencies in `pyproject.toml`.
2. Update the `download_asset` function in `src/gdl/github_downloader.py` to display a progress bar using `tqdm` during download.
3. Verify the progress bar displays correctly by running the tool with a test download.
4. Run `uv run ruff check --fix` and `uv run ruff format` to ensure code quality.
5. Run `uv run ty check` to verify type safety.
6. Run tests to ensure no regressions.