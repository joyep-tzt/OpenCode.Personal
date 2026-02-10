# OpenCode Skill Registry

> Complete index of available OpenCode skills with descriptions, workflows, and usage

**Last Updated:** 2026-02-07  
**Total Skills:** 6  
**Global Skills:** 3  
**Project Skills:** 3

---

## 📊 Quick Reference

| Skill | Location | Score | Grade | Workflow | Status |
|-------|----------|-------|-------|----------|--------|
| [architecture-analyzer](#architecture-analyzer) | Project | 100 | A | performance-testing | ✅ Active |
| [deploy-check](#deploy-check) | Global | 98 | A | deployment | ✅ Active |
| [team-review](#team-review) | Global | 94 | A | code-review | ✅ Active |
| [performance-test](#performance-test) | Project | 92 | A | performance-testing | ✅ Active |
| [security-audit](#security-audit) | Global | 90 | A | security | ✅ Active |
| [analyze-k6-results](#analyze-k6-results) | Project | 90 | A | performance-testing | ✅ Active |

---

## 🎯 By Workflow

### Performance Testing Suite

A complete workflow for performance testing:

```
architecture-analyzer → performance-test → analyze-k6-results
        ↓                       ↓                    ↓
  Creates profile      Generates k6 script    Analyzes results
  and test strategy    with load patterns     with extrapolation
```

| Order | Skill | Purpose |
|-------|-------|---------|
| 1 | **architecture-analyzer** | Parse system architecture and create test strategy |
| 2 | **performance-test** | Generate k6 test scripts with extrapolation |
| 3 | **analyze-k6-results** | Analyze results and predict production capacity |

### Code Quality

| Skill | Purpose |
|-------|---------|
| **team-review** | Review code against team standards |

### Security

| Skill | Purpose |
|-------|---------|
| **security-audit** | Comprehensive security vulnerability scanning |

### Deployment

| Skill | Purpose |
|-------|---------|
| **deploy-check** | Pre-deployment checklist verification |

---

## 📁 Global Skills

Available in `~/.config/opencode/skill/`

### deploy-check

**Score:** 98/100 (Grade A)  
**Workflow:** deployment  
**Audience:** developers, devops

**Purpose:**  
Verify all pre-deployment requirements are met before releasing to production.

**Key Features:**
- Code quality checks (tests, coverage, debug statements)
- Configuration validation (env vars, secrets)
- Database checks (migrations, backups)
- Documentation verification (CHANGELOG, README)
- Security validation
- Performance verification

**When to Use:**
- ✅ Before merging to main
- ✅ Before deploying to staging
- ✅ Before deploying to production
- ✅ After major dependency updates

**Integration:** Standalone skill

---

### security-audit

**Score:** 90/100 (Grade A)  
**Workflow:** security  
**Audience:** developers, security teams

**Purpose:**  
Perform comprehensive security audit of code changes, identifying vulnerabilities and security best practices violations.

**Key Features:**
- Input validation checks (SQL injection, XSS, command injection)
- Authentication & authorization validation
- Data protection verification (encryption, secrets)
- Dependency vulnerability scanning
- Configuration security review
- API security checks

**Severity Levels:**
- 🔴 Critical: SQL injection, exposed secrets, auth bypass
- 🟠 High: XSS, broken auth, sensitive data exposure
- 🟡 Medium: Missing rate limiting, weak crypto
- 🟢 Low: Code complexity, missing docs

**When to Use:**
- ✅ Before every PR merge
- ✅ Before production deployment
- ✅ After dependency updates
- ✅ Regular security audits
- ✅ When handling sensitive data

**Integration:** Standalone skill

---

### team-review

**Score:** 94/100 (Grade A)  
**Workflow:** code-review  
**Audience:** developers

**Purpose:**  
Review code against team-specific standards and best practices.

**Key Features:**
- Code quality (function length, magic numbers, naming)
- TypeScript standards (type annotations, no `any`)
- Testing requirements (coverage, edge cases)
- Documentation standards (JSDoc, README updates)

**Severity Levels:**
- **Critical:** Must fix before merge
- **Warning:** Should fix, but can merge
- **Info:** Nice to have improvement

**When to Use:**
- ✅ During code review
- ✅ Before PR approval
- ✅ Team onboarding

**Integration:** Standalone skill

---

## 📁 Project Skills

Available in `.opencode/skill/` (project-specific)

### architecture-analyzer

**Score:** 100/100 (Grade A)  
**Workflow:** performance-testing  
**Audience:** architects, performance engineers, devops

**Purpose:**  
Parse and understand system architecture for performance testing. Creates architecture profile and test strategy.

**Key Features:**
- Parse natural language architecture descriptions
- Analyze infrastructure as code (Terraform, K8s, CloudFormation)
- Identify components and dependencies
- Predict bottlenecks (DB connections, Lambda concurrency, etc.)
- Calculate extrapolation factors (QA → Production)
- Generate test strategy recommendations

**Input Formats:**
- Natural language descriptions
- YAML architecture files
- Terraform configurations
- Kubernetes manifests
- Application code analysis

**Output:**
- YAML architecture profile
- Bottleneck predictions
- Test strategy recommendations
- CloudWatch monitoring guide

**When to Use:**
- ✅ Before creating k6 test scripts
- ✅ When planning production capacity
- ✅ When investigating performance issues
- ✅ Before scaling infrastructure
- ✅ System documentation

**Integration:**
- Input to: `performance-test`
- Used by: `analyze-k6-results`

---

### performance-test

**Score:** 92/100 (Grade A)  
**Workflow:** performance-testing  
**Audience:** QA engineers, performance testers, devops

**Purpose:**  
Generate production-ready k6 test scripts with appropriate load patterns, thresholds, and extrapolation logic.

**Key Features:**
- Multiple load patterns (constant, ramping, spike, stress, soak)
- QA load calculation from production targets
- SLO-based threshold configuration
- Complete k6 script template with comments
- CI/CD integration examples
- CloudWatch monitoring commands

**Load Patterns:**
1. **Baseline:** Constant load for steady-state measurement
2. **Ramp-up:** Gradual increase to find capacity limits
3. **Spike:** Sudden traffic bursts (Black Friday scenarios)
4. **Stress:** Push beyond limits to find breaking point
5. **Soak:** Long-running stability test (12+ hours)

**Output:**
- Runnable k6 JavaScript file
- README with usage instructions
- CloudWatch monitoring queries
- Environment variable template

**When to Use:**
- ✅ After architecture analysis
- ✅ Before production deployment
- ✅ When capacity planning
- ✅ After infrastructure changes
- ✅ Regular regression testing

**Integration:**
- Uses: `architecture-analyzer` (profile)
- Produces input for: `analyze-k6-results`

---

### analyze-k6-results

**Score:** 90/100 (Grade A)  
**Workflow:** performance-testing  
**Audience:** performance engineers, devops, architects

**Purpose:**  
Analyze k6 test results, extrapolate QA findings to production capacity, identify bottlenecks, and provide cost-performance recommendations.

**Key Features:**
- Parse k6 JSON and text output
- Threshold compliance checking
- Production extrapolation with multi-factor scaling
- Bottleneck identification (DB connections, Lambda concurrency, SQS)
- Comprehensive cost analysis and scenarios
- Reality checks and confidence levels

**Analysis Components:**
1. Result parsing (RPS, latency, errors)
2. Threshold compliance check
3. Production extrapolation (6.8x factor example)
4. Bottleneck identification
5. Cost analysis (current + scaling scenarios)
6. Reality checks and caveats

**Output Formats:**
- Markdown report (human-readable)
- JSON data (machine-readable)
- Cost scenarios (CSV for budgeting)

**When to Use:**
- ✅ After k6 test completes
- ✅ Before production deployment
- ✅ When planning capacity increases
- ✅ After infrastructure changes
- ✅ Regular performance reviews

**Integration:**
- Uses: `architecture-analyzer` (profile)
- Analyzes: `performance-test` output

---

## 🔧 Using Skills

### Load a Skill

In OpenCode TUI:
```
/skill skill-name
```

Or let opencode discover and load automatically when relevant.

### Check Available Skills

Run the auditor:
```bash
python skill_auditor.py
```

### Audit a Specific Skill

```bash
python skill_auditor.py --skill skill-name
```

---

## 📝 Creating New Skills

1. Use the template:
   ```bash
   cp SKILL_TEMPLATE.md .opencode/skill/new-skill/SKILL.md
   ```

2. Follow conventions:
   - Read [SKILL_CONVENTIONS.md](SKILL_CONVENTIONS.md)
   - Use standard workflow categories
   - Include all required sections

3. Validate quality:
   ```bash
   python skill_auditor.py --skill new-skill
   ```

4. Target score: 80+ (Grade A)

---

## 🎯 Recommended Next Skills

Based on coverage gaps:

### High Priority

| Skill | Workflow | Use Case |
|-------|----------|----------|
| **test-coverage** | testing | Analyze test coverage gaps |
| **docs-check** | documentation | Verify documentation completeness |
| **ci-cd-helper** | deployment | GitHub Actions workflow assistance |

### Medium Priority

| Skill | Workflow | Use Case |
|-------|----------|----------|
| **accessibility-audit** | testing | WCAG compliance checks |
| **database-review** | database | Migration safety and query optimization |
| **api-documentation** | documentation | OpenAPI/Swagger validation |

---

## 📈 Quality Metrics

### Overall Portfolio Health

```
Skills: 6
Grade A: 6 (100%)
Grade B: 0 (0%)
Grade C: 0 (0%)
Grade D: 0 (0%)
Grade F: 0 (0%)

Average Score: 94/100
Critical Issues: 0
Warnings: 0
```

### By Workflow

| Workflow | Skills | Avg Score |
|----------|--------|-----------|
| performance-testing | 3 | 94 |
| deployment | 1 | 98 |
| code-review | 1 | 94 |
| security | 1 | 90 |

---

## 🔍 Finding Skills

### By Use Case

**Performance Testing:**
1. Start with `architecture-analyzer`
2. Generate tests with `performance-test`
3. Analyze results with `analyze-k6-results`

**Pre-Deployment:**
- Run `deploy-check` before any deployment
- Run `security-audit` for security-critical changes

**Code Review:**
- Use `team-review` for standards compliance

### By Audience

**Architects:**
- `architecture-analyzer`
- `analyze-k6-results`

**Developers:**
- `team-review`
- `security-audit`
- `deploy-check`

**DevOps:**
- `deploy-check`
- `performance-test`
- `analyze-k6-results`

**QA Engineers:**
- `performance-test`
- `analyze-k6-results`

---

## 📚 Resources

- [SKILL_CONVENTIONS.md](SKILL_CONVENTIONS.md) - Standards and best practices
- [SKILL_TEMPLATE.md](SKILL_TEMPLATE.md) - Template for new skills
- [skill_auditor.py](skill_auditor.py) - Audit and validation tool

---

## 🔄 Maintenance

Last full audit: 2026-02-07  
Next scheduled audit: 2026-03-07  

Run monthly:
```bash
python skill_auditor.py --format markdown -o monthly-audit.md
```

---

**Registry Version:** 1.0  
**Maintained by:** OpenCode Personal Skills
