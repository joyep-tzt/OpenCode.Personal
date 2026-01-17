# OpenCode Native Git Workflows

OpenCode has built-in understanding of git workflows - no custom skills needed!

---

## The Problem with Custom Git Skills

**Claude Code approach:**
```
Create custom skills for every git operation:
- .claude/skills/branch/SKILL.md
- .claude/skills/commit/SKILL.md
- .claude/skills/push/SKILL.md
- .claude/skills/create-pr/SKILL.md

Then use: /branch, /commit, /push, /create-pr
```

**OpenCode approach:**
```
No skills needed! Just ask naturally:
"create a branch for this feature"
"commit my changes"
"push this"
"create a PR"
```

---

## Native Git Commands

### 1. Creating Commits

**Just ask:**
```
"commit my changes"
"commit this with a good message"
"create a commit for these changes"
```

**What OpenCode does:**
1. Runs `git status` to see what's changed
2. Runs `git diff` to understand the changes
3. Analyzes the code changes
4. Suggests a conventional commit message
5. Creates the commit

**Example:**
```
You: "commit my changes"

OpenCode analyzes and suggests:
"feat: implement JWT authentication middleware

This adds:
- JWT token validation
- User session management
- Error handling for expired tokens

Create this commit? (yes/no)"

You: "yes"

OpenCode: 
[main a1b2c3d] feat: implement JWT authentication middleware
 3 files changed, 145 insertions(+), 12 deletions(-)
```

---

### 2. Creating Pull Requests

**Just ask:**
```
"create a PR"
"create a pull request for this"
"make a PR with these changes"
```

**What OpenCode does:**
1. Runs `git log main..HEAD` to see all commits
2. Runs `git diff main...HEAD` to see all changes
3. Analyzes the complete changeset
4. Generates comprehensive PR description
5. Uses `gh pr create` to create the PR
6. Returns the PR URL

**Example:**
```
You: "create a PR"

OpenCode:
"Creating pull request...

Analyzed 3 commits:
- feat: add authentication middleware
- feat: add JWT validation
- test: add auth tests

Generating PR description...

## Summary
- Implement JWT authentication
- Add token validation
- Include comprehensive tests

## Changes
- src/auth/middleware.ts: Authentication logic
- src/auth/jwt.ts: Token validation
- src/auth/__tests__/: Test suite

Running: gh pr create --title "Add JWT authentication" --body "..."

✓ Pull request created: https://github.com/user/repo/pull/123"
```

---

### 3. Pushing to Remote

**Just ask:**
```
"push this"
"push to remote"
"push my changes"
```

**What OpenCode does:**
1. Checks if branch has remote tracking
2. Sets up tracking if needed (`-u origin branch-name`)
3. Pushes changes

**Example:**
```
You: "push this"

OpenCode:
"Pushing changes...

git push -u origin feature/auth

Enumerating objects: 12, done.
Counting objects: 100% (12/12), done.
Delta compression using up to 8 threads
Compressing objects: 100% (8/8), done.
Writing objects: 100% (8/8), 2.34 KiB | 2.34 MiB/s, done.
Total 8 (delta 4), reused 0 (delta 0)
To github.com:user/repo.git
 * [new branch]      feature/auth -> feature/auth
Branch 'feature/auth' set up to track remote branch 'feature/auth' from 'origin'.

✓ Pushed successfully"
```

---

### 4. Creating Branches

**Just ask:**
```
"create a branch for authentication"
"make a new feature branch"
"create a branch called feature/auth"
```

**What OpenCode does:**
1. Creates branch with descriptive name
2. Checks out the new branch
3. Confirms creation

**Example:**
```
You: "create a branch for adding authentication"

OpenCode:
"Creating branch...

git checkout -b feature/add-authentication

Switched to a new branch 'feature/add-authentication'

✓ Branch created and checked out"
```

---

## Complete Workflow Example

### Scenario: Adding a New Feature

**Step 1: Create Branch**
```
You: "create a feature branch for user authentication"

OpenCode:
git checkout -b feature/user-authentication
✓ Branch created
```

**Step 2: Make Changes**
```
(You edit code files)
```

**Step 3: Commit Changes**
```
You: "commit my changes with a good message"

OpenCode analyzes changes:
"I see you've added JWT authentication. 

Suggested commit message:
feat: implement JWT authentication middleware

- Add JWT token validation
- Implement user session management
- Include error handling for expired tokens

Proceed? (yes/no)"

You: "yes"

OpenCode:
[feature/user-authentication a1b2c3d] feat: implement JWT authentication middleware
 3 files changed, 145 insertions(+), 12 deletions(-)
✓ Committed
```

