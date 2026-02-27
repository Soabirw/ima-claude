---
name: ima-brand
description: >-
  IMA Brand Book v4.0 knowledge — identity, voice, logo rules, content guidelines,
  audience profiles, and visual standards. Use when: writing IMA content, choosing brand voice/tone,
  applying logo usage rules, selecting brand colors for design decisions, creating social media
  content, drafting medical disclaimers, or reviewing brand compliance. Triggers on: IMA brand,
  brand guidelines, brand voice, logo usage, brand colors, content tone, social media guidelines,
  medical disclaimer, brand identity, IMA imagery, brand values, brand persona, IMA mission,
  IMA audience. For CSS/SCSS implementation, see ima-bootstrap skill instead.
---

# IMA Brand Guidelines

Brand Book v4.0 (September 2025) — Independent Medical Alliance.

## Core Principle

**Brand consistency builds trust in healthcare communication.**

Every piece of content, every design decision, every communication should reinforce IMA's position as a trustworthy, patient-centric medical alliance.

## Decision Tree

```
What type of brand question?
├── Identity (who we are, mission, values)
│   → references/brand-identity.md
├── Audience (who we're talking to, messaging)
│   → references/brand-identity.md
├── Voice & Tone (how we sound, copywriting)
│   → references/brand-identity.md
├── Colors (palette, usage, accessibility)
│   → references/visual-system.md
├── Typography (fonts, hierarchy, weights)
│   → references/visual-system.md
├── Logo (usage rules, lockups, clear space)
│   → references/visual-system.md
├── Imagery (photography, iconography style)
│   → references/visual-system.md
├── Social Media (platforms, sizes, content)
│   → references/digital-standards.md
├── Legal (disclaimers, copyright, compliance)
│   → references/digital-standards.md
├── Accessibility (WCAG, contrast ratios)
│   → references/digital-standards.md
└── CSS/SCSS implementation?
    → Use ima-bootstrap skill instead
```

## Quick Reference: Color Palette

| Name | Hex | Usage |
|------|-----|-------|
| Trustworthy Indigo | `#040C53` | Primary brand, headers, trust |
| Aquatic Pulse | `#0296A1` | CTAs, buttons, links |
| Bright Teal | `#00B8B8` | Highlights, hover states |
| Guidance Sky | `#A2CFF0` | Light accents, backgrounds |
| Vital Gold | `#FFCC00` | Warnings, attention |
| Red Ribbon | `#DD153B` | Urgency, errors |
| Plum Velvet | `#7B024D` | Accent, distinction |
| Calm Stone | `#919396` | Secondary text, labels |
| Clarity Wash | `#F2F3F5` | Backgrounds, cards |
| Accessible Teal | `#007BB4` | High-contrast alternative |
| Brand Gradient | `150deg, #00066F → #00B8B8` | Hero sections, overlays |

## Quick Reference: Typography

| Element | Font | Weight | Size |
|---------|------|--------|------|
| Page headers | Lato | Bold/Black | 40px |
| Section headers | Lato | Bold | 20px |
| Body text | Proxima Nova / Open Sans | Regular | 16px |
| Buttons | Lato | Bold | 18px, uppercase |
| Form labels | Open Sans | Regular | 14px |

## Quick Reference: Voice & Tone

| Context | Tone | Example |
|---------|------|---------|
| Website / General | Professional + Friendly | "We're here to support your health journey" |
| Medical content | Professional + Informative | "Research suggests..." with citations |
| Social media | Friendly + Inspirational | "Join thousands who've found better health" |
| Crisis / Urgent | Supportive + Professional | "If you're experiencing..." with clear next steps |
| Newsletters | Friendly + Supportive | "Here's what we've been working on for you" |
| Fundraising | Inspirational + Supportive | "Your support makes independent research possible" |

## Anti-Patterns

| BAD | GOOD | Why |
|-----|------|-----|
| "FLCCC" in new content | "IMA" or "Independent Medical Alliance" | Rebranded; FLCCC is legacy |
| Stretching or recoloring the logo | Use approved lockup variants | Brand integrity |
| Logo on busy/patterned backgrounds | White, light, dark, or gradient bg only | Readability |
| Logo below 200px width | Minimum 200px, use IMA lettermark for small sizes | Legibility |
| Jargon-heavy copy without explanation | Plain language with medical terms defined | Patient accessibility |
| Fear-based messaging | Solution-oriented, empowering language | Brand persona |
| Missing medical disclaimer on health content | Include standard disclaimer | Legal compliance |
| Inconsistent tone across channels | Match tone to context (see Voice table) | Brand consistency |
| Using non-brand colors for key elements | Brand palette only for primary UI | Visual consistency |

## Cross-References

- **CSS/SCSS implementation** (variables, mixins, components): `ima-bootstrap` skill
- **SCSS source files**: `~/IMA/dev/ima-brand/sass/` (ima-brand plugin repo)
- **Brand identity deep dive**: [references/brand-identity.md](references/brand-identity.md)
- **Visual system details**: [references/visual-system.md](references/visual-system.md)
- **Digital & legal standards**: [references/digital-standards.md](references/digital-standards.md)
