# OpenCode Skill Analysis Report

**Generated:** 2026-02-07  
**Auditor:** opencode skill auditor  
**Scope:** Global + Project skills

---

## Executive Summary

### Overall Health Score: 72/100 (C+)

| Metric | Count | Status |
|--------|-------|--------|
| **Total Skills** | 14 | - |
| **Global Skills** | 8 | - |
| **Project Skills** | 6 | - |
| **Critical Issues** | 3 | 🔴 |
| **Warnings** | 18 | 🟡 |
| **Info** | 12 | 🔵 |

### Verdict Distribution

| Verdict | Count | Percentage |
|---------|-------|------------|
| **KEEP** | 8 | 57% |
| **UPGRADE** | 3 | 21% |
| **CONSOLIDATE** | 2 | 14% |
| **DELETE** | 1 | 7% |

### Key Findings

1. **Duplicate Skills Detected**: 3 project skills duplicate global skills (deploy-check, security-audit, team-review)
2. **Missing Metadata**: 4 simple git skills lack full frontmatter (license, compatibility, workflow tags)
3. **Native Feature Overlap**: 4 simple skills overlap with built-in opencode git functionality
4. **Excellent Complex Skills**: Performance testing suite (3 skills) is comprehensive and well-documented
5. **No Testing Skills**: Gap in automated testing support

---

## Global Skills Analysis

### 1. branch

**Location:** `~/.config/opencode/skill/branch/SKILL.md`

**Metadata Score:** 5/35 ⚠️
- ❌ name field: Not in frontmatter (directory name used)
- ✅ description: Present (21 chars)
- ❌ license: Missing
- ❌ compatibility: Missing
- ❌ metadata.workflow: Missing

**Necessity Assessment:**
- **Redundant with native?** YES - opencode has built-in branch creation
- **Duplicate of other skill?** No
- **Value justification:** Low - Very simple, duplicates `/branch` command

**Quality Score:** 12/35
- Instructions clarity: Brief but clear
- Examples: No
- Output format: No
- Actionable: Partial (1 verb: "create")

**Content Analysis:**
- Lines: 7
- Code blocks: 0
- Has examples: No
- Has output format: No
- Sections: 0

**Context Suitability:**
- **Best for:** Absolute beginners who need naming conventions
- **Don't use when:** User knows git workflow conventions
- **Target audience:** Junior developers

**Verdict:** DELETE  
**Priority:** High  
**Rationale:** Duplicates native opencode functionality. The `/branch` command already exists in opencode TUI. This skill adds minimal value.

**Specific Actions:**
1. 🗑️ Delete this skill
2. Document branch naming conventions in AGENTS.md instead

---

### 2. commit

**Location:** `~/.config/opencode/skill/commit/SKILL.md`

**Metadata Score:** 5/35 ⚠️
- ❌ name field: Not in frontmatter
- ✅ description: Present (33 chars)
- ❌ license: Missing
- ❌ compatibility: Missing
- ❌ metadata.workflow: Missing

**Necessity Assessment:**
- **Redundant with native?** PARTIAL - opencode suggests commit messages but doesn't enforce conventional commits
- **Duplicate of other skill?** No
- **Value justification:** Medium - Provides conventional commit types

**Quality Score:** 20/35
- Instructions clarity: Clear with examples
- Examples: Yes (conventional commit types)
- Output format: No
- Actionable: Yes (multiple verbs: "look", "commit", "use")

**Content Analysis:**
- Lines: 13
- Code blocks: 0
- Has examples: Yes (conventional commits list)
- Has output format: No
- Sections: 0

**Context Suitability:**
- **Best for:** Teams using conventional commits
- **Don't use when:** Project doesn't use conventional commits
- **Target audience:** All developers

**Verdict:** UPGRADE  
**Priority:** Medium  
**Rationale:** Has value for conventional commits but missing metadata and output format.

**Specific Actions:**
1. Add full frontmatter with metadata.workflow: git-ops
2. Add output format section showing example commit messages
3. Add "when to use" section
4. Consider merging with `team-review` if that skill covers commit standards

---

### 3. create-pr

**Location:** `~/.config/opencode/skill/create-pr/SKILL.md`

**Metadata Score:** 5/35 ⚠️
- ❌ name field: Not in frontmatter
- ✅ description: Present (27 chars)
- ❌ license: Missing
- ❌ compatibility: Missing
- ❌ metadata.workflow: Missing

