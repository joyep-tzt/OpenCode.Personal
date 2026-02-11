---
name: testing-patterns-enhancer
description: Testing best practices and pattern detection for Playwright, Jest, Vitest, and React Testing Library
license: MIT
compatibility: opencode
metadata:
  audience: developers
  workflow: testing
---

## What I Do

Analyze testing setup and provide best practice recommendations for Playwright, Jest, Vitest, and React Testing Library. Identifies missing tests, anti-patterns, and optimization opportunities.

## Supported Frameworks

### Playwright
- E2E test structure
- Page Object Model patterns
- Selector strategies (data-testid preferred)
- Test isolation and setup
- Visual testing setup

### Jest/Vitest
- Unit test organization
- Mocking strategies
- Coverage thresholds
- Test naming conventions
- Async test patterns

### React Testing Library
- Component test patterns
- Query priority (getByRole > getByText)
- User event simulation
- Accessibility testing
- Async assertions

## Analysis Areas

### 1. Test Coverage Gaps
- Untested critical paths
- Missing error scenarios
- Edge cases not covered
- Integration test gaps

### 2. Test Quality
- Flaky test detection
- Slow test identification
- Test duplication
- Over-mocking issues

### 3. Best Practices
- AAA pattern (Arrange-Act-Assert)
- Descriptive test names
- Proper assertions
- Cleanup and teardown

### 4. CI/CD Integration
- Test parallelization
- Retry configuration
- Reporting setup
- Artifact collection

## Output

Enhances the core analysis report with:
- Testing-specific recommendations
- Missing test scenarios
- Refactoring suggestions
- Best practice violations

## Usage

Loaded conditionally when test configuration detected by orchestrator.
