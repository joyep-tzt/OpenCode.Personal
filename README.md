# OpenCode Personal

Personal collection of skills, agents, and commands for OpenCode. Get started in under 5 minutes.

---

## Quick Start

### Install Skills (1 minute)

```bash
./install-skills.sh
```

This interactive script will:
- Copy all skills, agents, and commands to your OpenCode config
- Let you choose installation location (`~/.config/opencode` recommended)
- Show installation summary and next steps

**Manual installation:**
```bash
cp -r .opencode/skill ~/.config/opencode/
cp -r .opencode/agent ~/.config/opencode/
cp -r .opencode/command ~/.config/opencode/
```

**Verify installation:**
```bash
./VERIFICATION-GUIDE.sh
```

---

## What's Included

### 📦 Skills (`skill/`)

**Code Quality:**
- **team-review** - Enforce team code standards
- **deploy-check** - Pre-deployment checklist
- **security-audit** - Security vulnerability scanning

**Performance Testing (NEW in v3.0):**
- **architecture-analyzer** - Parse system architecture for performance testing
- **performance-test** - Generate k6 test scripts with load patterns
- **analyze-k6-results** - Analyze results with production extrapolation and cost modeling

> **Note:** Git workflow skills (branch, commit, push, create-pr) have been removed. OpenCode has **native git support** - just use natural language! See examples below.

### 🤖 Agents (`agent/`)
- **code-reviewer** - Specialized code review agent
- **test-writer** - Test generation agent
- **k6-tester** - Performance testing with k6, architecture analysis, and cost modeling (NEW)

### ⚡ Commands (`command/`)
- **/review** - Quick code review
- **/test** - Run tests with analysis
- **/perf** - Performance testing workflow (NEW)

---

## Usage

### Native Git Workflows (No setup needed!)

OpenCode understands git operations naturally:

```
"commit my changes with a good message"
→ OpenCode analyzes changes and creates commit

"push this and create a PR"
→ OpenCode pushes and creates PR with description
```

**Time saved:** 5-10 minutes per workflow

---

### Using Skills

After installation, use skills by name:

```javascript
skill({ name: "team-review" })
skill({ name: "deploy-check" })
```

Or just ask naturally - OpenCode will invoke the right skill:
```
"review this code for our team standards"
"check if this is ready to deploy"
```

---

### Using Agents

Invoke agents with @ mention:

```
@code-reviewer analyze this file for security issues
@test-writer generate tests for this function
```

---

### Using Commands

Use slash commands:

```
/review
/test
/perf analyze    # NEW: Analyze architecture
/perf create     # NEW: Generate k6 test script
/perf results    # NEW: Analyze k6 results
```

---

## Performance Testing with k6 (NEW in v3.0)

Test your system's performance, extrapolate QA results to production, and estimate costs for scaling.

### Quick Start

```bash
# 1. Analyze your architecture
/perf analyze "My API runs on EKS with 4 CPU, 2GB RAM, 2 pods in prod. 
               QA has 1 CPU, 512MB, 1 pod. Target: 2,000 RPS."

# 2. Generate k6 test script
/perf create --target-rps 2000

# 3. Run test (manually)
k6 run performance-test.js --out json=results.json

# 4. Analyze results
/perf analyze-results results.json
```

### What You Get

**Architecture Analysis:**
- Component identification (API, SQS, Lambda, RDS)
- Resource mapping (QA vs Production)
- Bottleneck predictions
- Test strategy recommendations

**K6 Script Generation:**
- Multiple load patterns (baseline, ramp, spike, stress, soak)
- Appropriate thresholds (p95, p99, error rate)
- Portable scripts (run anywhere)
- CloudWatch monitoring instructions

**Results Analysis:**
- Production capacity extrapolation (QA → Prod)
- Multi-factor scaling formulas
- Reality adjustments (cold starts, network latency)
- Confidence levels

**Cost Modeling:**
- Current infrastructure costs
- Scaling scenarios (2x, 3x, 5x load)
- Optimization opportunities (batching, spot instances)
- Cost per RPS analysis

### Example Output

```
## Production Estimate (from QA test)

QA Results: 250 RPS @ 78% CPU
Production Capacity: 1,471 RPS (75% confidence)

Extrapolation:
- CPU scaling: 4x
- Pod scaling: 2x
- Reality factor: 1.25x
- Combined: 6.8x capacity

Cost for 3,000 RPS: $1,205/month
(with RDS Proxy and optimizations)

Critical Recommendations:
🔴 Implement RDS Proxy ($11/month) - Database connections will exhaust
🟡 Request Lambda concurrency increase to 3,000 (free)
```

### Architecture Examples

See `examples/k6/` for:
- Sample architecture profiles (YAML)
- k6 test scripts (all load patterns)
- Complete analysis reports
- Cost estimation examples

### Supported AWS Stack