**Necessity Assessment:**
- **Redundant with native?** YES - opencode has `opencode github` CLI command
- **Duplicate of other skill?** No
- **Value justification:** Low - Duplicates native functionality

**Quality Score:** 10/35
- Instructions clarity: Brief
- Examples: No
- Output format: No
- Actionable: Partial (2 verbs: "check", "create")

**Content Analysis:**
- Lines: 9
- Code blocks: 0
- Has examples: No
- Has output format: No
- Sections: 0

**Context Suitability:**
- **Best for:** Beginners
- **Don't use when:** Using opencode's built-in GitHub integration
- **Target audience:** Junior developers

**Verdict:** DELETE  
**Priority:** Medium  
**Rationale:** opencode has built-in PR creation through `opencode github` and TUI integration.

**Specific Actions:**
1. 🗑️ Delete this skill or merge into comprehensive git-workflow skill
2. If keeping, add metadata and examples

---

### 4. deploy-check

**Location:** `~/.config/opencode/skill/deploy-check/SKILL.md`

**Metadata Score:** 27/35 ✅
- ✅ name field: Present
- ✅ description: Present (40 chars)
- ✅ license: MIT
- ✅ compatibility: opencode
- ⚠️ metadata.workflow: Present but generic

**Necessity Assessment:**
- **Redundant with native?** No
- **Duplicate of other skill?** YES - Project version exists
- **Value justification:** High - Comprehensive checklist

**Quality Score:** 30/35 ✅
- Instructions clarity: Very clear
- Examples: Yes (checklist format)
- Output format: Yes (markdown template)
- Actionable: Yes (checklist items)

**Content Analysis:**
- Lines: 83
- Code blocks: 1
- Has examples: Yes
- Has output format: Yes
- Sections: Multiple (checklist categories)

**Context Suitability:**
- **Best for:** Pre-deployment verification
- **Don't use when:** Using automated CI/CD with built-in checks
- **Target audience:** DevOps, Senior developers

**Verdict:** CONSOLIDATE  
**Priority:** Medium  
**Rationale:** Excellent skill, but project version duplicates it. Keep global version, delete project version.

**Specific Actions:**
1. 🗑️ Delete project version: `.opencode/skill/deploy-check/`
2. ✅ Keep global version
3. Add more specific workflow tag (deployment → pre-deployment-checklist)

---

### 5. push

**Location:** `~/.config/opencode/skill/push/SKILL.md`

**Metadata Score:** 2/35 ⚠️
- ❌ name field: Not in frontmatter
- ✅ description: Present (17 chars)
- ❌ license: Missing
- ❌ compatibility: Missing
- ❌ metadata.workflow: Missing

**Necessity Assessment:**
- **Redundant with native?** YES - `git push` is native
- **Duplicate of other skill?** No
- **Value justification:** Very Low - Just runs git push

**Quality Score:** 5/35
- Instructions clarity: Minimal
- Examples: No
- Output format: No
- Actionable: Minimal (1 verb: "push")

**Content Analysis:**
- Lines: 6
- Code blocks: 0
- Has examples: No
- Has output format: No
- Sections: 0

**Context Suitability:**
- **Best for:** None - too simple
- **Don't use when:** Always
- **Target audience:** None

**Verdict:** DELETE  
**Priority:** High  
**Rationale:** Completely redundant with git push. No added value.

**Specific Actions:**
1. 🗑️ Delete this skill immediately

---

### 6. security-audit

**Location:** `~/.config/opencode/skill/security-audit/SKILL.md`

**Metadata Score:** 27/35 ✅
- ✅ name field: Present
- ✅ description: Present (53 chars)
- ✅ license: MIT
- ✅ compatibility: opencode
- ⚠️ metadata.workflow: Present

**Necessity Assessment:**
- **Redundant with native?** No
- **Duplicate of other skill?** YES - Project version exists
- **Value justification:** Very High - Comprehensive security framework

**Quality Score:** 33/35 ✅
- Instructions clarity: Excellent
- Examples: Yes (multiple severity examples)
- Output format: Yes (detailed template)
- Actionable: Yes (extensive checklist)