**Step 4: Push and Create PR**
```
You: "push this and create a PR"

OpenCode:
"Pushing changes...
git push -u origin feature/user-authentication
✓ Pushed

Creating pull request...
Analyzing 1 commit since main...

gh pr create \
  --title "Implement JWT authentication" \
  --body "## Summary
- Add JWT token validation
- Implement session management
- Include error handling

## Changes
- src/auth/jwt.ts: Token validation logic
- src/middleware/auth.ts: Authentication middleware
- src/__tests__/auth.test.ts: Test suite

## Testing
- All existing tests pass
- New tests added for auth flows"

✓ PR created: https://github.com/user/repo/pull/123"
```

**Total time: ~30 seconds**  
**Manual git commands needed: 0**

---

## Why This Works Better

### Traditional Approach (Manual Git)
```bash
git checkout -b feature/auth
# ... make changes ...
git add .
git commit -m "add auth"  # Generic message
git push -u origin feature/auth
gh pr create  # Type description manually
```
**Time: 5-10 minutes**

### Claude Code Approach (Custom Skills)
```bash
/branch auth
# ... make changes ...
/commit
/push
/create-pr
```
**Time: 2-3 minutes**  
**Setup: Create 4 custom skills**

### OpenCode Approach (Native)
```bash
"create a branch for auth"
# ... make changes ...
"commit my changes and create a PR"
```
**Time: 30 seconds**  
**Setup: None!**

---

## Advanced Git Workflows

### Amend Last Commit

```
You: "amend the last commit with these changes"

OpenCode:
git add .
git commit --amend --no-edit
✓ Amended
```

### Interactive Rebase

```
You: "rebase the last 3 commits interactively"

OpenCode:
git rebase -i HEAD~3
(opens editor for interactive rebase)
```

### Cherry Pick

```
You: "cherry pick commit abc123 from main"

OpenCode:
git cherry-pick abc123
✓ Applied commit abc123
```

### Stash Changes

```
You: "stash my changes"

OpenCode:
git stash push -m "WIP: authentication changes"
Saved working directory and index state
✓ Stashed
```

---

## Best Practices

### 1. Be Descriptive

**Good:**
```
"commit my changes to the authentication system"
```

**Better:**
```
"commit my JWT authentication changes with a conventional commit message"
```

### 2. Provide Context

**Good:**
```
"create a PR"
```

**Better:**
```
"create a PR for the authentication feature, emphasizing the security improvements"
```

### 3. Combine Operations

**Instead of:**
```
"commit my changes"
"push this"
"create a PR"
```

**Do:**
```
"commit my changes, push, and create a PR"
```

---

## Understanding Conventional Commits

OpenCode uses conventional commits format by default:

```
<type>(<scope>): <description>

<body>

<footer>
```

**Types:**
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation only
- `style:` - Formatting (no code change)
- `refactor:` - Code restructuring
- `test:` - Adding tests
- `chore:` - Maintenance tasks

**Examples:**
```
feat: add user authentication
feat(api): add JWT validation endpoint
fix: resolve token expiration bug
fix(auth): handle missing refresh token
docs: update authentication guide
test: add JWT validation tests
refactor(auth): simplify token generation
```

---

## Customizing Git Behavior

While OpenCode has native git support, you can still customize behavior with configuration.

### Example: Custom Commit Message Format

Create `.opencode/command/commit.md`:
```markdown
---
description: Commit with team-specific format
---

Analyze the changes and create a commit following our team format:

<type>(<ticket>): <description>

Where ticket is extracted from the branch name.

Example:
feat(JIRA-123): add user authentication
```

Now `/commit` uses your custom format, while natural language still uses the native approach.

---

## FAQ

### Do I need custom skills for git operations?

**No!** OpenCode understands git natively. Custom skills are only needed for team-specific requirements beyond standard git operations.

### Can I still create custom git skills?

**Yes**, but it's not recommended. OpenCode's native git support is more powerful than custom skills. Only create custom skills if you have very specific requirements.

### What about complex git operations?

OpenCode can handle complex git workflows through natural language:
- Rebasing
- Cherry-picking
- Stashing
- Branch management
- Conflict resolution

Just describe what you want to do.

### Does this work with GitLab/Bitbucket?

OpenCode works with any git repository. For creating PRs/MRs:
- GitHub: Uses `gh` CLI
- GitLab: Uses `glab` CLI
- Bitbucket: Uses `bb` CLI

Make sure the appropriate CLI tool is installed.

---

## Summary

### ✅ Do This:
```
"commit my changes"
"create a PR"
"push this"
```

### ❌ Not This:
```
Create .opencode/skill/commit/SKILL.md
Create .opencode/skill/push/SKILL.md
Create .opencode/skill/create-pr/SKILL.md
```

**OpenCode knows git. Just ask!**

---

## Next Steps

1. **Try it:** Make some changes and ask OpenCode to commit them
2. **Combine operations:** "commit and push my changes"
3. **Full workflow:** "commit my changes, push, and create a PR"
4. **Read more:** Check out [../examples/git-workflow-demo.md](../examples/git-workflow-demo.md)

---

**Remember:** The best git skill is no git skill! 🚀
