# OpenCode Skill Audit Report

Generated: 2026-02-07 18:04:10

## Executive Summary

**Total Skills Audited:** 13

| Verdict | Count | Percentage |
|---------|-------|------------|
| KEEP | 9 | 69.2% |
| UPGRADE | 0 | 0.0% |
| DELETE | 4 | 30.8% |

**Critical Issues:** 4

---

## Detailed Skill Analysis

### branch

**Location:** `/home/userjyep/.config/opencode/skill/branch/SKILL.md`

**Type:** global

**Score:** 30/100 (Grade: F)

**Verdict:** `DELETE` | **Priority:** Critical

**Score Breakdown:**
- Metadata: 25/35
- Quality: 0/35
- Necessity: 5/30

**Issues:**

🔵 **[INFO]** metadata
   - **Issue:** Missing optional field: license
   - **Recommendation:** Consider adding 'license: MIT'

🔵 **[INFO]** metadata
   - **Issue:** Missing optional field: compatibility
   - **Recommendation:** Consider adding 'compatibility: opencode'

🟡 **[WARNING]** metadata
   - **Issue:** Missing metadata.workflow field
   - **Recommendation:** Add workflow categorization (e.g., 'git-ops', 'security', 'deployment')

🟡 **[WARNING]** quality
   - **Issue:** No examples section found
   - **Recommendation:** Add concrete examples of skill usage

🟡 **[WARNING]** quality
   - **Issue:** No output format defined
   - **Recommendation:** Add '## Output Format' section

🟡 **[WARNING]** quality
   - **Issue:** Instructions lack actionable verbs
   - **Recommendation:** Use verbs like 'check', 'verify', 'create', 'implement'

🔵 **[INFO]** quality
   - **Issue:** No 'when to use' section
   - **Recommendation:** Add guidance on appropriate usage contexts

🟡 **[WARNING]** quality
   - **Issue:** No code blocks found
   - **Recommendation:** Add code examples or templates

🔴 **[CRITICAL]** necessity
   - **Issue:** Likely duplicates native tui_slash command: /new
   - **Recommendation:** Consider deleting - functionality is built into opencode

🟡 **[WARNING]** necessity
   - **Issue:** Description is too brief (< 30 chars)
   - **Recommendation:** Add more detail about what the skill does

**Content Analysis:**
- Lines: 2
- Has examples: ❌
- Has output format: ❌
- Has actionable instructions: ❌
- Code blocks: 0

---

### push

**Location:** `/home/userjyep/.config/opencode/skill/push/SKILL.md`

**Type:** global

**Score:** 30/100 (Grade: F)

**Verdict:** `DELETE` | **Priority:** Critical

**Score Breakdown:**
- Metadata: 25/35
- Quality: 0/35
- Necessity: 5/30

**Issues:**

🔵 **[INFO]** metadata
   - **Issue:** Missing optional field: license
   - **Recommendation:** Consider adding 'license: MIT'

🔵 **[INFO]** metadata
   - **Issue:** Missing optional field: compatibility
   - **Recommendation:** Consider adding 'compatibility: opencode'

🟡 **[WARNING]** metadata
   - **Issue:** Missing metadata.workflow field
   - **Recommendation:** Add workflow categorization (e.g., 'git-ops', 'security', 'deployment')

🟡 **[WARNING]** quality
   - **Issue:** No examples section found
   - **Recommendation:** Add concrete examples of skill usage

🟡 **[WARNING]** quality
   - **Issue:** No output format defined
   - **Recommendation:** Add '## Output Format' section

🟡 **[WARNING]** quality
   - **Issue:** Instructions lack actionable verbs
   - **Recommendation:** Use verbs like 'check', 'verify', 'create', 'implement'

🔵 **[INFO]** quality
   - **Issue:** No 'when to use' section
   - **Recommendation:** Add guidance on appropriate usage contexts

🟡 **[WARNING]** quality
   - **Issue:** No code blocks found
   - **Recommendation:** Add code examples or templates

🔴 **[CRITICAL]** necessity
   - **Issue:** Duplicates native git_workflows command: push
   - **Recommendation:** Consider deleting - functionality is built into opencode

🟡 **[WARNING]** necessity
   - **Issue:** Description is too brief (< 30 chars)
   - **Recommendation:** Add more detail about what the skill does

**Content Analysis:**
- Lines: 1
- Has examples: ❌
- Has output format: ❌
- Has actionable instructions: ❌
- Code blocks: 0

---

### create-pr

**Location:** `/home/userjyep/.config/opencode/skill/create-pr/SKILL.md`

