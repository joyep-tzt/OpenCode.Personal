#!/bin/bash
#
# Pre-commit hook for OpenCode skill validation
# 
# This hook runs the skill auditor before every commit to ensure
# skill quality standards are maintained.
#
# Installation:
#   cp scripts/validate-skills.sh .git/hooks/pre-commit
#   chmod +x .git/hooks/pre-commit
#
# Or use the install script:
#   ./scripts/install-hooks.sh

set -e

echo "🔍 Running OpenCode skill validation..."
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if skill_auditor.py exists
if [ ! -f "skill_auditor.py" ]; then
    echo -e "${RED}❌ Error: skill_auditor.py not found${NC}"
    echo "Make sure you're in the OpenCode.Personal directory"
    exit 1
fi

# Run the auditor
python3 skill_auditor.py --format json -o /tmp/skill-audit-precommit.json

# Check exit code
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Skill validation failed!${NC}"
    echo ""
    echo "Critical issues found. Please fix them before committing."
    echo ""
    echo "Run the following to see details:"
    echo "  python3 skill_auditor.py --format detailed"
    echo ""
    exit 1
fi

# Parse results to check for DELETE verdicts or low scores
if command -v jq &> /dev/null; then
    # Count skills with DELETE verdict
    DELETE_COUNT=$(jq '.skills | map(select(.score.verdict == "DELETE")) | length' /tmp/skill-audit-precommit.json)
    
    # Count skills with score < 60
    LOW_SCORE_COUNT=$(jq '.skills | map(select(.score.total_score < 60)) | length' /tmp/skill-audit-precommit.json)
    
    # Count critical issues
    CRITICAL_COUNT=$(jq '.summary.critical_issues' /tmp/skill-audit-precommit.json)
    
    if [ "$DELETE_COUNT" -gt 0 ]; then
        echo -e "${RED}❌ Found $DELETE_COUNT skill(s) marked for deletion${NC}"
        echo ""
        echo "Skills marked for DELETE:"
        jq -r '.skills | map(select(.score.verdict == "DELETE")) | .[].name' /tmp/skill-audit-precommit.json | while read skill; do
            echo "  - $skill"
        done
        echo ""
        echo "Please remove these skills or fix the issues."
        echo ""
        exit 1
    fi
    
    if [ "$LOW_SCORE_COUNT" -gt 0 ]; then
        echo -e "${YELLOW}⚠️  Found $LOW_SCORE_COUNT skill(s) with score < 60${NC}"
        echo ""
        echo "Low scoring skills:"
        jq -r '.skills | map(select(.score.total_score < 60)) | .[] | "  - \(.name) (\(.score.total_score)/100)"' /tmp/skill-audit-precommit.json
        echo ""
        echo -e "${YELLOW}Commit blocked. Please improve these skills.${NC}"
        echo ""
        echo "Run the following to see details:"
        echo "  python3 skill_auditor.py --format detailed"
        echo ""
        exit 1
    fi
    
    if [ "$CRITICAL_COUNT" -gt 0 ]; then
        echo -e "${RED}❌ Found $CRITICAL_COUNT critical issue(s)${NC}"
        echo ""
        echo "Run the following to see details:"
        echo "  python3 skill_auditor.py --format detailed"
        echo ""
        exit 1
    fi
    
    # Get summary stats
    TOTAL=$(jq '.summary.total_skills' /tmp/skill-audit-precommit.json)
    KEEP=$(jq '.summary.keep' /tmp/skill-audit-precommit.json)
    AVG_SCORE=$(jq '.skills | map(.score.total_score) | add / length' /tmp/skill-audit-precommit.json)
    
    echo -e "${GREEN}✅ All skills passed validation!${NC}"
    echo ""
    echo "Summary:"
    echo "  Total skills: $TOTAL"
    echo "  Skills to keep: $KEEP"
    echo "  Average score: $(printf "%.0f" $AVG_SCORE)/100"
    echo ""
else
    echo -e "${YELLOW}⚠️  jq not installed. Basic validation only.${NC}"
    echo -e "${GREEN}✅ No critical issues found.${NC}"
    echo ""
fi

# Check for new skills being added
if git diff --cached --name-only | grep -q "SKILL.md"; then
    echo "📝 New or modified skills detected"
    echo ""
    
    # List modified skills
    git diff --cached --name-only | grep "SKILL.md" | while read file; do
        skill_name=$(basename $(dirname "$file"))
        echo "  - $skill_name"
    done
    echo ""
    
    # Run detailed check on modified skills
    echo "Running detailed validation on modified skills..."
    git diff --cached --name-only | grep "SKILL.md" | while read file; do
        if [ -f "$file" ]; then
            skill_name=$(basename $(dirname "$file"))
            echo ""
            echo "Checking: $skill_name"
            
            # Extract score from JSON for this specific skill
            if command -v jq &> /dev/null; then
                SCORE=$(jq -r --arg name "$skill_name" '.skills | map(select(.name == $name)) | .[0].score.total_score' /tmp/skill-audit-precommit.json)
                GRADE=$(jq -r --arg name "$skill_name" '.skills | map(select(.name == $name)) | .[0].score.grade' /tmp/skill-audit-precommit.json)
                VERDICT=$(jq -r --arg name "$skill_name" '.skills | map(select(.name == $name)) | .[0].score.verdict' /tmp/skill-audit-precommit.json)
                
                if [ "$SCORE" != "null" ]; then
                    echo "  Score: $SCORE/100 (Grade $GRADE) - $VERDICT"
                    
                    if [ "$VERDICT" == "DELETE" ]; then
                        echo -e "  ${RED}❌ This skill is marked for deletion${NC}"
                        exit 1
                    elif [ "$SCORE" -lt 60 ]; then
                        echo -e "  ${YELLOW}⚠️  Score below 60 - needs improvement${NC}"
                        exit 1
                    elif [ "$SCORE" -lt 80 ]; then
                        echo -e "  ${YELLOW}⚠️  Score below 80 - consider improvements${NC}"
                    fi
                fi
            fi
        fi
    done
    
    if [ $? -ne 0 ]; then
        exit 1
    fi
    
    echo ""
    echo -e "${GREEN}✅ Modified skills validation passed${NC}"
    echo ""
fi

# Cleanup
rm -f /tmp/skill-audit-precommit.json

echo -e "${GREEN}✅ Pre-commit validation complete. Proceeding with commit...${NC}"
echo ""

exit 0
