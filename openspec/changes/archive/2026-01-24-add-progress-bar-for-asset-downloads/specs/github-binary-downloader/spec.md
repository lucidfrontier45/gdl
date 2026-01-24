## ADDED Requirements

### Requirement: Progress Bar During Download
The tool SHALL display a progress bar using `tqdm` during asset file downloads to provide user feedback.

#### Scenario: Download with progress bar
Given an asset to download
When the download starts
Then a progress bar is displayed showing download progress in bytes
And the progress bar updates in real-time until download completes