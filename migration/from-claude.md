# Migrating from Claude Code to OpenCode

Complete guide for transitioning Claude Code workflows to OpenCode.

---

## Key Principle: Delete Git Skills, Keep Custom Logic

**The #1 rule:**  
❌ Delete: `.claude/skills/branch/`, `commit/`, `push/`, `create-pr/`  
✅ Keep: All team-specific skills (reviews, checks, audits)  
✅ Migrate: Custom agents and workflows

**Why?** OpenCode has native git workflow support. You don't need custom skills for git operations.

---

## Quick Migration Steps

### Step 1: Identify What You Have

```bash
# List all Claude skills
find .claude/skills -type d -mindepth 1 -maxdepth 1

# Example output:
# .claude/skills/branch
# .claude/skills/commit
# .claude/skills/push
# .claude/skills/create-pr
# .claude/skills/team-review
# .claude/skills/deploy-check
```

**Categorize:**
- **Git workflows** (branch, commit, push, create-pr) → DELETE
- **Team-specific** (team-review, deploy-check) → MIGRATE
- **Agents** → MIGRATE with enhancements

---

### Step 2: Remove Git Workflow Skills

```bash
# These are NOT needed in OpenCode
rm -rf .claude/skills/branch
rm -rf .claude/skills/commit  
rm -rf .claude/skills/push
rm -rf .claude/skills/create-pr
```

**Instead, use natural language:**

| Old (Claude Code) | New (OpenCode) |
|-------------------|----------------|
| `/branch` | "create a feature branch for authentication" |
| `/commit` | "commit my changes with a good message" |
| `/push` | "push this to remote" |
| `/create-pr` | "create a PR for these changes" |

---

### Step 3: Migrate Custom Skills

#### Format Changes

**Claude Code format:**
```.claude/skills/team-review/SKILL.md
---
description: Review code for team standards
---
[instructions]
```

**OpenCode format:**
```
.opencode/skill/team-review/SKILL.md
---
name: team-review
description: Review code for team standards
license: MIT
compatibility: opencode
---
[instructions]
```

#### Migration Script

```bash
#!/bin/bash
# migrate-skills.sh

for skill_dir in .claude/skills/*/; do
    skill_name=$(basename "$skill_dir")
    
    # Skip git-related skills
    if [[ "$skill_name" =~ ^(branch|commit|push|create-pr)$ ]]; then
        echo "⏭️  Skipping $skill_name (native in OpenCode)"
        continue
    fi
    
    # Create OpenCode skill directory
    mkdir -p ".opencode/skill/$skill_name"
    
    # Read old SKILL.md
    old_file=".claude/skills/$skill_name/SKILL.md"
    if [ -f "$old_file" ]; then
        # Extract description
        description=$(grep "^description:" "$old_file" | sed 's/description: //')
        
        # Extract content (after frontmatter)
        content=$(awk '/^---$/,/^---$/{next} {print}' "$old_file")
        
        # Create new SKILL.md
        cat > ".opencode/skill/$skill_name/SKILL.md" <<EOF
---
name: $skill_name
description: $description
license: MIT
compatibility: opencode
---

$content
EOF
        
        echo "✅ Migrated $skill_name"
    fi
done
```

**Run it:**
```bash
chmod +x migrate-skills.sh
./migrate-skills.sh
```

---

### Step 4: Migrate Agents

#### Format Enhancements

**Claude Code:**
```markdown
---
name: code-reviewer
description: Reviews code
model: sonnet
---
Instructions...
```

**OpenCode (enhanced):**
```markdown
---
description: Reviews code for quality and best practices
mode: subagent
model: anthropic/claude-sonnet-4-20250514
temperature: 0.1
tools:
  write: false
  edit: false
permission:
  edit: deny
  bash:
    "*": deny
    "git status": allow
    "git diff*": allow
---
Instructions...
```

#### Key Additions

1. **Mode specification:**
   - `primary` - Main agent (Tab key switching)
   - `subagent` - Invoked by @ mention or automatically
   - `all` - Can be either (default)

2. **Tool control:**
   ```yaml
   tools:
     write: false
     edit: false
     bash: true
   ```

3. **Granular permissions:**
   ```yaml
   permission:
     edit: deny
     bash:
       "*": deny
       "git status": allow
       "git diff*": allow
       "git log*": allow
     webfetch: allow
   ```

4. **Model specification:**
   ```yaml
   model: anthropic/claude-sonnet-4-20250514
   # or: opencode/gpt-5.1-codex
   ```

---

### Step 5: Test Your Migration

```bash
cd your-project

# Start OpenCode
opencode

# Test native git workflow
> "commit my changes"
> "create a PR"

# Test migrated skills
> skill({ name: "team-review" })
> skill({ name: "deploy-check" })

# Test agents
> @code-reviewer analyze this file

# Switch to plan mode
<Tab>
> "analyze this architecture"
```

---

## Detailed Comparison

### Skills Directory Structure

| Claude Code | OpenCode | Compatible? |
|-------------|----------|-------------|
| `.claude/skills/name/SKILL.md` | `.opencode/skill/name/SKILL.md` | OpenCode reads both |
| Folder name can differ from skill | Folder name MUST match `name:` field | Strict |
| `description:` required | `name:` and `description:` required | More strict |

---

### Frontmatter Fields

| Field | Claude Code | OpenCode | Notes |
|-------|-------------|----------|-------|
| `name` | Optional | **Required** | Must match folder name |
| `description` | Required | Required | 1-1024 characters |
| `license` | N/A | Optional | e.g., MIT |
| `compatibility` | N/A | Optional | e.g., opencode |
| `metadata` | N/A | Optional | Key-value pairs |

