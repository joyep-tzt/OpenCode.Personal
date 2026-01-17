#!/bin/bash
# Install OpenCode Skills: Copy skills, agents, and commands to user's OpenCode config

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Detect script location
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_DIR="$SCRIPT_DIR/.opencode"

# Default target directory
DEFAULT_TARGET="$HOME/.config/opencode"

echo "═══════════════════════════════════════════════════════"
echo "🚀 OpenCode Skills Installer"
echo "═══════════════════════════════════════════════════════"
echo ""

# Check if source directory exists
if [ ! -d "$SOURCE_DIR" ]; then
    echo -e "${RED}✗ Error: Source directory not found: $SOURCE_DIR${NC}"
    echo "  Make sure you're running this script from the opencode directory"
    exit 1
fi

echo -e "${BLUE}📂 Source directory: $SOURCE_DIR${NC}"
echo ""

# Ask user for target directory
echo -e "${YELLOW}Where do you want to install OpenCode skills?${NC}"
echo "  1. $HOME/.config/opencode (Recommended)"
echo "  2. $HOME/.opencode"
echo "  3. Custom location"
echo ""
read -p "Enter choice [1-3] (default: 1): " choice
choice=${choice:-1}

case $choice in
    1)
        TARGET_DIR="$HOME/.config/opencode"
        ;;
    2)
        TARGET_DIR="$HOME/.opencode"
        ;;
    3)
        read -p "Enter custom path: " custom_path
        TARGET_DIR="${custom_path/#\~/$HOME}"  # Expand ~ to $HOME
        ;;
    *)
        echo -e "${RED}✗ Invalid choice. Using default: $DEFAULT_TARGET${NC}"
        TARGET_DIR="$DEFAULT_TARGET"
        ;;
esac

echo ""
echo -e "${BLUE}📍 Target directory: $TARGET_DIR${NC}"
echo ""

# Create target directories
echo -e "${YELLOW}Creating directories...${NC}"
mkdir -p "$TARGET_DIR/skill"
mkdir -p "$TARGET_DIR/agent"
mkdir -p "$TARGET_DIR/command"
echo -e "${GREEN}✓ Directories created${NC}"
echo ""

# Function to count files
count_files() {
    local dir=$1
    local pattern=$2
    find "$dir" -name "$pattern" 2>/dev/null | wc -l
}

# Check what will be copied
SKILL_COUNT=$(count_files "$SOURCE_DIR/skill" "SKILL.md")
AGENT_COUNT=$(count_files "$SOURCE_DIR/agent" "*.md")
COMMAND_COUNT=$(count_files "$SOURCE_DIR/command" "*.md")

