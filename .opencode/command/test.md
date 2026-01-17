---
description: Run tests with coverage and analyze results
agent: build
subtask: false
---

Run the test suite and analyze results:

!`npm test -- --coverage 2>&1 || true`

Based on the test results above:

## If Tests Pass ✅
1. **Summarize coverage:**
   - Statement coverage percentage
   - Branch coverage percentage
   - Function coverage percentage
   - Line coverage percentage

2. **Identify gaps:**
   - Files with low coverage (< 80%)
   - Uncovered code paths
   - Missing edge case tests

3. **Suggest improvements:**
   - Priority areas for additional tests
   - Specific test cases to add
   - Integration test opportunities

## If Tests Fail ❌
1. **Identify failing tests:**
   - List each failing test
   - Show error messages
   - Identify patterns in failures

2. **Analyze failure reasons:**
   - Logic errors
   - Incorrect assumptions
   - Environment issues
   - Race conditions

3. **Suggest fixes:**
   - Provide code examples for fixes
   - Explain why tests are failing
   - Recommend debugging approach

## Format Output As:

```markdown
## Test Results

### Status: [PASS/FAIL]

### Coverage Summary
- Statements: XX% (threshold: 80%)
- Branches: XX% (threshold: 75%)
- Functions: XX% (threshold: 90%)
- Lines: XX% (threshold: 80%)

### Failing Tests (if any)
1. **Test Name**
   - File: path/to/test.ts
   - Error: Error message
   - Fix: Suggested solution

### Low Coverage Areas
1. **File Name** (XX% coverage)
   - Uncovered: Lines X-Y
   - Recommendation: Add tests for [specific functionality]

### Recommended Tests
1. **Test Case:** [Description]
   - File: path/to/code.ts
   - Reason: [Why this test is needed]
   - Example:
     ```typescript
     it('should [behavior]', () => {
       // test code
     });
     ```
```
