# Claude Code skills

Shared skills for Claude Code. To install one, copy its folder into `~/.claude/skills/`.

## Skills

- **duo-review** — full pre-launch readiness audit (technical, SEO, AEO/GEO, social share, code hygiene, conversion). Depends on the `cro-review` skill being present at `~/.claude/skills/cro-review` (loaded as Phase 6) — install that skill too, or `--phase` runs other than `conversion` still work without it.
- **marketo** — build, fix, and troubleshoot Adobe Marketo Engage Design Studio landing page templates and Marketo Forms. Covers the Guided vs Free-Form template distinction (the layout-collapse gotcha), full `mkto*` tag syntax, common validation errors and fixes, and popup/modal form integration with Forms 2.0. Includes a bundled `validate_template.py` script to catch duplicate IDs, missing `mktoName`, smart quotes, and unbalanced tags before pasting into Design Studio.
- **twitter** (`social-persona`) — write X (Twitter) and LinkedIn posts, threads, replies, and bios in Subash's voice. Hard voice rules (no em-dashes, no "not X but Y", no generic LinkedIn-isms, threads capped at 2-3 tweets, light approved Nepali code-switching) plus a draft → hard-question pass → humanizing pass workflow.
