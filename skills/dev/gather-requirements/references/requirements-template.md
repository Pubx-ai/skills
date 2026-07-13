# Requirements Document Template

Fill in this structure to produce the requirements document. Omit sections that genuinely
don't apply to the feature (e.g. SEO for an internal CLI tool) rather than padding them,
and keep every entry concrete — file paths, versions, endpoint names, and measurable
targets beat vague adjectives like "fast" or "secure".

`KEY DECISIONS` is the durable record of the interview: one line per design-shaping
decision, with the chosen answer and who decided it. Only user-confirmed (or otherwise
explicitly decided) items belong there — anything you assumed without confirmation goes
under `ASSUMPTIONS & OPEN QUESTIONS` instead, so the sign-off review shows exactly what
was agreed versus guessed.

```text
DESCRIPTION:
[What needs to be built and why it's valuable]

USER STORY:
As a [user type], I want [goal] so that [benefit]
[Additional user stories if applicable]

ACCEPTANCE CRITERIA:
- [Specific, testable criterion]
- [Specific, testable criterion]
- [...]

KEY DECISIONS:
- [Question that shaped the design] → [chosen answer] ([user-confirmed | decided by <who>])
- [...]

TECHNICAL CONTEXT:
- Tech Stack: [frameworks, libraries, versions — be specific]
- Existing Systems: [components, services, APIs this integrates with]
- Database: [database type, ORM, relevant schemas]
- Authentication: [auth system and approach]
- Styling: [styling solution and component library]
- State Management: [state management approach]

CONSTRAINTS:
- Performance: [measurable targets — e.g. "API response < 200ms"]
- Security: [e.g. "rate limit auth endpoints", "sanitize user input"]
- Accessibility: [e.g. "WCAG 2.1 AA"]
- Browser Support: [e.g. "Chrome 90+, Safari 14+, mobile responsive"]
- SEO: [if applicable]

TESTING REQUIREMENTS:
- Test Coverage: [expected coverage and types]
- Testing Tools: [frameworks — e.g. "Jest, React Testing Library, Playwright"]
- Critical Scenarios: [must-test scenarios]
- Testing Patterns: [existing patterns in the codebase to follow]

SCOPE:
- MVP Features: [must-haves for the initial release]
- Future Enhancements: [nice-to-haves for later]
- Out of Scope: [explicitly excluded]

INTEGRATION POINTS:
- Existing Components: [components to reuse, with file paths]
- APIs: [internal/external APIs with endpoints]
- Data Models: [existing schemas/types to use]
- Utilities: [existing utilities/hooks to leverage]

ASSUMPTIONS & OPEN QUESTIONS:
- Assumptions: [decisions you made in the absence of an answer, so they can be corrected]
- Open Questions: [anything still genuinely undecided — never invent an answer for these]

ADDITIONAL CONTEXT:
- Design References: [Figma links, screenshots, mockups]
- Related Documentation: [links to relevant docs]
- References: [similar features in the codebase, with file paths]
```
