# OpenCode Skill Conventions

> Standards and best practices for creating high-quality OpenCode skills

---

## 📁 File Structure

```
skill-name/
└── SKILL.md          # Required: Must be uppercase, must exist
```

**Rules:**
- Directory name must match `name` field in frontmatter
- Only one file per skill: `SKILL.md`
- Place skills in appropriate location:
  - **Global:** `~/.config/opencode/skill/<name>/SKILL.md`
  - **Project:** `.opencode/skill/<name>/SKILL.md`

---

## 📝 Naming Conventions

### Skill Name Format

```
^[a-z0-9]+(-[a-z0-9]+)*$
```

**Valid:**
- `security-audit`
- `deploy-check`
- `analyze-k6-results`
- `performance-test`

**Invalid:**
- `Security-Audit` (uppercase)
- `deploy_check` (underscore)
- `security--audit` (double hyphen)
- `-deploy-check` (starts with hyphen)
- `deploy-check-` (ends with hyphen)

### Naming Guidelines

1. **Use verbs for actions:** `analyze`, `check`, `validate`, `generate`
2. **Be specific:** `security-audit` not `audit`
3. **Use domain terminology:** `k6` instead of `load-test` if k6-specific
4. **Keep it concise:** 2-4 words maximum

---

## 📋 Frontmatter Requirements

### Required Fields

```yaml
---
name: skill-name                    # Must match directory name
description: Clear description      # 1-1024 characters, specific and actionable
---
```

### Recommended Fields

```yaml
---
name: skill-name
description: What this skill does and when to use it
license: MIT                        # Or your preferred license
compatibility: opencode             # Target platform
metadata:
  audience: developers              # Who should use this skill
  workflow: category-name           # Workflow category (see below)
---
```

### Workflow Categories

Use standardized workflow tags for consistency:

| Category | Use Case | Examples |
|----------|----------|----------|
| `security` | Security checks and audits | `security-audit` |
| `deployment` | Pre/post deployment tasks | `deploy-check` |
| `code-review` | Code quality and standards | `team-review` |
| `performance-testing` | Load testing and analysis | `performance-test`, `analyze-k6-results` |
| `git-ops` | Git workflow assistance | (avoid - prefer native features) |
| `documentation` | Documentation generation | `docs-check` |
| `testing` | Test-related tasks | `test-coverage` |

---

## 📄 Content Structure

### Standard Sections

Every skill should include these sections in order:

```markdown
## What I Do

Clear, concise description of the skill's purpose. One paragraph maximum.

## Input Requirements

### Required Inputs
- List required inputs
- Include format examples

### Optional Inputs
- List optional inputs
- Include default values

## Processing / How It Works

Explain the logic, steps, or methodology.

## Output Format

Define what the skill produces:
- Format (markdown, JSON, code)
- Structure
- Example output

## Examples

### Example 1: [Scenario Name]
[Concrete example with input and output]

### Example 2: [Scenario Name]
[Another concrete example]

## When to Use

### ✅ Use This Skill When:
- Specific scenario 1
- Specific scenario 2

### ❌ Don't Use When:
- Alternative approach 1
- Alternative approach 2

## Integration with Other Skills

If this skill works with others:
1. **skill-name-1** → Does X
2. **skill-name-2** (this skill) → Does Y
3. **skill-name-3** → Does Z
```

### Optional Sections

Add these as needed:

```markdown
## Severity Levels

For audit/review skills:

### 🔴 Critical
Description of critical issues

### 🟠 High
Description of high issues

### 🟡 Medium
Description of medium issues

### 🟢 Low
Description of low issues

## Cost Analysis

For skills that involve resource planning:

### Current Costs
Breakdown of current costs

### Projected Costs
Breakdown at different scales

## Troubleshooting

Common issues and solutions

## Best Practices

Tips for using this skill effectively
```

---

## ✅ Quality Checklist

Before submitting a skill, verify:

### Metadata
- [ ] `name` field matches directory name
- [ ] `description` is 1-1024 characters
- [ ] `description` is specific (no vague terms like "stuff", "things", "various")
- [ ] `license` is specified (recommended: MIT)
- [ ] `compatibility` is specified (recommended: opencode)
- [ ] `metadata.workflow` is defined with standard category

