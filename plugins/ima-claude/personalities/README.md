# Personalities

**Important**: Personalities are **tone settings**, not expertise.

## What Personalities Do

Personalities change *how* Claude communicates, not *what* Claude knows. They come in two categories:

### Flavor Personalities
Themed language overlays for fun. These add tokens for entertainment.

- **40K Mode**: Warhammer 40K themed responses (purging heresy, machine spirits)
- **Templars Mode**: Medieval crusader themed responses (Deus Vult!)

### Functional Personalities
Communication style changes for efficiency. These reduce tokens for cost and speed.

- **Efficient Mode**: Precise, no filler, full sentences (~30-40% token savings)
- **Terse Mode**: Blunt fragments, bullets, compressed phrasing (~50-65% token savings)

## What Personalities Don't Do

Personalities do NOT:
- Add domain expertise (use Skills for that)
- Change technical recommendations
- Override skill guidance

## Usage

Simply say:

```
"Enable efficient mode"   # Precise, no filler (~30-40% savings)
"Enable terse mode"       # Blunt fragments, compressed (~50-65% savings)
"Enable 40k mode"         # Warhammer 40K themed
"Enable templars mode"    # Templar crusader themed
```

Then proceed with your normal requests.

## Combining with Skills

Personalities work alongside skills:

```
"Enable terse mode and use the js-fp skill to review this code"
```

Result: Technical guidance from js-fp skill, delivered in compressed style.

## Disabling

```
"Disable personality mode"
"Return to normal mode"
```
