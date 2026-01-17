---
name: deploy-check
description: Pre-deployment checklist verification
license: MIT
compatibility: opencode
metadata:
  audience: developers
  workflow: deployment
---

## What I Do
Verify all pre-deployment requirements are met before releasing to production.

## Deployment Checklist

### Code Quality
- [ ] All tests pass
- [ ] No console.log statements
- [ ] No debugger statements
- [ ] No TODO comments for critical items
- [ ] Code coverage meets threshold (80%+)

### Configuration
- [ ] Environment variables documented
- [ ] .env.example up to date
- [ ] Configuration validated for production
- [ ] API keys not hardcoded

### Database
- [ ] Migrations tested
- [ ] Rollback plan exists
- [ ] Database backups current
- [ ] No destructive operations without confirmation

### Documentation
- [ ] CHANGELOG updated
- [ ] API documentation current
- [ ] README reflects new features
- [ ] Deployment instructions updated

### Security
- [ ] No exposed secrets
- [ ] Dependencies updated
- [ ] Security headers configured
- [ ] Authentication tested

### Performance
- [ ] Load testing completed
- [ ] Database queries optimized
- [ ] Caching configured
- [ ] CDN assets optimized

## Output Format

```markdown
## Pre-Deployment Check Results

### ✅ Passed (X/Y)
- Tests passing
- No console statements
- Environment variables documented

### ❌ Failed (X/Y)
- [CRITICAL] Console.log found in src/api/handler.ts:45
  Fix: Remove or use proper logging library

- [WARNING] Missing CHANGELOG entry
  Fix: Document new authentication feature

### ⚠️ Manual Review Required
- Database migration needs review
- Load testing results pending
```

## Usage

Run this check before:
1. Merging to main
2. Deploying to staging
3. Deploying to production

When all items pass, proceed with deployment.
