# Remove "win" from Windows OS Synonyms

## Summary
Remove "win" as a synonym for the "windows" OS in the GitHub binary downloader tool. The tool will no longer recognize "win" as a valid OS identifier, only accepting "windows" and "win32".

## Motivation
To standardize OS naming and reduce ambiguity, "win" is an overly abbreviated synonym that may cause confusion. Retaining "win32" as a synonym maintains compatibility with common naming conventions while removing the more ambiguous "win".

## Impact
- Assets named with "win" in the filename will no longer be matched when specifying "windows" as the OS
- Users will need to use "windows" or "win32" instead of "win"
- Documentation and README will be updated to reflect the change</content>
<parameter name="filePath">D:\workspace\gdl\openspec\changes\remove-win-synonym\proposal.md