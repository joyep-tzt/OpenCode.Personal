---
name: {{skill-name}}
description: {{Clear, specific description of what this skill does (1-1024 characters)}}
license: MIT
compatibility: opencode
metadata:
  audience: {{developers|devops|architects|qa|all}}
  workflow: {{security|deployment|code-review|performance-testing|git-ops|documentation|testing}}
---

## What I Do

{{Write a clear, concise description of the skill's purpose. One paragraph maximum. Explain what problem it solves and why it's useful.}}

Example:
> Analyze k6 performance test results, extrapolate QA findings to production capacity, identify bottlenecks, and provide cost-performance recommendations with reality checks.

---

## Input Requirements

### Required Inputs

- **{{Input Name}}**: {{Description and format}}
  - Example: `{{example value}}`
  - Format: {{file format, string, JSON, etc.}}

### Optional Inputs

- **{{Input Name}}**: {{Description}}
  - Default: `{{default value}}`
  - Example: `{{example value}}`

---

## Processing / How It Works

{{Explain the methodology, logic, or steps the skill takes. Be specific about the process.}}

### Step 1: {{First Step}}
{{Description of what happens}}

### Step 2: {{Second Step}}
{{Description of what happens}}

### Step 3: {{Third Step}}
{{Description of what happens}}

---

## Output Format

{{Define the output format clearly. Include structure, format type, and example.}}

### Markdown Report

```markdown
## {{Report Title}}

### Summary
{{Summary structure}}

### Details
{{Details structure}}

### Recommendations
{{Recommendations structure}}
```

### JSON Data (Optional)

```json
{
  "field1": "description",
  "field2": "description",
  "metrics": {
    "key": "value"
  }
}
```

---

## Examples

### Example 1: {{Scenario Name}}

**Input:**
```
{{Example input data or description}}
```

**Processing:**
{{What the skill does with this input}}

**Output:**
```markdown
{{Example output}}
```

### Example 2: {{Scenario Name}}

**Input:**
```
{{Example input data or description}}
```

**Processing:**
{{What the skill does with this input}}

**Output:**
```markdown
{{Example output}}
```

---

## When to Use

### ✅ Use This Skill When:

- {{Specific scenario 1}}
- {{Specific scenario 2}}
- {{Specific scenario 3}}

### ❌ Don't Use When:

- {{Alternative approach 1}}
- {{Alternative approach 2}}
- {{When native opencode features are sufficient}}

---

## Integration with Other Skills

{{If this skill works with others, document the workflow:}}

1. **{{skill-name-1}}** → {{What it does}}
2. **{{skill-name-2}}** (this skill) → {{What it does}}
3. **{{skill-name-3}}** → {{What it does}}

---

## Severity Levels (For Audit/Review Skills)

{{If this is an audit or review skill, define severity levels:}}

### 🔴 Critical

{{Description of what constitutes a critical issue}}

**Examples:**
- {{Example 1}}
- {{Example 2}}

### 🟠 High

{{Description of what constitutes a high issue}}

**Examples:**
- {{Example 1}}
- {{Example 2}}

### 🟡 Medium

{{Description of what constitutes a medium issue}}

**Examples:**
- {{Example 1}}
- {{Example 2}}

### 🟢 Low

{{Description of what constitutes a low issue}}

**Examples:**
- {{Example 1}}
- {{Example 2}}

---

## Best Practices

### Input Quality

- ✅ {{Best practice 1}}
- ✅ {{Best practice 2}}
- ✅ {{Best practice 3}}

### Output Usage

- ✅ {{Best practice 1}}
- ✅ {{Best practice 2}}
- ✅ {{Best practice 3}}

### Common Mistakes to Avoid

- ❌ {{Mistake 1}}
- ❌ {{Mistake 2}}
- ❌ {{Mistake 3}}

---

## Troubleshooting

### Issue: {{Problem Description}}

**Symptoms:**
- {{Symptom 1}}
- {{Symptom 2}}

**Solution:**
{{Step-by-step solution}}

### Issue: {{Problem Description}}

**Symptoms:**
- {{Symptom 1}}
- {{Symptom 2}}

**Solution:**
{{Step-by-step solution}}

---

## Output Files (Optional)

{{If the skill generates files, list them:}}

Generated artifacts:
- `{{filename1}}` - {{Description}}
- `{{filename2}}` - {{Description}}
- `{{filename3}}` - {{Description}}

---

## Notes

{{Any additional notes, limitations, or future improvements:}}

- {{Note 1}}
- {{Note 2}}
- {{Note 3}}

---

## Changelog

### v1.0.0 (YYYY-MM-DD)

- Initial release
- {{Feature 1}}
- {{Feature 2}}

---

<!-- 
QUALITY CHECKLIST:
Before finalizing this skill, verify:

Metadata:
- [ ] name matches directory name
- [ ] description is 1-1024 characters
- [ ] description is specific (no vague terms)
- [ ] license is specified
- [ ] compatibility is specified
- [ ] metadata.workflow is defined

Content:
- [ ] Has "What I Do" section
- [ ] Has "Input Requirements" section
- [ ] Has "Output Format" section
- [ ] Has at least 2 concrete examples
- [ ] Has "When to Use" section
- [ ] Instructions use actionable verbs
- [ ] Contains at least 2 code blocks
- [ ] Total length is 100+ lines

Necessity:
- [ ] Does NOT duplicate native opencode features
- [ ] Does NOT duplicate other skills
- [ ] Provides unique value

Style:
- [ ] Uses consistent formatting
- [ ] Uses emojis for visual indicators
- [ ] Code blocks specify language
- [ ] Tables are formatted consistently

Run this to validate:
    python skill_auditor.py --skill {{skill-name}}

Target score: 80+ (Grade A)
-->