---

### Agent Configuration

| Feature | Claude Code | OpenCode |
|---------|-------------|----------|
| Mode control | Limited | `primary`, `subagent`, `all` |
| Tool control | Basic | Per-tool enable/disable |
| Permissions | Basic | Granular (allow/deny/ask) |
| Temperature | Not configurable | Per-agent temperature |
| Max steps | N/A | Configurable iteration limit |
| Task permissions | N/A | Control which subagents can be invoked |

---

## Common Migration Patterns

### Pattern 1: Read-Only Review Agent

**Claude Code:**
```markdown
---
name: reviewer
description: Code reviewer
---
Review code for issues.
```

**OpenCode:**
```markdown
---
description: Code reviewer with read-only access
mode: subagent
tools:
  write: false
  edit: false
permission:
  edit: deny
  bash:
    "*": deny
    "git status": allow
    "git diff*": allow
---
Review code for issues. You are in read-only mode.
```

---

### Pattern 2: Test Writer with Controlled Access

**OpenCode enhancement:**
```markdown
---
description: Generates comprehensive tests
mode: subagent
temperature: 0.2
tools:
  write: true
  edit: true
permission:
  edit: ask
  bash:
    "npm test*": allow
    "yarn test": allow
    "*": deny
---
Generate tests following project patterns.
```

**Benefits:**
- `permission.edit: ask` - Prompts before writing files
- `permission.bash` - Only allows test commands
- `temperature: 0.2` - Slightly more creative for test cases

---

### Pattern 3: Security Agent with Web Access

**OpenCode enhancement:**
```markdown
---
description: Security vulnerability scanner
mode: subagent
model: anthropic/claude-sonnet-4-20250514
tools:
  write: false
permission:
  edit: deny
  webfetch: allow
---
Scan for security issues. You can fetch CVE databases and security advisories.
```

---

## Migration Checklist

### Pre-Migration
- [ ] Backup `.claude/` directory
- [ ] Document current Claude skills and agents
- [ ] Test OpenCode installation: `opencode --version`
- [ ] Read OpenCode docs: https://opencode.ai/docs

### During Migration
- [ ] Delete git workflow skills (branch, commit, push, create-pr)
- [ ] Create `.opencode/skill/` directory
- [ ] Migrate custom skills with updated frontmatter
- [ ] Create `.opencode/agent/` directory
- [ ] Migrate agents with OpenCode enhancements
- [ ] Add permission controls
- [ ] Convert appropriate skills to commands (`.opencode/command/`)

### Post-Migration
- [ ] Test native git workflows
- [ ] Test all migrated skills
- [ ] Test all agents
- [ ] Verify permissions work correctly
- [ ] Update team documentation
- [ ] Train team on OpenCode differences

---

## Common Pitfalls

### ❌ Mistake 1: Keeping Git Workflow Skills

**Don't:**
```
.opencode/skill/commit/SKILL.md
.opencode/skill/push/SKILL.md
```

**Do:**
Just ask: "commit my changes" or "push this"

---

### ❌ Mistake 2: Missing `name` Field

**Error:**
```
Skill not loading
```

**Fix:**
```yaml
---
name: team-review  # ← Required!
description: Review code for team standards
---
```

---

### ❌ Mistake 3: Wrong Directory Name

**Error:**
```
# Folder: .opencode/skills/  ← Wrong (with 's')
```

**Fix:**
```
.opencode/skill/  ← Correct (no 's')
```

---

### ❌ Mistake 4: Folder Name Doesn't Match

**Error:**
```yaml
# Folder: .opencode/skill/my-review/
# SKILL.md:
name: team-review  # ← Doesn't match folder!
```

**Fix:**
```yaml
# Either rename folder to match:
.opencode/skill/team-review/

# Or update name field:
name: my-review
```

---

### ❌ Mistake 5: Not Using Permissions

**Don't:**
```markdown
---
description: Code reviewer
mode: subagent
---
```

**Do:**
```markdown
---
description: Code reviewer
mode: subagent
permission:
  edit: deny  # ← Prevent accidental edits
  bash:
    "*": deny
    "git *": allow
---
```

---

## Testing Your Migration

### 1. Verify Skills Load

```bash
opencode

# Check skill tool description
# Should list your migrated skills
```

### 2. Test Each Skill

```bash
# In OpenCode:
skill({ name: "team-review" })
skill({ name: "deploy-check" })
skill({ name: "security-audit" })
```

### 3. Test Agents

```bash
# In OpenCode:
@code-reviewer analyze this function
@test-writer generate tests for this module
```

### 4. Test Permissions

```bash
# Try with plan agent (read-only):
<Tab>  # Switch to plan mode
> "edit this file"  # Should ask for permission or deny
```

### 5. Test Native Git Workflow

```bash
# Make some changes, then:
> "commit my changes with a descriptive message"
> "push this and create a PR"
```

---

## Need Help?

- **OpenCode Docs:** https://opencode.ai/docs/skills
- **Discord:** https://opencode.ai/discord
- **GitHub Issues:** https://github.com/anomalyco/opencode/issues
- **This Repo Examples:** [../examples/](../examples/)

---

## Next Steps

After successful migration:

1. **Test thoroughly** - Try all your workflows
2. **Update documentation** - Document OpenCode patterns for team
3. **Train team** - Explain key differences from Claude Code
4. **Iterate** - Refine skills based on usage
5. **Explore** - Try OpenCode-specific features (permissions, commands)

**Congratulations on migrating to OpenCode!** 🎉
