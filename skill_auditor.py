#!/usr/bin/env python3
"""
OpenCode Skill Auditor

Analyzes and audits OpenCode skills for quality, necessity, and compliance.
Checks both global (~/.config/opencode/skill/) and project-local (.opencode/skill/) skills.

Usage:
    python skill_auditor.py
    python skill_auditor.py --global-only
    python skill_auditor.py --project-only
    python skill_auditor.py --format json
    python skill_auditor.py --format markdown
    python skill_auditor.py --verbose
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from datetime import datetime

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False
    print("Warning: PyYAML not installed. Using basic YAML parsing.")


# Native OpenCode features that skills might duplicate
NATIVE_COMMANDS = {
    "tui_slash": [
        "/compact", "/connect", "/details", "/editor", "/exit", "/export",
        "/help", "/init", "/models", "/new", "/quit", "/redo", "/resume",
        "/sessions", "/share", "/summarize", "/themes", "/thinking", "/undo", "/unshare"
    ],
    "cli_commands": [
        "opencode", "opencode agent", "opencode attach", "opencode auth",
        "opencode github", "opencode mcp", "opencode models", "opencode run",
        "opencode serve", "opencode session", "opencode stats", "opencode export",
        "opencode import", "opencode web", "opencode acp", "opencode uninstall",
        "opencode upgrade"
    ],
    "git_workflows": [
        "commit", "branch", "push", "create-pr", "undo", "redo"
    ]
}


@dataclass
class SkillMetadata:
    """Represents skill metadata from frontmatter."""
    name: str = ""
    description: str = ""
    license: str = ""
    compatibility: str = ""
    audience: str = ""
    workflow: str = ""


@dataclass
class SkillScore:
    """Represents scoring results for a skill."""
    metadata_score: int = 0
    metadata_max: int = 35
    quality_score: int = 0
    quality_max: int = 35
    necessity_score: int = 0
    necessity_max: int = 30
    total_score: int = 0
    max_score: int = 100
    grade: str = "F"
    verdict: str = "UNKNOWN"
    priority: str = "LOW"


@dataclass
class SkillIssue:
    """Represents an issue found during audit."""
    severity: str  # critical, warning, info
    category: str  # metadata, quality, necessity, structure
    message: str
    recommendation: str = ""


@dataclass
class SkillReport:
    """Complete audit report for a single skill."""
    name: str
    location: str
    location_type: str  # global or project
    path: str
    metadata: SkillMetadata
    score: SkillScore
    issues: List[SkillIssue]
    content_analysis: Dict[str, Any]
    
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "location": self.location,
            "location_type": self.location_type,
            "path": self.path,
            "metadata": asdict(self.metadata),
            "score": asdict(self.score),
            "issues": [asdict(issue) for issue in self.issues],
            "content_analysis": self.content_analysis
        }


class SkillAuditor:
    """Main auditor class for analyzing OpenCode skills."""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.global_skills_dir = Path.home() / ".config" / "opencode" / "skill"
        self.project_skills_dir = Path(".opencode") / "skill"
        self.all_skills: Dict[str, SkillReport] = {}
        
    def discover_skills(self, global_only: bool = False, project_only: bool = False) -> Dict[str, Path]:
        """Discover all skills in both global and project locations."""
        skills = {}
        
        # Global skills
        if not project_only and self.global_skills_dir.exists():
            for skill_dir in self.global_skills_dir.iterdir():
                if skill_dir.is_dir():
                    skill_file = skill_dir / "SKILL.md"
                    if skill_file.exists():
                        skills[f"global:{skill_dir.name}"] = skill_file
                        if self.verbose:
                            print(f"Found global skill: {skill_dir.name}")
        
        # Project skills
        if not global_only and self.project_skills_dir.exists():
            for skill_dir in self.project_skills_dir.iterdir():
                if skill_dir.is_dir():
                    skill_file = skill_dir / "SKILL.md"
                    if skill_file.exists():
                        skills[f"project:{skill_dir.name}"] = skill_file
                        if self.verbose:
                            print(f"Found project skill: {skill_dir.name}")
        
        return skills
    
    def parse_frontmatter(self, content: str) -> Tuple[Dict, str]:
        """Parse YAML frontmatter from skill content."""
        if not content.startswith("---"):
            return {}, content
        
        parts = content.split("---", 2)
        if len(parts) < 3:
            return {}, content
        
        frontmatter_text = parts[1].strip()
        body = parts[2].strip()
        
        if YAML_AVAILABLE:
            try:
                frontmatter = yaml.safe_load(frontmatter_text) or {}
            except yaml.YAMLError:
                frontmatter = {}
        else:
            # Basic parsing for when PyYAML is not available
            frontmatter = self._basic_yaml_parse(frontmatter_text)
        
        return frontmatter, body
    
    def _basic_yaml_parse(self, text: str) -> Dict:
        """Basic YAML parsing without PyYAML."""
        result = {}
        current_key = None
        
        for line in text.split('\n'):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()
                
                if value:
                    result[key] = value
                else:
                    current_key = key
                    result[key] = {}
            elif current_key and line.startswith('-'):
                # Simple list handling
                if isinstance(result[current_key], dict):
                    result[current_key] = []
                if not isinstance(result[current_key], list):
                    result[current_key] = [result[current_key]]
                result[current_key].append(line[1:].strip())
        
        return result
    
    def validate_name(self, name: str) -> Tuple[bool, Optional[str]]:
        """Validate skill name according to OpenCode conventions."""
        if not name:
            return False, "Name is empty"
        
        if len(name) > 64:
            return False, f"Name too long ({len(name)} chars, max 64)"
        
        pattern = r'^[a-z0-9]+(-[a-z0-9]+)*$'
        if not re.match(pattern, name):
            return False, "Name must be lowercase alphanumeric with single hyphens"
        
        if name.startswith('-') or name.endswith('-'):
            return False, "Name cannot start or end with hyphen"
        
        if '--' in name:
            return False, "Name cannot contain consecutive hyphens"
        
        return True, None
    
    def check_native_duplication(self, skill_name: str, description: str) -> Optional[str]:
        """Check if skill duplicates native OpenCode functionality."""
        skill_lower = skill_name.lower()
        desc_lower = description.lower()
        
        for category, commands in NATIVE_COMMANDS.items():
            for command in commands:
                # Check if skill name matches command
                if skill_lower == command.lower() or skill_lower == command.lower().lstrip('/'):
                    return f"Duplicates native {category} command: {command}"
                
                # Check if description indicates native functionality
                if command.lower().lstrip('/') in desc_lower:
                    words = desc_lower.split()
                    if command.lower().lstrip('/') in words or command.lower() in words:
                        return f"Likely duplicates native {category} command: {command}"
        
        return None
    
    def analyze_content(self, body: str) -> Dict[str, Any]:
        """Analyze skill content for quality metrics."""
        analysis = {
            "line_count": len(body.split('\n')),
            "has_examples": False,
            "has_output_format": False,
            "has_actionable_instructions": False,
            "has_severity_levels": False,
            "has_when_to_use": False,
            "code_blocks": 0,
            "sections": [],
            "actionable_verbs": []
        }
        
        # Check for examples
        if 'example' in body.lower():
            analysis["has_examples"] = True
        
        # Check for output format
        if 'output' in body.lower() and 'format' in body.lower():
            analysis["has_output_format"] = True
        
        # Check for actionable instructions (verbs)
        actionable_patterns = [
            r'\b(check|verify|validate|ensure|create|add|implement|fix|remove|update|run|test)\b'
        ]
        for pattern in actionable_patterns:
            matches = re.findall(pattern, body, re.IGNORECASE)
            analysis["actionable_verbs"].extend(matches)
        
        analysis["has_actionable_instructions"] = len(analysis["actionable_verbs"]) >= 3
        
        # Check for severity levels (for complex skills)
        if re.search(r'(critical|high|medium|low|severity)', body, re.IGNORECASE):
            analysis["has_severity_levels"] = True
        
        # Check for when to use section
        if re.search(r'when to use|usage|use this', body, re.IGNORECASE):
            analysis["has_when_to_use"] = True
        
        # Count code blocks
        analysis["code_blocks"] = len(re.findall(r'```', body)) // 2
        
        # Extract sections
        for line in body.split('\n'):
            if line.startswith('## '):
                analysis["sections"].append(line[3:].strip())
        
        return analysis
    
    def calculate_metadata_score(self, metadata: SkillMetadata) -> Tuple[int, List[SkillIssue]]:
        """Calculate metadata completeness score."""
        score = 0
        issues = []
        
        # Required fields (25 points)
        if metadata.name:
            score += 15
        else:
            issues.append(SkillIssue(
                severity="critical",
                category="metadata",
                message="Missing required field: name",
                recommendation="Add 'name' field to frontmatter"
            ))
        
        if metadata.description:
            desc_len = len(metadata.description)
            if 1 <= desc_len <= 1024:
                score += 10
            else:
                issues.append(SkillIssue(
                    severity="warning",
                    category="metadata",
                    message=f"Description length {desc_len} chars (should be 1-1024)",
                    recommendation="Adjust description length"
                ))
        else:
            issues.append(SkillIssue(
                severity="critical",
                category="metadata",
                message="Missing required field: description",
                recommendation="Add 'description' field to frontmatter"
            ))
        
        # Optional fields (10 points)
        if metadata.license:
            score += 3
        else:
            issues.append(SkillIssue(
                severity="info",
                category="metadata",
                message="Missing optional field: license",
                recommendation="Consider adding 'license: MIT'"
            ))
        
        if metadata.compatibility:
            score += 3
        else:
            issues.append(SkillIssue(
                severity="info",
                category="metadata",
                message="Missing optional field: compatibility",
                recommendation="Consider adding 'compatibility: opencode'"
            ))
        
        if metadata.workflow:
            score += 4
        else:
            issues.append(SkillIssue(
                severity="warning",
                category="metadata",
                message="Missing metadata.workflow field",
                recommendation="Add workflow categorization (e.g., 'git-ops', 'security', 'deployment')"
            ))
        
        return score, issues
    
    def calculate_quality_score(self, content_analysis: Dict, body: str) -> Tuple[int, List[SkillIssue]]:
        """Calculate content quality score."""
        score = 0
        issues = []
        
        # Examples (10 points)
        if content_analysis["has_examples"]:
            score += 10
        else:
            issues.append(SkillIssue(
                severity="warning",
                category="quality",
                message="No examples section found",
                recommendation="Add concrete examples of skill usage"
            ))
        
        # Output format (8 points)
        if content_analysis["has_output_format"]:
            score += 8
        else:
            issues.append(SkillIssue(
                severity="warning",
                category="quality",
                message="No output format defined",
                recommendation="Add '## Output Format' section"
            ))
        
        # Actionable instructions (8 points)
        if content_analysis["has_actionable_instructions"]:
            score += 8
        else:
            issues.append(SkillIssue(
                severity="warning",
                category="quality",
                message="Instructions lack actionable verbs",
                recommendation="Use verbs like 'check', 'verify', 'create', 'implement'"
            ))
        
        # When to use (6 points)
        if content_analysis["has_when_to_use"]:
            score += 6
        else:
            issues.append(SkillIssue(
                severity="info",
                category="quality",
                message="No 'when to use' section",
                recommendation="Add guidance on appropriate usage contexts"
            ))
        
        # Code blocks (3 points)
        if content_analysis["code_blocks"] >= 2:
            score += 3
        elif content_analysis["code_blocks"] == 1:
            score += 1
            issues.append(SkillIssue(
                severity="info",
                category="quality",
                message="Only one code block found",
                recommendation="Add more code examples"
            ))
        else:
            issues.append(SkillIssue(
                severity="warning",
                category="quality",
                message="No code blocks found",
                recommendation="Add code examples or templates"
            ))
        
        return score, issues
    
    def calculate_necessity_score(self, skill_name: str, metadata: SkillMetadata, 
                                   all_skills: Dict[str, Path]) -> Tuple[int, List[SkillIssue]]:
        """Calculate necessity/value score."""
        score = 30  # Start with full score, deduct for issues
        issues = []
        
        # Check for native duplication (major penalty)
        duplication = self.check_native_duplication(skill_name, metadata.description)
        if duplication:
            score -= 20
            issues.append(SkillIssue(
                severity="critical",
                category="necessity",
                message=duplication,
                recommendation="Consider deleting - functionality is built into opencode"
            ))
        
        # Check for duplicate skills
        base_name = skill_name.lower().replace('-', '').replace('_', '')
        duplicates = []
        for key, path in all_skills.items():
            other_name = key.split(':')[1].lower().replace('-', '').replace('_', '')
            if other_name == base_name and key != f"global:{skill_name}" and key != f"project:{skill_name}":
                duplicates.append(key)
        
        if duplicates:
            score -= 15
            issues.append(SkillIssue(
                severity="critical",
                category="necessity",
                message=f"Duplicate skill found: {', '.join(duplicates)}",
                recommendation="Consolidate or delete duplicate skills"
            ))
        
        # Check description quality
        if metadata.description:
            if len(metadata.description) < 30:
                score -= 5
                issues.append(SkillIssue(
                    severity="warning",
                    category="necessity",
                    message="Description is too brief (< 30 chars)",
                    recommendation="Add more detail about what the skill does"
                ))
            
            vague_terms = ['stuff', 'things', 'various', 'some', 'etc']
            if any(term in metadata.description.lower() for term in vague_terms):
                score -= 5
                issues.append(SkillIssue(
                    severity="warning",
                    category="necessity",
                    message="Description contains vague terms",
                    recommendation="Be specific about functionality"
                ))
        
        return max(0, score), issues
    
    def determine_verdict(self, score: SkillScore, issues: List[SkillIssue]) -> Tuple[str, str]:
        """Determine final verdict and priority."""
        # Count issues by severity
        critical = sum(1 for i in issues if i.severity == "critical")
        warnings = sum(1 for i in issues if i.severity == "warning")
        
        # Determine verdict
        if score.total_score < 40 or critical > 0:
            verdict = "DELETE"
            priority = "Critical"
        elif critical == 0 and warnings >= 3:
            verdict = "UPGRADE"
            priority = "High"
        elif score.total_score < 60:
            verdict = "UPGRADE"
            priority = "Medium"
        elif score.total_score >= 80 and critical == 0 and warnings <= 1:
            verdict = "KEEP"
            priority = "Low"
        else:
            verdict = "UPGRADE"
            priority = "Medium"
        
        return verdict, priority
    
    def audit_skill(self, skill_key: str, skill_path: Path, all_skills: Dict[str, Path]) -> SkillReport:
        """Perform complete audit of a single skill."""
        location_type, skill_name = skill_key.split(':', 1)
        
        # Read skill file
        content = skill_path.read_text()
        frontmatter, body = self.parse_frontmatter(content)
        
        # Extract metadata
        metadata = SkillMetadata(
            name=frontmatter.get('name', skill_name),
            description=frontmatter.get('description', ''),
            license=frontmatter.get('license', ''),
            compatibility=frontmatter.get('compatibility', ''),
            audience=frontmatter.get('metadata', {}).get('audience', '') if isinstance(frontmatter.get('metadata'), dict) else '',
            workflow=frontmatter.get('metadata', {}).get('workflow', '') if isinstance(frontmatter.get('metadata'), dict) else ''
        )
        
        # Validate name
        issues = []
        name_valid, name_error = self.validate_name(metadata.name)
        if not name_valid:
            issues.append(SkillIssue(
                severity="critical",
                category="structure",
                message=f"Invalid skill name: {name_error}",
                recommendation="Rename skill to follow conventions"
            ))
        
        # Analyze content
        content_analysis = self.analyze_content(body)
        
        # Calculate scores
        metadata_score, metadata_issues = self.calculate_metadata_score(metadata)
        quality_score, quality_issues = self.calculate_quality_score(content_analysis, body)
        necessity_score, necessity_issues = self.calculate_necessity_score(
            skill_name, metadata, all_skills
        )
        
        # Combine all issues
        issues.extend(metadata_issues)
        issues.extend(quality_issues)
        issues.extend(necessity_issues)
        
        # Calculate total score
        total_score = metadata_score + quality_score + necessity_score
        
        # Determine grade
        if total_score >= 80:
            grade = "A"
        elif total_score >= 70:
            grade = "B"
        elif total_score >= 60:
            grade = "C"
        elif total_score >= 50:
            grade = "D"
        else:
            grade = "F"
        
        # Create score object
        score = SkillScore(
            metadata_score=metadata_score,
            quality_score=quality_score,
            necessity_score=necessity_score,
            total_score=total_score,
            grade=grade,
            verdict="",
            priority=""
        )
        
        # Determine verdict
        verdict, priority = self.determine_verdict(score, issues)
        score.verdict = verdict
        score.priority = priority
        
        return SkillReport(
            name=metadata.name or skill_name,
            location="global" if location_type == "global" else "project",
            location_type=location_type,
            path=str(skill_path),
            metadata=metadata,
            score=score,
            issues=issues,
            content_analysis=content_analysis
        )
    
    def audit_all(self, global_only: bool = False, project_only: bool = False) -> List[SkillReport]:
        """Audit all discovered skills."""
        skills = self.discover_skills(global_only, project_only)
        reports = []
        
        for skill_key, skill_path in skills.items():
            if self.verbose:
                print(f"\nAuditing: {skill_key}")
            
            report = self.audit_skill(skill_key, skill_path, skills)
            reports.append(report)
            self.all_skills[skill_key] = report
        
        return reports
    
    def print_table_report(self, reports: List[SkillReport]):
        """Print CLI table report."""
        # Header
        print("\n" + "="*100)
        print(f"{'Skill':<25} {'Location':<10} {'Score':<8} {'Grade':<8} {'Verdict':<12} {'Priority':<10}")
        print("="*100)
        
        # Sort by score descending
        sorted_reports = sorted(reports, key=lambda r: r.score.total_score, reverse=True)
        
        for report in sorted_reports:
            grade_color = {
                'A': '\033[92m',  # Green
                'B': '\033[94m',  # Blue
                'C': '\033[93m',  # Yellow
                'D': '\033[91m',  # Red
                'F': '\033[91m',  # Red
            }.get(report.score.grade, '')
            
            verdict_color = {
                'KEEP': '\033[92m',
                'UPGRADE': '\033[93m',
                'DELETE': '\033[91m',
            }.get(report.score.verdict, '')
            
            reset = '\033[0m'
            
            print(f"{report.name:<25} "
                  f"{report.location:<10} "
                  f"{report.score.total_score:<8} "
                  f"{grade_color}{report.score.grade:<8}{reset} "
                  f"{verdict_color}{report.score.verdict:<12}{reset} "
                  f"{report.score.priority:<10}")
        
        print("="*100)
        
        # Summary
        total = len(reports)
        keep = sum(1 for r in reports if r.score.verdict == "KEEP")
        upgrade = sum(1 for r in reports if r.score.verdict == "UPGRADE")
        delete = sum(1 for r in reports if r.score.verdict == "DELETE")
        
        print(f"\nSummary: {total} skills total")
        print(f"  ✅ KEEP: {keep}")
        print(f"  ⚠️  UPGRADE: {upgrade}")
        print(f"  ❌ DELETE: {delete}")
        
        # Critical issues
        critical_count = sum(len([i for i in r.issues if i.severity == "critical"]) for r in reports)
        if critical_count > 0:
            print(f"\n⚠️  {critical_count} critical issues found!")
    
    def print_detailed_report(self, reports: List[SkillReport]):
        """Print detailed report with all issues."""
        self.print_table_report(reports)
        
        print("\n" + "="*100)
        print("DETAILED REPORT")
        print("="*100)
        
        for report in sorted(reports, key=lambda r: r.score.total_score):
            print(f"\n{'='*80}")
            print(f"Skill: {report.name}")
            print(f"Location: {report.path}")
            print(f"Score: {report.score.total_score}/100 (Grade: {report.score.grade})")
            print(f"Verdict: {report.score.verdict} | Priority: {report.score.priority}")
            print(f"{'='*80}")
            
            if report.issues:
                print("\nIssues Found:")
                for issue in report.issues:
                    icon = {"critical": "❌", "warning": "⚠️", "info": "ℹ️"}.get(issue.severity, "•")
                    print(f"  {icon} [{issue.severity.upper()}] {issue.category}: {issue.message}")
                    if issue.recommendation:
                        print(f"      → {issue.recommendation}")
            else:
                print("\n✅ No issues found!")
            
            print(f"\nContent Analysis:")
            print(f"  Lines: {report.content_analysis['line_count']}")
            print(f"  Code blocks: {report.content_analysis['code_blocks']}")
            print(f"  Sections: {len(report.content_analysis['sections'])}")
            print(f"  Has examples: {report.content_analysis['has_examples']}")
            print(f"  Has output format: {report.content_analysis['has_output_format']}")
    
    def generate_json_report(self, reports: List[SkillReport]) -> str:
        """Generate JSON report."""
        data = {
            "generated_at": datetime.now().isoformat(),
            "summary": {
                "total_skills": len(reports),
                "keep": sum(1 for r in reports if r.score.verdict == "KEEP"),
                "upgrade": sum(1 for r in reports if r.score.verdict == "UPGRADE"),
                "delete": sum(1 for r in reports if r.score.verdict == "DELETE"),
                "critical_issues": sum(len([i for i in r.issues if i.severity == "critical"]) for r in reports),
                "warning_issues": sum(len([i for i in r.issues if i.severity == "warning"]) for r in reports),
            },
            "skills": [report.to_dict() for report in reports]
        }
        return json.dumps(data, indent=2)
    
    def generate_markdown_report(self, reports: List[SkillReport]) -> str:
        """Generate comprehensive markdown report."""
        lines = [
            "# OpenCode Skill Audit Report",
            f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "\n## Executive Summary",
            f"\n**Total Skills Audited:** {len(reports)}",
            f"\n| Verdict | Count | Percentage |",
            "|---------|-------|------------|",
        ]
        
        total = len(reports)
        for verdict in ["KEEP", "UPGRADE", "DELETE"]:
            count = sum(1 for r in reports if r.score.verdict == verdict)
            pct = (count / total * 100) if total > 0 else 0
            lines.append(f"| {verdict} | {count} | {pct:.1f}% |")
        
        critical_count = sum(len([i for i in r.issues if i.severity == "critical"]) for r in reports)
        lines.extend([
            f"\n**Critical Issues:** {critical_count}",
            "\n---",
            "\n## Detailed Skill Analysis",
        ])
        
        # Sort by score ascending (worst first)
        for report in sorted(reports, key=lambda r: r.score.total_score):
            lines.extend([
                f"\n### {report.name}",
                f"\n**Location:** `{report.path}`",
                f"\n**Type:** {report.location}",
                f"\n**Score:** {report.score.total_score}/100 (Grade: {report.score.grade})",
                f"\n**Verdict:** `{report.score.verdict}` | **Priority:** {report.score.priority}",
                "\n**Score Breakdown:**",
                f"- Metadata: {report.score.metadata_score}/{report.score.metadata_max}",
                f"- Quality: {report.score.quality_score}/{report.score.quality_max}",
                f"- Necessity: {report.score.necessity_score}/{report.score.necessity_max}",
            ])
            
            if report.issues:
                lines.extend(["\n**Issues:**"])
                for issue in report.issues:
                    emoji = {"critical": "🔴", "warning": "🟡", "info": "🔵"}.get(issue.severity, "⚪")
                    lines.append(f"\n{emoji} **[{issue.severity.upper()}]** {issue.category}")
                    lines.append(f"   - **Issue:** {issue.message}")
                    if issue.recommendation:
                        lines.append(f"   - **Recommendation:** {issue.recommendation}")
            
            lines.extend([
                "\n**Content Analysis:**",
                f"- Lines: {report.content_analysis['line_count']}",
                f"- Has examples: {'✅' if report.content_analysis['has_examples'] else '❌'}",
                f"- Has output format: {'✅' if report.content_analysis['has_output_format'] else '❌'}",
                f"- Has actionable instructions: {'✅' if report.content_analysis['has_actionable_instructions'] else '❌'}",
                f"- Code blocks: {report.content_analysis['code_blocks']}",
                "\n---",
            ])
        
        return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Audit OpenCode skills for quality, necessity, and compliance"
    )
    parser.add_argument(
        "--global-only",
        action="store_true",
        help="Only audit global skills (~/.config/opencode/skill/)"
    )
    parser.add_argument(
        "--project-only",
        action="store_true",
        help="Only audit project skills (./.opencode/skill/)"
    )
    parser.add_argument(
        "--format",
        choices=["table", "detailed", "json", "markdown"],
        default="table",
        help="Output format (default: table)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    parser.add_argument(
        "--output", "-o",
        help="Output file path (for json/markdown formats)"
    )
    
    args = parser.parse_args()
    
    # Create auditor
    auditor = SkillAuditor(verbose=args.verbose)
    
    # Run audit
    print("🔍 Auditing OpenCode skills...")
    reports = auditor.audit_all(args.global_only, args.project_only)
    
    if not reports:
        print("⚠️  No skills found!")
        return
    
    # Output results
    if args.format == "table":
        auditor.print_table_report(reports)
    elif args.format == "detailed":
        auditor.print_detailed_report(reports)
    elif args.format == "json":
        output = auditor.generate_json_report(reports)
        if args.output:
            Path(args.output).write_text(output)
            print(f"✅ JSON report saved to: {args.output}")
        else:
            print(output)
    elif args.format == "markdown":
        output = auditor.generate_markdown_report(reports)
        if args.output:
            Path(args.output).write_text(output)
            print(f"✅ Markdown report saved to: {args.output}")
        else:
            print(output)
    
    # Exit with error code if critical issues found
    critical_count = sum(len([i for i in r.issues if i.severity == "critical"]) for r in reports)
    if critical_count > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
