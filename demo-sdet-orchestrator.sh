#!/bin/bash
#
# Quick Demo Script for SDET Orchestrator System
# Run this to demonstrate the system capabilities

echo "🎯 SDET Orchestrator System Demo"
echo "================================="
echo ""

# Check if we're in the right directory
if [ ! -f "skill_auditor.py" ]; then
    echo "❌ Error: Please run from OpenCode.Personal directory"
    exit 1
fi

echo "✅ Environment check passed"
echo ""

# Show current skills
echo "📊 Current Skills Registry"
echo "--------------------------"
python3 skill_auditor.py --format table 2>&1 | head -15
echo ""

# Show SDET Orchestrator components
echo "🤖 SDET Orchestrator Components"
echo "--------------------------------"
echo "✓ Agent: sdet-orchestrator"
ls -la .opencode/agent/sdet-orchestrator/
echo ""

echo "✓ Skills:"
ls -la .opencode/skill/stack-detective/
ls -la .opencode/skill/sdet-core-analyzer/
ls -la .opencode/skill/testing-patterns-enhancer/
echo ""

echo "📖 Documentation"
echo "----------------"
echo "✓ SDET_ORCHESTRATOR_README.md"
echo "✓ SKILL_REGISTRY.md (updated)"
echo ""

echo "🚀 Ready to Use!"
echo "----------------"
echo ""
echo "To analyze a project:"
echo "  1. Navigate to target project"
echo "  2. Run: /agent sdet-orchestrator analyze"
echo "  3. View: sdet-analysis-report.md"
echo ""
echo "Example target: https://github.com/Realtyka/playwright-qa-tech-lead-project"
echo ""
echo "✨ Wave 1 Implementation Complete!"
