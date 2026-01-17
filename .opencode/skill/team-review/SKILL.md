---
name: team-review
description: Review code for team standards and best practices
license: MIT
compatibility: opencode
metadata:
  audience: developers
  workflow: code-review
---

## What I Do
Review code against team-specific standards and best practices.

## Review Criteria

### Code Quality
- Functions are under 50 lines
- No magic numbers (use named constants)
- Descriptive variable names (no single letters except loop counters)
- Proper error handling with try/catch

### TypeScript (if applicable)
- All functions have return type annotations
- No `any` types (use `unknown` or specific types)
- Async functions use async/await (not `.then()`)
- Interfaces for complex objects

### Testing
- New functions have corresponding tests
- Edge cases are covered
- Error paths are tested
- Test descriptions are clear

### Documentation
- Complex logic has inline comments
- Public APIs have JSDoc comments
- README updated if adding features
- CHANGELOG updated for user-facing changes

## Output Format

For each issue found:
- **[SEVERITY]** Category: Description
- **File:** `path/to/file.ts:line`
- **Fix:** Specific recommendation

### Severity Levels
- **Critical:** Must fix before merge
- **Warning:** Should fix, but can merge
- **Info:** Nice to have improvement

## Examples

**Critical:**
```
[CRITICAL] Security: Hardcoded API key
- File: src/api/client.ts:12
- Fix: Move to environment variable: process.env.API_KEY
```

**Warning:**
```
[WARNING] Code Quality: Function too long (78 lines)
- File: src/utils/parser.ts:45
- Fix: Split into smaller functions (parseHeader, parseBody, parseFooter)
```

**Info:**
```
[INFO] Documentation: Missing JSDoc comment
- File: src/helpers/format.ts:23
- Fix: Add JSDoc describing parameters and return value
```
