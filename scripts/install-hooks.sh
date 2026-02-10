#!/bin/bash
#
# Install pre-commit hooks for OpenCode skill validation
#
# Usage:
#   ./scripts/install-hooks.sh
#

set -e

echo "🔧 Installing OpenCode skill validation hooks..."
echo ""

# Check if we're in a git repo
if [ ! -d ".git" ]; then
    echo "❌ Error: Not a git repository"
    echo "Run this script from the root of your OpenCode.Personal directory"
    exit 1
fi

# Create hooks directory if it doesn't exist
mkdir -p .git/hooks

# Copy pre-commit hook
echo "📋 Installing pre-commit hook..."
cp scripts/validate-skills.sh .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit

echo "✅ Pre-commit hook installed successfully!"
echo ""

# Verify installation
if [ -f ".git/hooks/pre-commit" ]; then
    echo "✓ Hook location: .git/hooks/pre-commit"
    echo "✓ Hook is executable"
    echo ""
    echo "The hook will now run automatically before every commit to:"
    echo "  • Validate all skills meet quality standards"
    echo "  • Check for duplicate or redundant skills"
    echo "  • Ensure no critical issues exist"
    echo "  • Verify new skills score above 60/100"
    echo ""
    echo "To skip validation (not recommended):"
    echo "  git commit --no-verify"
    echo ""
    echo "To test the hook manually:"
    echo "  .git/hooks/pre-commit"
    echo ""
    echo -e "\033[32m✅ Installation complete!\033[0m"
else
    echo "❌ Installation failed"
    exit 1
fi