echo "═══════════════════════════════════════════════════════"
echo "📋 Installation Summary"
echo "═══════════════════════════════════════════════════════"
echo ""
echo -e "${BLUE}Skills to install:${NC} $SKILL_COUNT"
if [ -d "$SOURCE_DIR/skill" ]; then
    for skill_dir in "$SOURCE_DIR/skill"/*; do
        if [ -d "$skill_dir" ] && [ -f "$skill_dir/SKILL.md" ]; then
            skill_name=$(basename "$skill_dir")
            echo "  • $skill_name"
        fi
    done
fi
echo ""

echo -e "${BLUE}Agents to install:${NC} $AGENT_COUNT"
if [ -d "$SOURCE_DIR/agent" ]; then
    for agent_file in "$SOURCE_DIR/agent"/*.md; do
        if [ -f "$agent_file" ]; then
            agent_name=$(basename "$agent_file" .md)
            echo "  • $agent_name"
        fi
    done
fi
echo ""

echo -e "${BLUE}Commands to install:${NC} $COMMAND_COUNT"
if [ -d "$SOURCE_DIR/command" ]; then
    for command_file in "$SOURCE_DIR/command"/*.md; do
        if [ -f "$command_file" ]; then
            command_name=$(basename "$command_file" .md)
            echo "  • $command_name"
        fi
    done
fi
echo ""

# Ask for confirmation
echo -e "${YELLOW}⚠️  This will copy all files to: $TARGET_DIR${NC}"
echo -e "${YELLOW}   Existing files will be overwritten.${NC}"
echo ""
read -p "Continue with installation? [y/N]: " confirm
confirm=${confirm:-n}

if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
    echo ""
    echo -e "${YELLOW}Installation cancelled.${NC}"
    exit 0
fi

echo ""
echo "═══════════════════════════════════════════════════════"
echo "🔄 Installing..."
echo "═══════════════════════════════════════════════════════"
echo ""

# Copy skills
echo -e "${BLUE}📦 Copying skills...${NC}"
if [ -d "$SOURCE_DIR/skill" ]; then
    for skill_dir in "$SOURCE_DIR/skill"/*; do
        if [ -d "$skill_dir" ]; then
            skill_name=$(basename "$skill_dir")
            cp -r "$skill_dir" "$TARGET_DIR/skill/"
            echo -e "${GREEN}  ✓ $skill_name${NC}"
        fi
    done
else
    echo -e "${YELLOW}  ⚠ No skills directory found${NC}"
fi
echo ""

# Copy agents
echo -e "${BLUE}📦 Copying agents...${NC}"
if [ -d "$SOURCE_DIR/agent" ]; then
    cp "$SOURCE_DIR/agent"/*.md "$TARGET_DIR/agent/" 2>/dev/null || true
    for agent_file in "$SOURCE_DIR/agent"/*.md; do
        if [ -f "$agent_file" ]; then
            agent_name=$(basename "$agent_file" .md)
            echo -e "${GREEN}  ✓ $agent_name${NC}"
        fi
    done
else
    echo -e "${YELLOW}  ⚠ No agents directory found${NC}"
fi
echo ""

# Copy commands
echo -e "${BLUE}📦 Copying commands...${NC}"
if [ -d "$SOURCE_DIR/command" ]; then
    cp "$SOURCE_DIR/command"/*.md "$TARGET_DIR/command/" 2>/dev/null || true
    for command_file in "$SOURCE_DIR/command"/*.md; do
        if [ -f "$command_file" ]; then
            command_name=$(basename "$command_file" .md)
            echo -e "${GREEN}  ✓ $command_name${NC}"
        fi
    done
else
    echo -e "${YELLOW}  ⚠ No commands directory found${NC}"
fi
echo ""

# Verification
echo "═══════════════════════════════════════════════════════"
echo "✅ Installation Complete!"
echo "═══════════════════════════════════════════════════════"
echo ""

# Count installed files
INSTALLED_SKILLS=$(count_files "$TARGET_DIR/skill" "SKILL.md")
INSTALLED_AGENTS=$(count_files "$TARGET_DIR/agent" "*.md")
INSTALLED_COMMANDS=$(count_files "$TARGET_DIR/command" "*.md")

echo -e "${GREEN}📊 Installation Results:${NC}"
echo "  • Skills installed:   $INSTALLED_SKILLS"
echo "  • Agents installed:   $INSTALLED_AGENTS"
echo "  • Commands installed: $INSTALLED_COMMANDS"
echo ""
echo -e "${BLUE}📍 Installed to: $TARGET_DIR${NC}"
echo ""

# Next steps
echo "═══════════════════════════════════════════════════════"
echo "🎯 Next Steps"
echo "═══════════════════════════════════════════════════════"
echo ""
echo "1. Restart OpenCode (if already running)"
echo "2. Type /help to see available commands"
echo "3. Type @ to see available agents"
echo "4. Test a skill: /team-review"
echo "5. Try natural language: \"create a branch for my feature\""
echo ""
echo -e "${BLUE}📖 For verification, run:${NC}"
echo "   ./VERIFICATION-GUIDE.sh"
echo ""
echo "═══════════════════════════════════════════════════════"
echo ""
echo -e "${GREEN}🎉 Happy coding with OpenCode!${NC}"
echo ""
