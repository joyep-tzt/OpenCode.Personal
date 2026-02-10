#!/bin/bash
#
# CI/CD validation script for GitHub Actions
# 
# This script runs the skill auditor in CI/CD pipelines
# to ensure skill quality standards are maintained.
#
# Usage:
#   ./scripts/ci-validate.sh
#
# Environment variables:
#   FAIL_ON_DELETE=true        # Fail if skills marked for deletion (default: true)
#   FAIL_ON_LOW_SCORE=true     # Fail if skills score below 60 (default: true)
#   MIN_SCORE=60               # Minimum acceptable score (default: 60)

set -e

echo "🔍 OpenCode Skill CI Validation"
echo "================================"
echo ""

# Configuration
FAIL_ON_DELETE=${FAIL_ON_DELETE:-true}
FAIL_ON_LOW_SCORE=${FAIL_ON_LOW_SCORE:-true}
MIN_SCORE=${MIN_SCORE:-60}

echo "Configuration:"
echo "  Fail on DELETE: $FAIL_ON_DELETE"
echo "  Fail on low score: $FAIL_ON_LOW_SCORE"
echo "  Minimum score: $MIN_SCORE"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is required"
    exit 1
fi

# Check if skill_auditor.py exists
if [ ! -f "skill_auditor.py" ]; then
    echo "❌ Error: skill_auditor.py not found"
    exit 1
fi

# Run auditor
echo "Running skill auditor..."
python3 skill_auditor.py --format json -o /tmp/skill-audit-ci.json

if [ $? -ne 0 ]; then
    echo "❌ Skill auditor failed to run"
    exit 1
fi

# Check if jq is available
if ! command -v jq &> /dev/null; then
    echo "⚠️  Warning: jq not installed, using basic validation"
    echo "   Install jq for better validation: https://stedolan.github.io/jq/"
    echo ""
fi

# Parse results
if command -v jq &> /dev/null; then
    echo "Analyzing results..."
    echo ""
    
    # Get summary
    TOTAL=$(jq '.summary.total_skills' /tmp/skill-audit-ci.json)
    KEEP=$(jq '.summary.keep' /tmp/skill-audit-ci.json)
    UPGRADE=$(jq '.summary.upgrade' /tmp/skill-audit-ci.json)
    DELETE=$(jq '.summary.delete' /tmp/skill-audit-ci.json)
    CRITICAL=$(jq '.summary.critical_issues' /tmp/skill-audit-ci.json)
    WARNINGS=$(jq '.summary.warning_issues' /tmp/skill-audit-ci.json)
    
    # Calculate average score
    AVG_SCORE=$(jq '.skills | map(.score.total_score) | add / length' /tmp/skill-audit-ci.json)
    
    echo "📊 Summary"
    echo "========="
    echo "Total skills:     $TOTAL"
    echo "Keep:             $KEEP"
    echo "Upgrade:          $UPGRADE"
    echo "Delete:           $DELETE"
    echo "Critical issues:  $CRITICAL"
    echo "Warnings:         $WARNINGS"
    echo "Average score:    $(printf "%.1f" $AVG_SCORE)/100"
    echo ""
    
    # Check for DELETE verdicts
    if [ "$DELETE" -gt 0 ]; then
        echo "❌ Found $DELETE skill(s) marked for deletion:"
        jq -r '.skills | map(select(.score.verdict == "DELETE")) | .[] | "  - \(.name) (\(.score.total_score)/100)"' /tmp/skill-audit-ci.json
        echo ""
        
        if [ "$FAIL_ON_DELETE" == "true" ]; then
            echo "❌ FAIL: Skills marked for deletion found"
            exit 1
        fi
    fi
    
    # Check for low scores
    LOW_SCORE_COUNT=$(jq --arg min "$MIN_SCORE" '.skills | map(select(.score.total_score < ($min | tonumber))) | length' /tmp/skill-audit-ci.json)
    
    if [ "$LOW_SCORE_COUNT" -gt 0 ]; then
        echo "⚠️  Found $LOW_SCORE_COUNT skill(s) with score below $MIN_SCORE:"
        jq -r --arg min "$MIN_SCORE" '.skills | map(select(.score.total_score < ($min | tonumber))) | .[] | "  - \(.name): \(.score.total_score)/100"' /tmp/skill-audit-ci.json
        echo ""
        
        if [ "$FAIL_ON_LOW_SCORE" == "true" ]; then
            echo "❌ FAIL: Skills with low scores found"
            exit 1
        fi
    fi
    
    # Check for critical issues
    if [ "$CRITICAL" -gt 0 ]; then
        echo "❌ Found $CRITICAL critical issue(s)"
        echo ""
        
        # Show skills with critical issues
        echo "Skills with critical issues:"
        jq -r '.skills | map(select(any(.issues[]; .severity == "critical"))) | .[] | "  - \(.name)"' /tmp/skill-audit-ci.json
        echo ""
        
        echo "❌ FAIL: Critical issues found"
        exit 1
    fi
    
    # Check warnings
    if [ "$WARNINGS" -gt 0 ]; then
        echo "⚠️  Found $WARNINGS warning(s) - review recommended"
        echo ""
    fi
    
    # Grade distribution
    echo "📈 Grade Distribution"
    echo "===================="
    GRADE_A=$(jq '.skills | map(select(.score.grade == "A")) | length' /tmp/skill-audit-ci.json)
    GRADE_B=$(jq '.skills | map(select(.score.grade == "B")) | length' /tmp/skill-audit-ci.json)
    GRADE_C=$(jq '.skills | map(select(.score.grade == "C")) | length' /tmp/skill-audit-ci.json)
    GRADE_D=$(jq '.skills | map(select(.score.grade == "D")) | length' /tmp/skill-audit-ci.json)
    GRADE_F=$(jq '.skills | map(select(.score.grade == "F")) | length' /tmp/skill-audit-ci.json)
    
    echo "Grade A: $GRADE_A"
    echo "Grade B: $GRADE_B"
    echo "Grade C: $GRADE_C"
    echo "Grade D: $GRADE_D"
    echo "Grade F: $GRADE_F"
    echo ""
    
    # Top skills
    echo "🏆 Top Skills"
    echo "============"
    jq -r '.skills | sort_by(.score.total_score) | reverse | .[0:3] | .[] | "  \(.score.total_score)/100 - \(.name)"' /tmp/skill-audit-ci.json
    echo ""
    
else
    # Basic validation without jq
    if [ ! -s /tmp/skill-audit-ci.json ]; then
        echo "❌ Validation failed - no output generated"
        exit 1
    fi
    
    echo "✅ Basic validation passed"
    echo ""
fi

# Cleanup
rm -f /tmp/skill-audit-ci.json

echo "✅ CI Validation Complete"
echo ""
echo "All skills meet quality standards!"

exit 0
