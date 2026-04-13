# Code Review

## Goal
Review [PR URL | branch | file paths] for [correctness | security | FP compliance | all]

## Scope
- PR / branch / commit: [URL or ref]
- Files / modules: [paths or Serena symbol names — leave blank for all]
- Stack: [PHP | WordPress | JS | jQuery | React | Vue | etc.]

## Review focus
- [ ] Correctness — logic errors, edge cases, null paths
- [ ] Security — input validation, SQL injection, XSS, auth/authz, secrets
- [ ] FP — mutation, side effects, over-engineering, custom utilities over native
- [ ] Quality — naming, dead code, pattern consistency
- [ ] WordPress — nonce verification, capability checks, escaping
- [ ] [other]

## Pattern (proven)
Use `/ima-claude:task-master` to orchestrate:
1. Delegate to `/ima-claude:explorer` first — understand scope and surrounding context via Serena (not diff-only)
2. Delegate to `/ima-claude:reviewer` with domain skills: [php-fp, php-fp-wordpress, js-fp, js-fp-wordpress, jquery, etc.]
3. For each finding: request a 2nd opinion before finalizing
4. Document findings in Serena as `{pr-id}-review` for audit trail

## Do NOT
- Use `/code-review:code-review` (third-party) — its validation gates filter real issues
- Restrict reviewer to diff-only — bugs depend on surrounding context
- Skip the 2nd-opinion pass for Critical/Warning findings

## Acceptance
- [ ] All Critical issues have specific file:line + proposed fix
- [ ] Warnings include reasoning
- [ ] Findings saved to Serena
- [ ] 2nd opinion confirmed before reporting Critical