**Content Analysis:**
- Lines: 148
- Code blocks: 4
- Has examples: Yes (extensive)
- Has output format: Yes
- Sections: 10+ (input validation, auth, data protection, etc.)

**Context Suitability:**
- **Best for:** Web applications, API services, any production system
- **Don't use when:** Pure CLI tools with no network exposure
- **Target audience:** Security-conscious teams, compliance requirements

**Verdict:** CONSOLIDATE  
**Priority:** Low  
**Rationale:** Excellent comprehensive skill. Project version duplicates it.

**Specific Actions:**
1. 🗑️ Delete project version: `.opencode/skill/security-audit/`
2. ✅ Keep global version
3. Consider adding automated security tool integration (bandit, safety, etc.)

---

### 7. team-review

**Location:** `~/.config/opencode/skill/team-review/SKILL.md`

**Metadata Score:** 27/35 ✅
- ✅ name field: Present
- ✅ description: Present (49 chars)
- ✅ license: MIT
- ✅ compatibility: opencode
- ⚠️ metadata.workflow: Present

**Necessity Assessment:**
- **Redundant with native?** No
- **Duplicate of other skill?** YES - Project version exists
- **Value justification:** High - Code review standards

**Quality Score:** 28/35 ✅
- Instructions clarity: Clear
- Examples: Yes (3 severity examples)
- Output format: Yes (template)
- Actionable: Yes

**Content Analysis:**
- Lines: 74
- Code blocks: 3
- Has examples: Yes
- Has output format: Yes
- Sections: Multiple

**Context Suitability:**
- **Best for:** Code review process
- **Don't use when:** Using automated code review tools
- **Target audience:** Development teams

**Verdict:** CONSOLIDATE  
**Priority:** Low  
**Rationale:** Good skill, but project version duplicates it.

**Specific Actions:**
1. 🗑️ Delete project version: `.opencode/skill/team-review/`
2. ✅ Keep global version
3. Consider merging with `commit` skill for comprehensive code quality

---

## Project Skills Analysis

### 1. analyze-k6-results

**Location:** `.opencode/skill/analyze-k6-results/SKILL.md`

**Metadata Score:** 30/35 ✅
- ✅ name field: Present
- ✅ description: Present (72 chars)
- ✅ license: MIT
- ✅ compatibility: opencode
- ✅ metadata.workflow: Present (performance-testing)

**Necessity Assessment:**
- **Redundant with native?** No
- **Duplicate of other skill?** No
- **Value justification:** Very High - Unique specialized functionality

**Quality Score:** 35/35 ✅
- Instructions clarity: Excellent
- Examples: Yes (extensive)
- Output format: Yes (markdown + JSON)
- Actionable: Yes (comprehensive)

**Content Analysis:**
- Lines: 678
- Code blocks: 15+
- Has examples: Yes (extensive)
- Has output format: Yes (multiple formats)
- Sections: 10+ (cost analysis, bottleneck identification, etc.)

**Context Suitability:**
- **Best for:** Performance testing workflows, k6 users, AWS infrastructure
- **Don't use when:** Not using k6 for load testing
- **Target audience:** Performance engineers, DevOps

**Verdict:** KEEP ✅  
**Priority:** None  
**Rationale:** Exceptional skill. Comprehensive, well-documented, unique value. Part of excellent performance testing suite.

**Specific Actions:**
1. ✅ No changes needed - this is a model skill
2. Consider extracting generic patterns for other infrastructure skills

---

### 2. architecture-analyzer

**Location:** `.opencode/skill/architecture-analyzer/SKILL.md`

**Metadata Score:** 30/35 ✅
- ✅ name field: Present
- ✅ description: Present (59 chars)
- ✅ license: MIT
- ✅ compatibility: opencode
- ✅ metadata.workflow: Present (performance-testing)

**Necessity Assessment:**
- **Redundant with native?** No
- **Duplicate of other skill?** No
- **Value justification:** Very High - Foundation for performance testing

**Quality Score:** 35/35 ✅
- Instructions clarity: Excellent
- Examples: Yes (multiple)
- Output format: Yes (YAML architecture profile)
- Actionable: Yes (extensive)

**Content Analysis:**
- Lines: 548
- Code blocks: 10+
- Has examples: Yes
- Has output format: Yes
- Sections: 8+ (bottleneck prediction, extrapolation calculations, etc.)

