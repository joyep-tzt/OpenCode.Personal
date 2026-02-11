---
name: sdet-core-analyzer
description: Generic SDET analysis for any TypeScript project - works standalone without framework-specific skills
license: MIT
compatibility: opencode
metadata:
  audience: developers
  workflow: testing
---

## What I Do

Provide comprehensive SDET analysis that works with ANY TypeScript/JavaScript project. This skill is framework-agnostic and provides foundational testing assessment.

## Analysis Areas

### 1. Project Structure
- Source code organization
- Test file locations and naming
- Configuration completeness
- Directory structure best practices

### 2. TypeScript Configuration
- Strict mode enabled
- Target ES version appropriate
- Path aliases configured
- Type definitions present

### 3. Testing Infrastructure
- Test framework detected (Jest, Vitest, Playwright)
- Test scripts in package.json
- Coverage configuration
- Test utilities and helpers

### 4. Common Issues
- Missing .env.example
- No error boundaries
- Missing type definitions
- Unused dependencies

### 5. Security Basics
- Environment variables exposed in code
- Hardcoded secrets
- Missing input validation
- Unsafe dependencies

## Output Format

Generates sdet-analysis-report.md with:
- Executive summary
- Detected issues by severity
- Testing gaps identified
- Actionable recommendations
- Implementation guidance

## Usage

This skill is always loaded by the orchestrator as the foundation. Other skills enhance its findings.

## When Framework Skills Unavailable

This skill provides complete analysis even without specialist skills. It uses:
- Generic TypeScript patterns
- Universal testing principles
- Common SDET heuristics
- File system analysis