**Type:** global

**Score:** 38/100 (Grade: F)

**Verdict:** `DELETE` | **Priority:** Critical

**Score Breakdown:**
- Metadata: 25/35
- Quality: 8/35
- Necessity: 5/30

**Issues:**

🔵 **[INFO]** metadata
   - **Issue:** Missing optional field: license
   - **Recommendation:** Consider adding 'license: MIT'

🔵 **[INFO]** metadata
   - **Issue:** Missing optional field: compatibility
   - **Recommendation:** Consider adding 'compatibility: opencode'

🟡 **[WARNING]** metadata
   - **Issue:** Missing metadata.workflow field
   - **Recommendation:** Add workflow categorization (e.g., 'git-ops', 'security', 'deployment')

🟡 **[WARNING]** quality
   - **Issue:** No examples section found
   - **Recommendation:** Add concrete examples of skill usage

🟡 **[WARNING]** quality
   - **Issue:** No output format defined
   - **Recommendation:** Add '## Output Format' section

🔵 **[INFO]** quality
   - **Issue:** No 'when to use' section
   - **Recommendation:** Add guidance on appropriate usage contexts

🟡 **[WARNING]** quality
   - **Issue:** No code blocks found
   - **Recommendation:** Add code examples or templates

🔴 **[CRITICAL]** necessity
   - **Issue:** Duplicates native git_workflows command: create-pr
   - **Recommendation:** Consider deleting - functionality is built into opencode

🟡 **[WARNING]** necessity
   - **Issue:** Description is too brief (< 30 chars)
   - **Recommendation:** Add more detail about what the skill does

**Content Analysis:**
- Lines: 4
- Has examples: ❌
- Has output format: ❌
- Has actionable instructions: ✅
- Code blocks: 0

---

### commit

**Location:** `/home/userjyep/.config/opencode/skill/commit/SKILL.md`

**Type:** global

**Score:** 43/100 (Grade: F)

**Verdict:** `DELETE` | **Priority:** Critical

**Score Breakdown:**
- Metadata: 25/35
- Quality: 8/35
- Necessity: 10/30

**Issues:**

🔵 **[INFO]** metadata
   - **Issue:** Missing optional field: license
   - **Recommendation:** Consider adding 'license: MIT'

🔵 **[INFO]** metadata
   - **Issue:** Missing optional field: compatibility
   - **Recommendation:** Consider adding 'compatibility: opencode'

🟡 **[WARNING]** metadata
   - **Issue:** Missing metadata.workflow field
   - **Recommendation:** Add workflow categorization (e.g., 'git-ops', 'security', 'deployment')

🟡 **[WARNING]** quality
   - **Issue:** No examples section found
   - **Recommendation:** Add concrete examples of skill usage

🟡 **[WARNING]** quality
   - **Issue:** No output format defined
   - **Recommendation:** Add '## Output Format' section

🔵 **[INFO]** quality
   - **Issue:** No 'when to use' section
   - **Recommendation:** Add guidance on appropriate usage contexts

🟡 **[WARNING]** quality
   - **Issue:** No code blocks found
   - **Recommendation:** Add code examples or templates

🔴 **[CRITICAL]** necessity
   - **Issue:** Duplicates native git_workflows command: commit
   - **Recommendation:** Consider deleting - functionality is built into opencode

**Content Analysis:**
- Lines: 8
- Has examples: ❌
- Has output format: ❌
- Has actionable instructions: ✅
- Code blocks: 0

---

### security-audit

**Location:** `/home/userjyep/.config/opencode/skill/security-audit/SKILL.md`

**Type:** global

**Score:** 90/100 (Grade: A)

**Verdict:** `KEEP` | **Priority:** Low

**Score Breakdown:**
- Metadata: 35/35
- Quality: 25/35
- Necessity: 30/30

**Issues:**

🟡 **[WARNING]** quality
   - **Issue:** No examples section found
   - **Recommendation:** Add concrete examples of skill usage

**Content Analysis:**
- Lines: 137
- Has examples: ❌
- Has output format: ✅
- Has actionable instructions: ✅
- Code blocks: 3

---

### security-audit

**Location:** `.opencode/skill/security-audit/SKILL.md`

**Type:** project

**Score:** 90/100 (Grade: A)

**Verdict:** `KEEP` | **Priority:** Low

**Score Breakdown:**
- Metadata: 35/35
- Quality: 25/35
- Necessity: 30/30

**Issues:**

