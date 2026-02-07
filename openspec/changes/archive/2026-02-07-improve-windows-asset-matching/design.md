## Context

Current asset matching logic has incomplete Windows platform detection. Asset filenames may contain various Windows indicators (windows, win, win32, win64) but are not consistently matched to OS=windows. Additionally, the system should map win32/win64 variants to x86_64 architecture.

This is an enhancement to existing asset matching logic with no breaking changes. The change is localized to filename pattern matching.

## Goals / Non-Goals

**Goals:**
- Enhance Windows OS detection to recognize all common Windows indicators
- Map win32/win64 to x86_64 architecture
- Ensure case-insensitive pattern matching

**Non-Goals:**
- Modifying existing asset matching for other platforms
- Changing the underlying asset storage or retrieval mechanisms
- UI/UX changes to asset display or selection

## Decisions

**Pattern matching approach:**
- Use regex patterns for flexible substring matching
- Compile patterns at module load time for performance
- Apply Windows patterns before generic patterns to ensure specificity

**Pattern definitions:**
- OS patterns: `r'\bwindows\b'`, `r'\bwin\b'`, `r'\bwin32\b'`, `r'\bwin64\b'` (case-insensitive)
- Architecture patterns: `r'\bwin32\b'`, `r'\bwin64\b'` (case-insensitive) → x86_64
- Word boundaries (`\b`) prevent false positives (e.g., "twin" should not match "win")

**Integration point:**
- Extend existing asset matching function/module
- Add new Windows-specific patterns to pattern registry
- No changes to matching algorithm or data flow

## Risks / Trade-offs

**Risk**: Pattern matching may produce false positives
- **Mitigation**: Use word boundaries in regex patterns; test with common filename patterns

**Risk**: Case-insensitive matching may have performance overhead
- **Mitigation**: Compile regex patterns once at module load; minimal performance impact

**Trade-off**: Specificity vs. flexibility
- Word boundaries reduce false matches but may miss filenames without spaces/delimiters
- Acceptable trade-off given typical asset naming conventions (e.g., "app-win64.exe", "lib-windows.so")
