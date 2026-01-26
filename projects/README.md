# ima-claude Projects

Research and assistant projects designed to work with both **Claude Web Projects** and **Claude Code**.

> **Note**: These projects are **not part of the automated install**. They're provided for manual setup and as educational examples for building your own Claude Projects. Copy the patterns here to create domain-specific research assistants for any field.

## Concept

Each project contains:
- **`instructions.md`** - Claude Web ready instructions (copy/paste into Instructions box)
- **`CLAUDE.md`** - Claude Code bootstrap (auto-loaded when CC launched from project dir)
- **`files/`** - Committed knowledge files (indexes, references, guides we created)
- **`resources/`** - Gitignored user-downloaded content (see each project's SETUP.md)

## Available Projects

| Project | Description |
|---------|-------------|
| **patristic-researcher** | Early Church Fathers research (~30-430 AD) |
| **mecha-thomas** | Thomistic research with Chestertonian voice |
| **mecha-alphonsus** | Marian theology in the style of St. Alphonsus |

## Setup

### For Claude Web (claude.ai)

1. Create a new Project on [claude.ai](https://claude.ai)
2. Open the project folder you want to use
3. Copy content from `instructions.md` → paste into **Instructions** box
4. Upload all files from the `files/` directory to **Project Knowledge**
5. (Optional) Upload any referenced skills from `~/.claude/skills/` to **Capabilities**
6. (Optional) Download resources per `resources/SETUP.md` and upload those too

### For Claude Code

**Option A: Launch directly from project folder**
```bash
cd ~/dev/ima-claude/projects/patristic-researcher
claude
```

The `CLAUDE.md` file loads automatically, giving Claude Code the project context.

**Option B: Copy to a working directory**
```bash
# Copy project to your research folder
cp -r ~/dev/ima-claude/projects/patristic-researcher ~/research/early-church/
cd ~/research/early-church/
claude
```

This lets you add your own files without modifying the original project.

## File Organization

```
projects/
├── README.md                    # This file
├── .gitignore                   # Ignores resources/ (user downloads)
│
├── patristic-researcher/
│   ├── instructions.md          # Claude Web instructions
│   ├── CLAUDE.md                # Claude Code bootstrap
│   ├── files/                   # COMMITTED - our indexes & references
│   │   ├── Index-NT-Epistles.md
│   │   ├── Index-Apostolic-Fathers.md
│   │   ├── Index-Ante-Nicene.md
│   │   ├── Index-Nicene-Post-Nicene.md
│   │   ├── Patristic-Quick-Reference.md
│   │   └── references/
│   │       └── [thematic references]
│   └── resources/               # GITIGNORED - user downloads
│       └── SETUP.md             # Instructions for obtaining texts
│
├── mecha-thomas/
│   ├── instructions.md
│   ├── CLAUDE.md
│   ├── files/
│   │   ├── Index-Summa-Theologiae.md
│   │   ├── Index-Summa-Contra-Gentiles.md
│   │   ├── Index-Disputed-Questions.md
│   │   ├── Index-Other-Works.md
│   │   └── Thomistic-Quick-Reference.md
│   └── resources/
│       └── SETUP.md
│
└── mecha-alphonsus/
    ├── instructions.md
    ├── CLAUDE.md
    ├── files/
    │   └── [marian indexes/references]
    └── resources/
        └── SETUP.md
```

## Two-Folder Pattern

Each project uses a **files/** + **resources/** split:

| Folder | Committed | Contents |
|--------|-----------|----------|
| `files/` | Yes | Indexes, references, guides **we created** |
| `resources/` | No (gitignored) | Public domain texts, large PDFs **user downloads** |

This keeps the repo clean while allowing rich local research environments.

## Private Projects

For projects containing proprietary or sensitive content:

1. Create a sister repository (e.g., `ima-claude-private`)
2. Use the same structure as public projects
3. Reference public ima-claude skills without issue
4. Keep `resources/SETUP.md` pointing to your private storage (Nextcloud, etc.)

The convention is documented here but the private repo is created separately as needed.

## Skill References

Projects may reference installed skills from `~/.claude/skills/`:

- **patristic-theology** - Era overviews, major themes, Father summaries
- **marian-devotion** - Rosary variants, consecration, chaplets

For Claude Web, upload the skill files to the Project's Capabilities section.

For Claude Code, skills are auto-discovered from `~/.claude/skills/`.

## Building Your Own Projects

Use these projects as templates for any domain. The pattern works for:

- **Research assistants**: History, science, literature, theology
- **Domain experts**: Legal research, medical references, technical specs
- **Creative projects**: Writing assistants, worldbuilding, game design
- **Learning tools**: Language study, exam prep, skill development

### Template Structure

```
my-project/
├── instructions.md      # Persona, methodology, tone guidelines
├── CLAUDE.md            # CC bootstrap referencing instructions.md
├── files/               # Your curated knowledge (indexes, references)
└── resources/
    └── SETUP.md         # Where to get supplementary materials
```

### Key Principles

1. **instructions.md** should be self-contained for Claude Web (copy/paste ready)
2. **CLAUDE.md** adapts the same content for Claude Code's file-based context
3. **files/** contains your created content (indexes, guides, structured references)
4. **resources/** holds downloaded/external content (gitignored, user provides)

### Example: Creating a Legal Research Project

```
legal-researcher/
├── instructions.md      # Legal research methodology, citation formats
├── CLAUDE.md            # CC bootstrap
├── files/
│   ├── Index-Constitutional-Law.md
│   ├── Index-Contract-Law.md
│   └── Citation-Quick-Reference.md
└── resources/
    └── SETUP.md         # Links to case law databases, statutes
```

## Contributing

To add a new project to ima-claude:

1. Create directory: `projects/your-project/`
2. Create `instructions.md` with Claude Web-ready instructions
3. Create `CLAUDE.md` referencing instructions.md and files/
4. Add knowledge files to `files/`
5. Create `resources/SETUP.md` explaining where to get additional resources
6. Update this README's project table
