# Automated Skill Validation

> Automated quality assurance for OpenCode skills using pre-commit hooks and CI/CD

---

## 📋 Overview

This repository uses automated validation to ensure all OpenCode skills meet quality standards before being committed. The validation system includes:

1. **Pre-commit Hooks** - Run locally before every commit
2. **CI/CD Pipeline** - Run on GitHub Actions for every PR and push
3. **Manual Validation** - Run on-demand for development

---

## 🚀 Quick Start

### Install Pre-commit Hooks

```bash
./scripts/install-hooks.sh
```

This installs a pre-commit hook that automatically validates skills before every commit.

### Test the Hook

```bash
# Test manually
bash .git/hooks/pre-commit

# Or make a test commit
git add .
git commit -m "test: validate skills"
```

---

## 🔧 What Gets Validated

### Quality Checks

✅ **Metadata Completeness**
- Name matches directory
- Description is 1-1024 characters
- Description is specific (no vague terms)
- License specified (recommended: MIT)
- Compatibility specified (recommended: opencode)
- Workflow category defined

✅ **Content Quality**
- Has "What I Do" section
- Has input requirements
- Has output format definition
- Has at least 2 concrete examples
- Has "When to Use" section
- Instructions use actionable verbs
- Contains at least 2 code blocks

✅ **Necessity Assessment**
- Does NOT duplicate native opencode features
- Does NOT duplicate other skills
- Provides unique value
- Appropriate scope (not too narrow)

### Scoring

| Category | Max Points | Criteria |
|----------|------------|----------|
| Metadata | 35 | Required fields, valid name, description |
| Quality | 35 | Examples, format, actionable instructions |
| Necessity | 30 | Unique value, no duplication |
| **Total** | **100** | **Grade: A (80+), B (70-79), C (60-69), D (50-59), F (<50)** |

### Validation Rules

🔴 **BLOCKS Commit:**
- Skills marked for DELETE verdict
- Skills scoring below 60/100
- Critical issues found

🟡 **Warns but Allows:**
- Skills scoring 60-79 (Grade C)
- Missing optional metadata
- Minor quality issues

🟢 **Passes:**
- Skills scoring 80+ (Grade A or B)
- No critical issues
- All required fields present

---

## 📝 Pre-commit Hook

### Location
```
.git/hooks/pre-commit
```

### Features
- Automatically runs on every commit
- Validates all skills
- Provides detailed output for modified skills
- Blocks commits that don't meet standards
- Shows summary statistics

### Usage

**Normal commit (hook runs automatically):**
```bash
git add .
git commit -m "feat: add new skill"
# Hook runs validation automatically
```

**Skip validation (not recommended):**
```bash
git commit --no-verify -m "emergency fix"
```

**Test hook manually:**
```bash
bash .git/hooks/pre-commit
```

### Output Example

```
🔍 Running OpenCode skill validation...

====================================================================================================
Skill                     Location   Score    Grade    Verdict      Priority  
====================================================================================================
architecture-analyzer     project    100      A        KEEP         Low       
deploy-check              global     98       A        KEEP         Low       
team-review               global     94       A        KEEP         Low       
performance-test          project    92       A        KEEP         Low       
security-audit            global     90       A        KEEP         Low       
analyze-k6-results        project    90       A        KEEP         Low       
====================================================================================================

Summary: 6 skills total
  ✅ KEEP: 6
  ⚠️  UPGRADE: 0
  ❌ DELETE: 0

✅ Pre-commit validation complete. Proceeding with commit...
```

---

## 🔄 CI/CD Pipeline

### GitHub Actions Workflow

**File:** `.github/workflows/skill-validation.yml`

### Triggers
- Push to main/master/dev branches (when skills change)
- Pull requests (when skills change)
- Manual dispatch

### Jobs

1. **Setup**
   - Install Python 3.10
   - Install dependencies (pyyaml)
   - Install jq

2. **Validation**
   - Run skill auditor
   - Check for DELETE verdicts
   - Check for low scores (< 60)
   - Check for critical issues

3. **Reporting**
   - Generate markdown report
   - Upload as artifact
   - Comment on PR with results

### Configuration

Environment variables:
```yaml
FAIL_ON_DELETE: true        # Fail build if skills marked for deletion
FAIL_ON_LOW_SCORE: true     # Fail build if skills score below minimum
MIN_SCORE: 60              # Minimum acceptable score
```

### CI Output Example