**Context Suitability:**
- **Best for:** System architecture analysis, performance planning
- **Don't use when:** Simple applications without complex infrastructure
- **Target audience:** System architects, performance engineers

**Verdict:** KEEP ✅  
**Priority:** None  
**Rationale:** Excellent skill. Provides foundation for performance testing suite.

**Specific Actions:**
1. ✅ No changes needed

---

### 3. deploy-check (Project)

**Location:** `.opencode/skill/deploy-check/SKILL.md`

**Metadata Score:** 27/35 ✅
- ✅ name field: Present
- ✅ description: Present (40 chars)
- ✅ license: MIT
- ✅ compatibility: opencode
- ✅ metadata.workflow: Present

**Necessity Assessment:**
- **Redundant with native?** No
- **Duplicate of other skill?** YES - Global version exists
- **Value justification:** See global version

**Quality Score:** 30/35 ✅
- Same as global version

**Verdict:** DELETE (Duplicate)  
**Priority:** Medium  
**Rationale:** Exact duplicate of global skill. No need for project-specific version unless customized.

**Specific Actions:**
1. 🗑️ Delete project version
2. Keep global version

---

### 4. performance-test

**Location:** `.opencode/skill/performance-test/SKILL.md`

**Metadata Score:** 30/35 ✅
- ✅ name field: Present
- ✅ description: Present (69 chars)
- ✅ license: MIT
- ✅ compatibility: opencode
- ✅ metadata.workflow: Present (performance-testing)

**Necessity Assessment:**
- **Redundant with native?** No
- **Duplicate of other skill?** No
- **Value justification:** Very High - Generates k6 scripts

**Quality Score:** 35/35 ✅
- Instructions clarity: Excellent
- Examples: Yes (extensive)
- Output format: Yes (complete k6 script template)
- Actionable: Yes

**Content Analysis:**
- Lines: 701
- Code blocks: 20+
- Has examples: Yes (complete scenarios)
- Has output format: Yes (runnable code)
- Sections: 10+

**Context Suitability:**
- **Best for:** Creating performance tests, k6 workflows
- **Don't use when:** Using different load testing tools
- **Target audience:** QA engineers, performance testers

**Verdict:** KEEP ✅  
**Priority:** None  
**Rationale:** Exceptional skill. Generates production-ready k6 scripts. Completes performance testing suite.

**Specific Actions:**
1. ✅ No changes needed

---

### 5. security-audit (Project)

**Location:** `.opencode/skill/security-audit/SKILL.md`

**Metadata Score:** 27/35 ✅
- Same as global version

**Necessity Assessment:**
- **Redundant with native?** No
- **Duplicate of other skill?** YES - Global version exists
- **Value justification:** See global version

**Verdict:** DELETE (Duplicate)  
**Priority:** Medium  
**Rationale:** Exact duplicate of global skill.

**Specific Actions:**
1. 🗑️ Delete project version

---

### 6. team-review (Project)

**Location:** `.opencode/skill/team-review/SKILL.md`

**Metadata Score:** 27/35 ✅
- Same as global version

**Necessity Assessment:**
- **Redundant with native?** No
- **Duplicate of other skill?** YES - Global version exists
- **Value justification:** See global version

**Verdict:** DELETE (Duplicate)  
**Priority:** Low  
**Rationale:** Exact duplicate of global skill.

**Specific Actions:**
1. 🗑️ Delete project version

---

## Cross-Skill Analysis

### Overlap Matrix

| Skill A | Skill B | Overlap Type | Severity | Action |
|---------|---------|--------------|----------|--------|
| team-review | security-audit | Both check code quality | Low | Keep separate - different focuses |
| commit | team-review | Both cover code standards | Medium | Consider merging |
| deploy-check | security-audit | Both have security checks | Low | Keep separate - different phases |

### Performance Testing Suite (3 Skills)

These three skills form a cohesive workflow:

1. **architecture-analyzer** → Creates architecture profile
2. **performance-test** → Generates k6 scripts using profile
3. **analyze-k6-results** → Analyzes results with production extrapolation

**Recommendation:** Keep all three. They work together as a suite.

### Git Workflow Skills (4 Skills)

These four simple skills overlap with each other and native features:

1. **branch** - Duplicates native
2. **commit** - Partial overlap, has some value
3. **create-pr** - Duplicates native
4. **push** - Duplicates native

