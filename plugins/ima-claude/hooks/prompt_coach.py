#!/usr/bin/env python3
"""
UserPromptSubmit hook: Evaluate prompts with Haiku for team standards.
Provides feedback inline when valuable, stays silent otherwise.

Requirements:
  ANTHROPIC_API_KEY env var (same key used for Claude Code)
  pip install anthropic

Environment variables:
  PROMPT_COACH_ENABLED=true  - Enable evaluation
  PROMPT_COACH_LOG=true      - Log prompts + feedback to ~/.claude/prompt_coach.log
"""
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Only run if enabled
if os.environ.get("PROMPT_COACH_ENABLED", "").lower() != "true":
    sys.exit(0)

# Common skip patterns (case-insensitive)
SKIP_PATTERNS = {
    "yes", "no", "y", "n", "ok", "okay", "continue", "proceed",
    "do it", "looks good", "go ahead", "sure", "thanks", "thank you",
    "got it", "understood", "perfect", "great", "good", "nice",
    "yep", "nope", "yup", "done", "next", "stop", "cancel", "abort",
}


def should_skip(prompt: str) -> bool:
    """Skip short prompts and common follow-ups."""
    cleaned = prompt.strip().lower()
    if len(cleaned) < 20:
        return True
    if cleaned in SKIP_PATTERNS:
        return True
    return False


def log_feedback(prompt: str, feedback: str) -> None:
    """Optionally log to file for review."""
    if os.environ.get("PROMPT_COACH_LOG", "").lower() != "true":
        return
    log_path = Path.home() / ".claude" / "prompt_coach.log"
    timestamp = datetime.now().isoformat()
    try:
        with open(log_path, "a") as f:
            f.write(f"\n--- {timestamp} ---\n")
            f.write(f"PROMPT: {prompt[:200]}{'...' if len(prompt) > 200 else ''}\n")
            f.write(f"FEEDBACK: {feedback}\n")
    except Exception:
        pass  # Don't fail on logging errors


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    # Handle both possible input formats
    # UserPromptSubmit sends: {"prompt": "..."}
    prompt = data.get("prompt", "")

    if not prompt or should_skip(prompt):
        sys.exit(0)

    # Load system prompt and skills digest from adjacent files
    hooks_dir = Path(__file__).parent
    system_prompt_path = hooks_dir / "prompt_coach_system.md"
    digest_path = hooks_dir / "prompt_coach_digest.md"

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        sys.exit(0)

    model = "claude-haiku-4-5-20251001"

    try:
        system_prompt = system_prompt_path.read_text()
        skills_digest = digest_path.read_text()
    except FileNotFoundError as e:
        log_feedback(prompt, f"[error: {e.filename} not found]")
        sys.exit(0)

    # Combine system prompt with skills digest
    full_system = f"{system_prompt}\n\n---\n\n# SKILLS DIGEST\n\n{skills_digest}"

    # Call Haiku API
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)

        response = client.messages.create(
            model=model,
            max_tokens=300,
            system=full_system,
            messages=[{"role": "user", "content": f"USER PROMPT TO EVALUATE:\n\n{prompt}"}]
        )

        feedback = response.content[0].text.strip()

        # Check if Haiku decided to stay silent
        if feedback and feedback != "NO_FEEDBACK":
            print("📋 Prompt Coach:", file=sys.stderr)
            print(feedback, file=sys.stderr)
            print("---", file=sys.stderr)
            log_feedback(prompt, feedback)
        else:
            log_feedback(prompt, "[silent - no issues]")

    except ImportError:
        log_feedback(prompt, "[error: anthropic package not installed]")
    except Exception as e:
        # Fail silently - don't block on errors
        log_feedback(prompt, f"[error: {e}]")

    sys.exit(0)


if __name__ == "__main__":
    main()