```
🔍 OpenCode Skill CI Validation
================================

Configuration:
  Fail on DELETE: true
  Fail on low score: true
  Minimum score: 60

📊 Summary
=========
Total skills:     6
Keep:             6
Upgrade:          0
Delete:           0
Critical issues:  0
Warnings:         0
Average score:    94.0/100

📈 Grade Distribution
====================
Grade A: 6
Grade B: 0
Grade C: 0
Grade D: 0
Grade F: 0

🏆 Top Skills
============
  100/100 - architecture-analyzer
  98/100 - deploy-check
  94/100 - team-review

✅ CI Validation Complete
```

---

## 🛠️ Manual Validation

### Run Full Audit

```bash
# Basic table output
python skill_auditor.py

# Detailed report with all issues
python skill_auditor.py --format detailed

# JSON output for automation
python skill_auditor.py --format json -o results.json

# Markdown report
python skill_auditor.py --format markdown -o report.md
```

### Validate Specific Skill

```bash
python skill_auditor.py --skill skill-name
```

### Filter by Location

```bash
# Only global skills
python skill_auditor.py --global-only

# Only project skills
python skill_auditor.py --project-only
```

### CI Script

```bash
# Run CI validation locally
./scripts/ci-validate.sh

# With custom configuration
FAIL_ON_DELETE=false MIN_SCORE=50 ./scripts/ci-validate.sh
```

---

## 📂 File Structure

```
OpenCode.Personal/
├── scripts/
│   ├── validate-skills.sh       # Pre-commit hook logic
│   ├── install-hooks.sh         # Hook installer
│   └── ci-validate.sh           # CI validation script
├── .github/
│   └── workflows/
│       └── skill-validation.yml # GitHub Actions workflow
├── skill_auditor.py             # Main audit tool
└── VALIDATION.md                # This file
```

---

## 🔍 Troubleshooting

### Hook Not Running

**Check if hook exists:**
```bash
ls -la .git/hooks/pre-commit
```

**Reinstall hooks:**
```bash
./scripts/install-hooks.sh
```

### Validation Fails But Should Pass

**Check skill score:**
```bash
python skill_auditor.py --skill problematic-skill
```

**Review issues:**
```bash
python skill_auditor.py --format detailed | grep -A5 "problematic-skill"
```

### CI/CD Failures

**Check workflow status:**
- Go to GitHub Actions tab
- Click on the failed workflow
- Review the logs

**Common issues:**
- Missing `skill_auditor.py`
- Python dependencies not installed
- jq not available

**Download artifact for details:**
- Go to workflow run
- Download "skill-validation-report" artifact

### Performance Issues

**Hook taking too long:**
- The hook validates all skills on every commit
- Consider using `--skill` flag for specific skill validation
- Or run validation only when skill files change

**CI taking too long:**
- Workflow only runs when skills change (path filter)
- If still slow, optimize the auditor script

---

## 🎯 Best Practices

### For Skill Authors

1. **Before Creating a Skill:**
   - Check [SKILL_REGISTRY.md](SKILL_REGISTRY.md) for existing skills
   - Review [SKILL_CONVENTIONS.md](SKILL_CONVENTIONS.md)
   - Use [SKILL_TEMPLATE.md](SKILL_TEMPLATE.md)

2. **Before Committing:**
   - Run `python skill_auditor.py --format detailed`
   - Fix all critical issues
   - Target score: 80+ (Grade A)

3. **During Development:**
   - Test the skill locally
   - Add comprehensive examples
   - Document when NOT to use it

### For Maintainers

1. **Reviewing PRs:**
   - Check CI validation results
   - Review skill quality in PR
   - Ensure no duplicate skills

2. **Regular Maintenance:**
   - Run monthly audits
   - Archive deprecated skills
   - Update conventions as needed

---

## 📊 Validation Metrics

Track these metrics over time:

- **Total Skills:** Number of skills in repository
- **Average Score:** Portfolio health indicator
- **Grade Distribution:** Quality breakdown
- **Critical Issues:** Urgent fixes needed
- **DELETE Verdicts:** Skills to remove

**Current Status:**
```
Skills: 6
Average Score: 94/100
Grade A: 6 (100%)
Critical Issues: 0
```

---

## 🔗 Related Documentation

- [SKILL_CONVENTIONS.md](SKILL_CONVENTIONS.md) - Standards and best practices
- [SKILL_REGISTRY.md](SKILL_REGISTRY.md) - Complete skill index
- [SKILL_TEMPLATE.md](SKILL_TEMPLATE.md) - Template for new skills
- [skill_auditor.py](skill_auditor.py) - Audit tool source code

---

## 📝 Changelog

### v1.0.0 (2026-02-08)

- Initial validation system
- Pre-commit hook
- GitHub Actions workflow
- CI validation script

---

**Maintained by:** OpenCode Personal Skills  
**Last Updated:** 2026-02-08