### Content
- [ ] Has "What I Do" section
- [ ] Has "Input Requirements" section
- [ ] Has "Output Format" section
- [ ] Has at least 2 concrete examples
- [ ] Has "When to Use" section
- [ ] Instructions use actionable verbs (check, verify, create, implement)
- [ ] Contains at least 2 code blocks
- [ ] Total length is 100+ lines for complex skills

### Necessity
- [ ] Does NOT duplicate native opencode features
- [ ] Does NOT duplicate other skills
- [ ] Provides unique value
- [ ] Has clear use cases (not too narrow)

### Style
- [ ] Uses consistent formatting
- [ ] Uses emojis for visual indicators (✅ ❌ 🔴 🟠 🟡 🟢 ⚠️)
- [ ] Code blocks specify language (```javascript, ```yaml, etc.)
- [ ] Tables are formatted consistently

---

## 🚫 Anti-Patterns

### Don't Do This

❌ **Duplicate native features:**
```yaml
# Bad: Duplicates git push
name: push
description: Push to remote
```

❌ **Vague descriptions:**
```yaml
# Bad: Too vague
name: helper
description: Does various stuff for the project
```

❌ **Too narrow scope:**
```yaml
# Bad: Only useful for one specific edge case
name: fix-specific-bug-1234
description: Fixes the bug from ticket 1234
```

❌ **Missing structure:**
```markdown
# Bad: No sections, just free text
This skill does things. Use it when you need to do stuff.
```

❌ **No examples:**
```markdown
# Bad: No concrete examples
## Examples
See usage above.
```

---

## 📊 Scoring Rubric

Use the skill auditor to validate quality:

```bash
python skill_auditor.py --skill your-skill-name
```

### Score Breakdown

| Category | Max Points | Criteria |
|----------|------------|----------|
| **Metadata** | 35 | Required fields, valid name, description quality |
| **Quality** | 35 | Examples, output format, actionable instructions |
| **Necessity** | 30 | Unique value, no duplication, appropriate scope |
| **Total** | **100** | **Grade: A (80+), B (70-79), C (60-69), D (50-59), F (<50)** |

### Target Scores

- **New skills:** Minimum 70 (Grade B)
- **Complex skills:** Target 85+ (Grade A)
- **Simple skills:** Minimum 60 (Grade C)

---

## 🔄 Maintenance

### Regular Reviews

Run the auditor monthly:

```bash
python skill_auditor.py --format markdown -o monthly-audit.md
```

### Check for:
1. **Rot** - Skills that are no longer used
2. **Duplication** - New skills that overlap with existing
3. **Gaps** - Missing skill coverage
4. **Quality** - Skills that have degraded

### Deprecation Process

If a skill needs to be removed:

1. Mark as deprecated in SKILL.md:
   ```markdown
   > ⚠️ **DEPRECATED**: This skill is deprecated. Use `new-skill-name` instead.
   ```
2. Wait 30 days
3. Remove the skill directory
4. Update any documentation

---

## 📝 Example: Perfect Skill

See these skills as examples of best practices:

- **analyze-k6-results** - Comprehensive analysis skill (Score: 100)
- **architecture-analyzer** - System analysis (Score: 100)
- **performance-test** - Script generation (Score: 92)

---

## 🔧 Tools

### Skill Auditor

```bash
# Audit all skills
python skill_auditor.py

# Audit specific skill
python skill_auditor.py --skill skill-name

# Generate report
python skill_auditor.py --format markdown -o report.md
```

### Validation

```bash
# Check YAML frontmatter
python -c "import yaml; yaml.safe_load(open('SKILL.md').read().split('---')[1])"

# Check name format
echo "skill-name" | grep -P '^[a-z0-9]+(-[a-z0-9]+)*$'
```

---

## 📚 Resources

- [OpenCode Skills Documentation](https://opencode.ai/docs/skills/)
- [OpenCode CLI Reference](https://opencode.ai/docs/cli/)
- [SKILL_CONVENTIONS.md](SKILL_CONVENTIONS.md) (this file)
- [SKILL_TEMPLATE.md](SKILL_TEMPLATE.md) - Template for new skills

---

**Last Updated:** 2026-02-07  
**Version:** 1.0  
**Maintainer:** OpenCode Personal Skills
