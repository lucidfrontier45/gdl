## 1. Discovery and Analysis

- [x] 1.1 Locate existing asset matching/filename parsing logic
- [x] 1.2 Identify current pattern definitions and matching approach
- [x] 1.3 Review existing tests for asset matching

## 2. Pattern Implementation

- [x] 2.1 Add Windows OS regex patterns (windows, win, win32, win64) with word boundaries
- [x] 2.2 Add architecture mapping patterns (win32, win64) to x86_64
- [x] 2.3 Compile patterns with re.IGNORECASE flag for case-insensitive matching

## 3. Integration

- [x] 3.1 Register new Windows OS patterns in pattern matching system
- [x] 3.2 Register architecture mapping for win32/win64 to x86_64
- [x] 3.3 Ensure patterns are applied in correct order (specific before generic)

## 4. Testing

- [x] 4.1 Add test for "windows" pattern matching (lowercase)
- [x] 4.2 Add test for "Windows" pattern matching (mixed case)
- [x] 4.3 Add test for "WINDOWS" pattern matching (uppercase)
- [x] 4.4 Add test for "win" pattern matching
- [x] 4.5 Add test for "win32" pattern matching (OS=windows, Arch=x86_64)
- [x] 4.6 Add test for "win64" pattern matching (OS=windows, Arch=x86_64)
- [x] 4.7 Add test for false positive prevention (e.g., "twin" should not match)
- [x] 4.8 Run all existing asset matching tests to ensure no regressions

## 5. Verification

- [x] 5.1 Run `uv run ruff check --fix` to lint code
- [x] 5.2 Run `uv run ruff format` to format code
- [x] 5.3 Run `uv run ty check` for type checking
- [x] 5.4 Run `uv run pytest` to verify all tests pass