🟡 **[WARNING]** quality
   - **Issue:** No examples section found
   - **Recommendation:** Add concrete examples of skill usage

**Content Analysis:**
- Lines: 137
- Has examples: ❌
- Has output format: ✅
- Has actionable instructions: ✅
- Code blocks: 3

---

### analyze-k6-results

**Location:** `.opencode/skill/analyze-k6-results/SKILL.md`

**Type:** project

**Score:** 90/100 (Grade: A)

**Verdict:** `KEEP` | **Priority:** Low

**Score Breakdown:**
- Metadata: 35/35
- Quality: 25/35
- Necessity: 30/30

**Issues:**

🟡 **[WARNING]** quality
   - **Issue:** No examples section found
   - **Recommendation:** Add concrete examples of skill usage

**Content Analysis:**
- Lines: 667
- Has examples: ❌
- Has output format: ✅
- Has actionable instructions: ✅
- Code blocks: 15

---

### performance-test

**Location:** `.opencode/skill/performance-test/SKILL.md`

**Type:** project

**Score:** 92/100 (Grade: A)

**Verdict:** `KEEP` | **Priority:** Low

**Score Breakdown:**
- Metadata: 35/35
- Quality: 27/35
- Necessity: 30/30

**Issues:**

🟡 **[WARNING]** quality
   - **Issue:** No output format defined
   - **Recommendation:** Add '## Output Format' section

**Content Analysis:**
- Lines: 690
- Has examples: ✅
- Has output format: ❌
- Has actionable instructions: ✅
- Code blocks: 22

---

### team-review

**Location:** `/home/userjyep/.config/opencode/skill/team-review/SKILL.md`

**Type:** global

**Score:** 94/100 (Grade: A)

**Verdict:** `KEEP` | **Priority:** Low

**Score Breakdown:**
- Metadata: 35/35
- Quality: 29/35
- Necessity: 30/30

**Issues:**

🔵 **[INFO]** quality
   - **Issue:** No 'when to use' section
   - **Recommendation:** Add guidance on appropriate usage contexts

**Content Analysis:**
- Lines: 63
- Has examples: ✅
- Has output format: ✅
- Has actionable instructions: ✅
- Code blocks: 3

---

### team-review

**Location:** `.opencode/skill/team-review/SKILL.md`

**Type:** project

**Score:** 94/100 (Grade: A)

**Verdict:** `KEEP` | **Priority:** Low

**Score Breakdown:**
- Metadata: 35/35
- Quality: 29/35
- Necessity: 30/30

**Issues:**

🔵 **[INFO]** quality
   - **Issue:** No 'when to use' section
   - **Recommendation:** Add guidance on appropriate usage contexts

**Content Analysis:**
- Lines: 63
- Has examples: ✅
- Has output format: ✅
- Has actionable instructions: ✅
- Code blocks: 3

---

### deploy-check

**Location:** `/home/userjyep/.config/opencode/skill/deploy-check/SKILL.md`

**Type:** global

**Score:** 98/100 (Grade: A)

**Verdict:** `KEEP` | **Priority:** Low

**Score Breakdown:**
- Metadata: 35/35
- Quality: 33/35
- Necessity: 30/30

**Issues:**

🔵 **[INFO]** quality
   - **Issue:** Only one code block found
   - **Recommendation:** Add more code examples

**Content Analysis:**
- Lines: 72
- Has examples: ✅
- Has output format: ✅
- Has actionable instructions: ✅
- Code blocks: 1

---

### deploy-check

**Location:** `.opencode/skill/deploy-check/SKILL.md`

**Type:** project

**Score:** 98/100 (Grade: A)

**Verdict:** `KEEP` | **Priority:** Low

**Score Breakdown:**
- Metadata: 35/35
- Quality: 33/35
- Necessity: 30/30

**Issues:**

🔵 **[INFO]** quality
   - **Issue:** Only one code block found
   - **Recommendation:** Add more code examples

**Content Analysis:**
- Lines: 72
- Has examples: ✅
- Has output format: ✅
- Has actionable instructions: ✅
- Code blocks: 1

---

### architecture-analyzer

**Location:** `.opencode/skill/architecture-analyzer/SKILL.md`

**Type:** project

**Score:** 100/100 (Grade: A)

**Verdict:** `KEEP` | **Priority:** Low

**Score Breakdown:**
- Metadata: 35/35
- Quality: 35/35
- Necessity: 30/30

**Content Analysis:**
- Lines: 537
- Has examples: ✅
- Has output format: ✅
- Has actionable instructions: ✅
- Code blocks: 29

---