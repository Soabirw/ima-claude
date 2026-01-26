# Advanced Checklist (Skills with Scripts)

Use in addition to core-checklist.md when analyzing Skills that include executable code.

## Script Quality

- [ ] Scripts solve problems rather than punt to Claude
- [ ] Error handling is explicit and helpful
- [ ] No "voodoo constants" (all values justified and documented)
- [ ] Scripts are self-documenting with clear comments
- [ ] Clear distinction between "execute" vs "read as reference"

## Dependencies

- [ ] Required packages listed in instructions
- [ ] Packages verified as available in target environment
- [ ] Version constraints specified where necessary
- [ ] Installation commands provided

## Verification & Feedback Loops

- [ ] Validation steps for critical operations
- [ ] Feedback loops for quality-critical tasks
- [ ] Intermediate outputs are machine-verifiable
- [ ] Error messages are specific and actionable

## File Path Conventions

- [ ] All paths use forward slashes (Unix-style)
- [ ] Relative paths used where possible
- [ ] Path references are correct and exist

## Script Documentation

- [ ] Clear usage examples in SKILL.md
- [ ] Expected input/output documented
- [ ] Error conditions documented
- [ ] Return codes/exit statuses explained where relevant

## MCP Tool References (if applicable)

- [ ] Fully qualified tool names used (ServerName:tool_name)
- [ ] Server names match available MCP servers
- [ ] Tool capabilities accurately described