- **Compute:** EKS, ECS, Lambda
- **Queues:** SQS Standard
- **Notifications:** SNS
- **Database:** RDS PostgreSQL
- **Monitoring:** CloudWatch

### Learn More

- **k6 Installation:** https://k6.io/docs/get-started/installation/
- **Examples:** [examples/k6/README.md](examples/k6/README.md)
- **Agent Details:** [.opencode/agent/k6-tester.md](.opencode/agent/k6-tester.md)

---

## Key Features

### ✅ OpenCode vs Claude Code

| Feature | Claude Code | OpenCode |
|---------|-------------|----------|
| **Git Workflows** | Custom skills required | **Built-in native support** |
| **Commits** | `/commit` skill | "commit with good message" |
| **PRs** | `/create-pr` skill | "create a PR" |
| **Permissions** | Basic | **Granular** (allow/deny/ask) |
| **Agents** | Limited | Primary + Subagents with Tab |

### 🚀 What Makes This Different

- **Native git support** - No custom skills needed for commits/PRs
- **Production-ready** - All skills tested and documented
- **One-command install** - Get started immediately
- **Team-friendly** - Share skills via git repo
- **Verified** - Includes verification script

---

## Structure

```
.opencode/              # Skills, agents, and commands
├── skill/             # Custom skills
│   ├── team-review/
│   ├── deploy-check/
│   ├── security-audit/
│   ├── architecture-analyzer/  # NEW
│   ├── performance-test/       # NEW
│   └── analyze-k6-results/     # NEW
├── agent/             # Custom agents
│   ├── code-reviewer.md
│   ├── test-writer.md
│   └── k6-tester.md            # NEW
└── command/           # Slash commands
    ├── review.md
    ├── test.md
    └── perf.md                 # NEW

examples/              # Example usage
└── k6/               # Performance testing examples
    ├── architecture-qa-vs-prod.yaml
    └── README.md

guides/                # Documentation
└── native-workflows.md

migration/             # Migration guides
└── from-claude.md
```

---

## Documentation

### For Users
- **Quick Start** - This README (you're here!)
- **Native Workflows** - [guides/native-workflows.md](guides/native-workflows.md)
- **Verification** - Run `./VERIFICATION-GUIDE.sh`

### For Teams
- **Migration from Claude** - [migration/from-claude.md](migration/from-claude.md)
- **Team Adoption** - Share this repo with your team

---

## When to Use What

### ✅ Use Native OpenCode For:
- Git commits (don't create custom skills!)
- Pushing to remote
- Creating PRs
- Branch management
- Basic code analysis

### ✅ Create Custom Skills For:
- Team-specific code standards
- Custom deployment checks
- Specialized security audits
- Domain-specific reviews

### ✅ Create Custom Agents For:
- Specialized workflows (code review, testing)
- Multi-step processes
- Tasks requiring specific tool access

### ✅ Create Custom Commands For:
- Frequently repeated tasks
- Parameterized operations
- Quick shortcuts

---

## Contributing

Found a useful skill/agent/command? Share it!

1. Add to `.opencode/skill/`, `.opencode/agent/`, or `.opencode/command/`
2. Test thoroughly
3. Document in README
4. Submit PR

---

## Resources

### OpenCode
- **Official Docs:** https://opencode.ai/docs
- **Skills Guide:** https://opencode.ai/docs/skills
- **Agents Guide:** https://opencode.ai/docs/agents
- **Commands Guide:** https://opencode.ai/docs/commands
- **Discord:** https://opencode.ai/discord
- **GitHub:** https://github.com/anomalyco/opencode

### This Repository
- **Issues:** Report bugs or request features
- **Discussions:** Share ideas and use cases

---

## FAQ

**Q: Do I need to restart OpenCode after installing?**  
A: Yes, restart OpenCode to load new skills/agents/commands.

**Q: Can I use this with Claude Code too?**  
A: Yes! OpenCode also reads `.claude/` for compatibility. See [migration guide](migration/from-claude.md).

**Q: Should I commit `.opencode/` to my project repo?**  
A: Yes! Share skills/agents/commands with your team via git.

**Q: Where should I install skills?**  
A: `~/.config/opencode/` for personal global skills, or `.opencode/` in your project for team-shared skills.

---

## License

MIT - Feel free to use and modify for your team's needs.

---

## Getting Help

1. Check [OpenCode docs](https://opencode.ai/docs)
2. Read [native workflows guide](guides/native-workflows.md)
3. Run verification: `./VERIFICATION-GUIDE.sh`
4. Ask in [Discord](https://opencode.ai/discord)
5. [File an issue](https://github.com/joyep-tzt/OpenCode.Personal/issues)

---

**Ready to get started?**

```bash
./install-skills.sh
```

Then open OpenCode and try:
```
skill({ name: "team-review" })
@code-reviewer analyze this file
/review
```

🎉 Happy coding with OpenCode!
