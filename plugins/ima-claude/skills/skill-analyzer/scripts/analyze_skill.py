#!/usr/bin/env python3
"""
Skill Analyzer - Automated validation against best practices.

Usage:
    python analyze_skill.py /path/to/skill-directory
    python analyze_skill.py /path/to/skill.skill  # .skill files are zips
"""

import sys
import re
import os
import zipfile
import tempfile
import shutil
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Issue:
    severity: str  # "critical", "warning", "info"
    category: str
    message: str
    suggestion: Optional[str] = None


@dataclass
class AnalysisResult:
    skill_name: str = ""
    skill_path: str = ""
    issues: list = field(default_factory=list)
    metrics: dict = field(default_factory=dict)
    
    def add(self, severity: str, category: str, message: str, suggestion: str = None):
        self.issues.append(Issue(severity, category, message, suggestion))
    
    @property
    def critical_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == "critical")
    
    @property
    def warning_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == "warning")


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Extract YAML frontmatter and body from SKILL.md content."""
    if not content.startswith("---"):
        return {}, content
    
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content
    
    frontmatter_text = parts[1].strip()
    body = parts[2].strip()
    
    # Simple YAML parsing (key: value)
    frontmatter = {}
    for line in frontmatter_text.split("\n"):
        if ":" in line:
            key, value = line.split(":", 1)
            frontmatter[key.strip()] = value.strip()
    
    return frontmatter, body


def check_frontmatter(frontmatter: dict, result: AnalysisResult):
    """Validate YAML frontmatter requirements."""
    
    # Name field
    if "name" not in frontmatter:
        result.add("critical", "frontmatter", "Missing required 'name' field")
    else:
        name = frontmatter["name"]
        result.skill_name = name
        
        if len(name) > 64:
            result.add("critical", "frontmatter", 
                      f"Name exceeds 64 characters ({len(name)} chars)",
                      "Shorten the skill name")
        
        if not re.match(r'^[a-z0-9-]+$', name):
            result.add("critical", "frontmatter",
                      "Name must use only lowercase letters, numbers, and hyphens",
                      f"Current name '{name}' contains invalid characters")
        
        reserved = ["anthropic", "claude"]
        for word in reserved:
            if word in name.lower():
                result.add("critical", "frontmatter",
                          f"Name contains reserved word '{word}'")
    
    # Description field
    if "description" not in frontmatter:
        result.add("critical", "frontmatter", "Missing required 'description' field")
    else:
        desc = frontmatter["description"]
        
        if not desc:
            result.add("critical", "frontmatter", "Description is empty")
        elif len(desc) > 1024:
            result.add("critical", "frontmatter",
                      f"Description exceeds 1024 characters ({len(desc)} chars)")
        
        if "<" in desc and ">" in desc:
            result.add("critical", "frontmatter",
                      "Description may contain XML tags",
                      "Remove any XML-like content from description")
        
        # Check for first/second person
        first_person = re.search(r'\bI\s+(can|will|am|help)\b', desc, re.IGNORECASE)
        second_person = re.search(r'\b(You|Your)\s+(can|will|should)\b', desc, re.IGNORECASE)
        
        if first_person:
            result.add("warning", "description",
                      "Description uses first person ('I can...', 'I will...')",
                      "Use third person: 'Extracts text from...' not 'I can extract...'")
        
        if second_person:
            result.add("warning", "description",
                      "Description uses second person ('You can...')",
                      "Use third person: 'Processes files...' not 'You can process...'")
        
        # Check for vague descriptions
        vague_patterns = [
            r'\bhelps?\s+with\b',
            r'\bprocesses?\s+data\b',
            r'\bdoes?\s+stuff\b',
            r'\bhandles?\s+things\b',
            r'^utils?$',
            r'^helper$',
            r'^tools?$',
        ]
        for pattern in vague_patterns:
            if re.search(pattern, desc, re.IGNORECASE):
                result.add("warning", "description",
                          f"Description may be too vague (matches: {pattern})",
                          "Be specific about what the skill does and when to use it")
                break
        
        # Check for trigger context
        trigger_indicators = ["use when", "trigger", "invoke", "activate", "for:", "(1)", "(2)"]
        has_trigger = any(ind.lower() in desc.lower() for ind in trigger_indicators)
        
        if not has_trigger and len(desc) < 100:
            result.add("info", "description",
                      "Description may lack trigger context",
                      "Include when the skill should be used, e.g., 'Use when working with...'")


def check_body(body: str, skill_path: Path, result: AnalysisResult):
    """Check SKILL.md body content."""
    
    lines = body.split("\n")
    line_count = len(lines)
    result.metrics["body_lines"] = line_count
    
    if line_count > 500:
        result.add("warning", "content",
                  f"SKILL.md body has {line_count} lines (target: <500)",
                  "Split large sections into separate reference files")
    elif line_count > 300:
        result.add("info", "content",
                  f"SKILL.md body has {line_count} lines - approaching limit")
    
    # Check for Windows paths
    windows_path = re.search(r'[a-zA-Z]:\\|\\[a-zA-Z]', body)
    if windows_path:
        result.add("warning", "content",
                  "Windows-style paths detected",
                  "Use forward slashes for cross-platform compatibility")
    
    # Check for time-sensitive content
    time_patterns = [
        r'\b(before|after)\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\b',
        r'\b(before|after)\s+\d{4}\b',
        r'\bas of\s+\d{4}\b',
        r'\buntil\s+(January|February|March|April|May|June|July|August|September|October|November|December)\b',
    ]
    for pattern in time_patterns:
        if re.search(pattern, body, re.IGNORECASE):
            result.add("warning", "content",
                      "Time-sensitive information detected",
                      "Move to 'old patterns' section or remove")
            break
    
    # Check for multiple equivalent options
    option_phrases = [
        r'you can use .+ or .+ or',
        r'options include:?\s*\n\s*[-*].*\n\s*[-*].*\n\s*[-*]',
        r'choose (from|between)',
    ]
    for pattern in option_phrases:
        if re.search(pattern, body, re.IGNORECASE):
            result.add("info", "content",
                      "Multiple equivalent options may be offered",
                      "Provide one default approach with escape hatches for edge cases")
            break
    
    # Check reference depth (look for references in references)
    ref_files = list(skill_path.glob("references/*.md")) + list(skill_path.glob("*.md"))
    for ref_file in ref_files:
        if ref_file.name == "SKILL.md":
            continue
        try:
            ref_content = ref_file.read_text()
            # Look for markdown links to other md files
            nested_refs = re.findall(r'\[.*?\]\((.*?\.md)\)', ref_content)
            if nested_refs:
                result.add("warning", "structure",
                          f"Nested references found in {ref_file.name}: {nested_refs}",
                          "Keep references one level deep from SKILL.md")
        except Exception:
            pass


def check_structure(skill_path: Path, result: AnalysisResult):
    """Check skill directory structure."""
    
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        result.add("critical", "structure", "SKILL.md not found at skill root")
        return
    
    # Check for unnecessary files
    unnecessary = ["README.md", "CHANGELOG.md", "INSTALLATION_GUIDE.md", 
                   "QUICK_REFERENCE.md", "CONTRIBUTING.md"]
    for filename in unnecessary:
        if (skill_path / filename).exists():
            result.add("warning", "structure",
                      f"Unnecessary file found: {filename}",
                      "Skills should only contain SKILL.md + essential resources")
    
    # Check reference files for TOC if large
    refs_dir = skill_path / "references"
    if refs_dir.exists():
        for ref_file in refs_dir.glob("*.md"):
            try:
                content = ref_file.read_text()
                lines = len(content.split("\n"))
                if lines > 100:
                    # Check for TOC indicators
                    has_toc = any(ind in content.lower() for ind in 
                                 ["## contents", "## table of contents", "- ["])
                    if not has_toc:
                        result.add("info", "structure",
                                  f"{ref_file.name} has {lines} lines without a table of contents",
                                  "Add a table of contents for files >100 lines")
            except Exception:
                pass
    
    # Count scripts
    scripts_dir = skill_path / "scripts"
    if scripts_dir.exists():
        scripts = list(scripts_dir.glob("*.py")) + list(scripts_dir.glob("*.sh"))
        result.metrics["script_count"] = len(scripts)


def check_scripts(skill_path: Path, result: AnalysisResult):
    """Check script quality (if scripts exist)."""
    
    scripts_dir = skill_path / "scripts"
    if not scripts_dir.exists():
        return
    
    for script in scripts_dir.glob("*.py"):
        try:
            content = script.read_text()
            
            # Check for magic numbers without explanation
            magic_numbers = re.findall(r'=\s*(\d{2,})\s*(?:#|$|\n)', content)
            for num in magic_numbers:
                # Check if there's a comment nearby
                if f"# {num}" not in content and f"#{num}" not in content:
                    result.add("info", "scripts",
                              f"Potential magic number '{num}' in {script.name}",
                              "Document why this value was chosen")
            
            # Check for bare exception handling (punting)
            if re.search(r'except:\s*\n\s*(pass|raise)', content):
                result.add("warning", "scripts",
                          f"Bare exception handling in {script.name}",
                          "Handle errors explicitly rather than punting to Claude")
                          
        except Exception:
            pass


def format_report(result: AnalysisResult) -> str:
    """Format analysis results as a readable report."""
    
    # Determine overall status
    if result.critical_count > 0:
        status = "❌ Major Issues"
    elif result.warning_count > 0:
        status = "⚠️  Needs Work"
    else:
        status = "✅ Pass"
    
    lines = [
        f"# Skill Analysis: {result.skill_name or 'Unknown'}",
        "",
        "## Summary",
        f"- **Status**: {status}",
        f"- **Path**: {result.skill_path}",
        f"- **Body lines**: {result.metrics.get('body_lines', 'N/A')} (target: <500)",
        f"- **Critical issues**: {result.critical_count}",
        f"- **Warnings**: {result.warning_count}",
        "",
    ]
    
    # Group issues by severity
    critical = [i for i in result.issues if i.severity == "critical"]
    warnings = [i for i in result.issues if i.severity == "warning"]
    info = [i for i in result.issues if i.severity == "info"]
    
    if critical:
        lines.append("## ❌ Critical Issues (must fix)")
        lines.append("")
        for issue in critical:
            lines.append(f"- **[{issue.category}]** {issue.message}")
            if issue.suggestion:
                lines.append(f"  - *Suggestion*: {issue.suggestion}")
        lines.append("")
    
    if warnings:
        lines.append("## ⚠️  Warnings")
        lines.append("")
        for issue in warnings:
            lines.append(f"- **[{issue.category}]** {issue.message}")
            if issue.suggestion:
                lines.append(f"  - *Suggestion*: {issue.suggestion}")
        lines.append("")
    
    if info:
        lines.append("## ℹ️  Suggestions")
        lines.append("")
        for issue in info:
            lines.append(f"- **[{issue.category}]** {issue.message}")
            if issue.suggestion:
                lines.append(f"  - *Suggestion*: {issue.suggestion}")
        lines.append("")
    
    if not result.issues:
        lines.append("## ✅ No issues found")
        lines.append("")
        lines.append("The skill follows best practices. Consider testing with all target models.")
        lines.append("")
    
    return "\n".join(lines)


def analyze_skill(path: str) -> AnalysisResult:
    """Main analysis function."""
    
    result = AnalysisResult()
    skill_path = Path(path)
    
    # Handle .skill files (zip archives)
    temp_dir = None
    if skill_path.suffix == ".skill" and zipfile.is_zipfile(skill_path):
        temp_dir = tempfile.mkdtemp()
        with zipfile.ZipFile(skill_path, 'r') as zf:
            zf.extractall(temp_dir)
        # Find the actual skill directory inside
        contents = list(Path(temp_dir).iterdir())
        if len(contents) == 1 and contents[0].is_dir():
            skill_path = contents[0]
        else:
            skill_path = Path(temp_dir)
    
    result.skill_path = str(skill_path)
    
    try:
        skill_md = skill_path / "SKILL.md"
        if not skill_md.exists():
            result.add("critical", "structure", "SKILL.md not found")
            return result
        
        content = skill_md.read_text()
        frontmatter, body = parse_frontmatter(content)
        
        check_frontmatter(frontmatter, result)
        check_body(body, skill_path, result)
        check_structure(skill_path, result)
        check_scripts(skill_path, result)
        
    finally:
        if temp_dir:
            shutil.rmtree(temp_dir, ignore_errors=True)
    
    return result


def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze_skill.py /path/to/skill-directory")
        print("       python analyze_skill.py /path/to/skill.skill")
        sys.exit(1)
    
    path = sys.argv[1]
    
    if not os.path.exists(path):
        print(f"Error: Path does not exist: {path}")
        sys.exit(1)
    
    result = analyze_skill(path)
    print(format_report(result))
    
    # Exit with error code if critical issues
    sys.exit(1 if result.critical_count > 0 else 0)


if __name__ == "__main__":
    main()