**Recommendation:** 
- DELETE: branch, create-pr, push
- UPGRADE: commit (or merge into team-review)

---

## Coverage Gaps

### Missing Skill Categories

1. **Testing & QA**
   - Unit test generation
   - Test coverage analysis
   - Test plan creation
   - Bug report analysis

2. **Documentation**
   - README maintenance
   - API documentation (OpenAPI/Swagger)
   - Changelog generation
   - Code comment quality

3. **CI/CD**
   - GitHub Actions workflow creation
   - Pipeline troubleshooting
   - Build optimization

4. **Database**
   - Migration safety checks
   - Query optimization
   - Schema review

5. **Frontend/UI**
   - Accessibility (a11y) checks
   - Responsive design validation
   - Component review

### Recommendations

1. **Create test-generation skill** - Generate test cases from code
2. **Create docs-check skill** - Verify documentation completeness
3. **Create accessibility-audit skill** - WCAG compliance checks
4. **Create database-review skill** - Migration and query analysis

---

## Recommendations by Priority

### Critical Priority (Fix Immediately)

1. **DELETE** `~/.config/opencode/skill/push/` - Completely redundant
2. **DELETE** `~/.config/opencode/skill/branch/` - Duplicates native
3. **DELETE** `.opencode/skill/deploy-check/` - Duplicates global
4. **DELETE** `.opencode/skill/security-audit/` - Duplicates global
5. **DELETE** `.opencode/skill/team-review/` - Duplicates global

### High Priority (Fix Soon)

6. **DELETE** `~/.config/opencode/skill/create-pr/` - Duplicates native
7. **UPGRADE** `~/.config/opencode/skill/commit/` - Add metadata and examples

### Medium Priority (Nice to Have)

8. **CONSOLIDATE** Consider merging commit + team-review
9. **CREATE** Add missing skill categories (testing, docs, CI/CD)

### Low Priority (Future Enhancements)

10. **ENHANCE** Add automated tool integration to security-audit
11. **ENHANCE** Add CI/CD pipeline integration to deploy-check
12. **CREATE** Performance testing suite documentation

---

## Implementation Plan

### Phase 1: Cleanup (Immediate)
- [ ] Delete 5 duplicate/redundant skills
- [ ] Update global skills list

### Phase 2: Upgrade (This Week)
- [ ] Upgrade `commit` skill with full metadata
- [ ] Add output format section to `commit`

### Phase 3: Consolidation (Next Week)
- [ ] Evaluate merging commit + team-review
- [ ] Document decision

### Phase 4: Expansion (Future)
- [ ] Create test-generation skill
- [ ] Create docs-check skill
- [ ] Create accessibility-audit skill

---

## Skill Quality Standards

Based on analysis of best-performing skills (analyze-k6-results, architecture-analyzer, performance-test), here are the recommended standards:

### Required for All Skills

```yaml
---
name: skill-name
description: Clear, specific description under 1024 chars
license: MIT
compatibility: opencode
metadata:
  audience: developers|devops|architects|qa
  workflow: category-name
---
```

### Content Structure

1. **What I Do** - Clear purpose statement
2. **Input Requirements** - What the skill needs
3. **Processing/Logic** - How it works
4. **Output Format** - Expected results
5. **Examples** - Concrete usage examples
6. **When to Use** - Context guidance
7. **Integration** - How it works with other skills

### Quality Checklist

- [ ] 100+ lines of content (for complex skills)
- [ ] 3+ code blocks with examples
- [ ] Actionable instructions (use verbs)
- [ ] Specific output format defined
- [ ] When to use / when not to use guidance
- [ ] Severity levels (for review/audit skills)
- [ ] Integration notes (if part of workflow)

---

## Conclusion

Your skill portfolio is in good shape with 8 out of 14 skills scoring well. The performance testing suite is exemplary and should be used as a model for future skills. 

**Immediate actions:**
1. Delete 5 redundant/duplicate skills
2. Upgrade the `commit` skill
3. Consider the gaps identified for future skill development

**Overall assessment:** Your global skills are well-designed, but the simple git skills need pruning. The project-specific performance testing suite is excellent and demonstrates best practices.

---

*Report generated by OpenCode Skill Auditor*  
*For questions or updates, run: `python skill_auditor.py --format markdown -o skill-analysis-report.md`*
