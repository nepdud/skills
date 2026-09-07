# Agent skills

Reusable skills for Codex and Claude Code. Each skill packages specialized
instructions, references, and optional scripts that help an agent handle a
specific kind of work consistently.

## Skills at a glance

| Skill | Purpose | Main output |
|---|---|---|
| `duo-review` | Audit a landing page or site before launch | Phase-by-phase readiness report and ordered action plan |
| `marketo` | Build and troubleshoot Adobe Marketo Engage landing pages and forms | Valid Marketo template code, diagnosis, and implementation guidance |
| `twitter` (`social-persona`) | Write social content in Subash's established voice | X posts, threads, replies, LinkedIn posts, and bios |

## Installation

Copy the complete skill directory into the skills directory used by your agent.
For example, to install all three skills:

```bash
# Codex
cp -R duo-review ~/.codex/skills/duo-review
cp -R marketo ~/.codex/skills/marketo
cp -R twitter ~/.codex/skills/twitter

# Claude Code
cp -R duo-review ~/.claude/skills/duo-review
cp -R marketo ~/.claude/skills/marketo
cp -R twitter ~/.claude/skills/twitter
```

Restart the agent or begin a new session after installation so the skills are
discovered. Copy each complete directory, not only its `SKILL.md`, because its
references and scripts are part of the skill.

## Install directly in ChatGPT Desktop

Use only the three files in [`chatgpt-upload/`](chatgpt-upload/) for manual
drag-and-drop installation:

```text
chatgpt-upload/
|-- duo-review.skill
|-- marketo.skill
`-- social-persona.skill
```

Each archive contains exactly one skill and exactly one `SKILL.md`. To install:

1. Delete previous duplicate copies from ChatGPT's **Created by me** list.
2. Drag `duo-review.skill` into ChatGPT once.
3. Drag `marketo.skill` into ChatGPT once.
4. Drag `social-persona.skill` into ChatGPT once.
5. Confirm that the list contains exactly three entries: **duo review**,
   **marketo**, and **social persona**.

Do not drag the entire repository, the `plugins/` directory, or the ZIP in
`dist/` into the Skills screen. Those locations contain publishing artifacts
and repeat the canonical skill files, which causes ChatGPT to create multiple
entries with the same skill name.

## ChatGPT plugin package

The following package is for Plugin Directory submission, not manual dragging
into the **Created by me** screen. The three skills are bundled for publication
at:

```text
plugins/designerduo-agent-skills/
|-- .codex-plugin/
|   `-- plugin.json
`-- skills/
    |-- duo-review/
    |-- marketo/
    `-- twitter/
```

The plugin is named `designerduo-agent-skills`. Its manifest contains the
public listing metadata, three starter prompts, and a single `skills` entry
that exposes all bundled workflows. The distributable ZIP is generated at
`dist/designerduo-agent-skills-0.1.0.zip`.

Publishing it in ChatGPT requires submission through the OpenAI Platform:

1. Use an organization whose submitter has **Apps Management: Write** access.
2. Verify the individual or business identity that will publish the plugin.
3. Open the Plugin Submission Portal and create a **Skills only** submission.
4. Upload the ZIP bundle and complete the listing, policy, availability, test
   case, and release-note fields.
5. Submit the draft for review. After approval and publication, users can find
   and install the plugin from the shared ChatGPT and Codex Plugin Directory.

See [`SUBMISSION.md`](SUBMISSION.md) for prepared listing copy, starter prompts,
test cases, release notes, and the remaining publisher-owned requirements.

## DuoReview

### Purpose

`duo-review` is a full pre-launch readiness audit for landing pages, sales
pages, and websites. It checks whether a target is technically ready, visible
to search and answer engines, correctly represented when shared, clean enough
to ship, and prepared to convert visitors.

The skill is broader than a conversion-only review. It combines six audit
phases into one launch decision and turns the findings into a practical order
of operations.

### When it activates

Use the skill when a user asks to:

- Review a page or site before launch
- Find launch blockers or missing production requirements
- Audit technical readiness, SEO, AEO/GEO, social sharing, or code quality
- Produce a go-live checklist or an ordered launch plan
- Run a complete conversion review as part of a wider launch audit
- Audit a local project, a specific HTML file, or a live URL

The explicit command is `/duo-review`. A phase can be selected with
`--phase technical`, `seo`, `aeo`, `social`, `code`, or `conversion`.

### What it covers

The full audit is divided into six phases:

1. **Technical foundation:** availability, HTTPS, mobile behavior, forms,
   navigation, analytics, error handling, and launch-blocking failures.
2. **SEO:** titles, descriptions, canonical URLs, indexing directives,
   headings, image alternatives, sitemaps, and structured data.
3. **AEO/GEO:** direct-answer content, entity clarity, FAQ structure, AI crawler
   access, `llms.txt`, and whether content is easy for answer engines to cite.
4. **Social sharing:** Open Graph data, Twitter Card data, preview images,
   favicons, platform icons, and real share-preview verification.
5. **Code and performance:** debug artifacts, placeholder content, exposed
   secrets, mixed content, redirects, third-party embeds, and launch hygiene.
6. **Conversion:** the complete `cro-review` workflow, reported as quick fixes,
   larger improvements, and polish opportunities.

### Workflow and output

The skill reads the master checklist first, inspects the actual source or live
target, and marks each requirement as complete, missing, or needing external
verification. Findings must cite concrete evidence from the target instead of
relying on assumptions.

A full report contains a checklist for Phases 1 through 5, the tiered conversion
findings for Phase 6, explicit launch blockers, and one final ordered action
plan. A single-phase audit loads only the relevant material and returns a
focused checklist and action list.

Suggested headlines, calls to action, and other copy are passed through the
included humanization rules. Reports and rewrites avoid generic AI phrasing and
keep recommendations specific to the audited page.

### Included files

```text
duo-review/
|-- SKILL.md
`-- references/
    |-- aeo-geo.md
    |-- code-quality-launch.md
    |-- humanize-copy.md
    |-- pre-launch-checklist.md
    |-- seo-fundamentals.md
    `-- social-share-readiness.md
```

- `SKILL.md` defines invocation, phase routing, audit order, and report format.
- `pre-launch-checklist.md` is the master checklist and report spine.
- `seo-fundamentals.md` covers search-engine readiness.
- `aeo-geo.md` covers answer-engine and generative-engine readiness.
- `social-share-readiness.md` covers metadata, icons, and preview testing.
- `code-quality-launch.md` covers code and production hygiene.
- `humanize-copy.md` controls the style of rewritten or suggested copy.

### Dependencies and limitations

The conversion phase depends on the separate `cro-review` skill at
`~/.claude/skills/cro-review/`. The other five phases can still run without it.
Some checks against a local source can only be marked as needing verification,
such as live analytics, production redirects, or third-party services.

## Marketo

### Purpose

`marketo` helps an agent build, fix, and troubleshoot Adobe Marketo Engage
Design Studio landing-page templates and native Marketo Forms 2.0 integrations.
It provides platform-specific guidance for behavior that generic HTML and CSS
knowledge does not predict reliably.

### When it activates

Use the skill for requests involving:

- Adobe Marketo Engage or Design Studio landing pages
- Guided or Free-Form landing-page templates
- `mktoText`, `mktoImg`, `mktoForm`, `mktoVideo`, `mktoColor`, `mktoBoolean`,
  `mktoString`, or other `mkto*` declarations
- `Invalid tags`, missing `mktoContent`, or related validation failures
- Responsive layout failures in Marketo landing pages
- Inline, embedded, modal, or popup Marketo forms
- Styling the DOM generated by Marketo Forms 2.0
- Content that does not update after a template has changed

### What it covers

The skill begins with the architectural difference between Guided and
Free-Form templates. Guided templates preserve authored structure, grids,
columns, backgrounds, and responsive behavior. Free-Form templates convert
editable regions into independently positioned canvas objects. Structured
designs therefore normally require a Guided template.

It distinguishes head-level variables such as `mktoColor`, `mktoBoolean`, and
`mktoString` from body-level editable regions such as `mktoText`, `mktoImg`,
`mktoVideo`, and `mktoForm`. It documents required IDs, matching classes,
`mktoName` values, defaults, attributes, and reusable declaration patterns.

Its troubleshooting library covers duplicate IDs, smart quotes, zero-width
characters, invalid nesting, unbalanced tags, form spacing, native select
rendering, browser validation, floating labels, overflow behavior, container
widths, saved field content, and Marketo's separate approval steps.

The Forms 2.0 guidance explains native Marketo form placeholders, external
embedding, popup and modal patterns, generated CSS classes, close behavior, and
post-submit handling. It also explains which field configuration must happen
inside Marketo before template code can display it.

### Workflow and output

For new templates, the skill confirms the required template type, creates the
HTML and CSS with valid Marketo declarations, keeps each ID unique, and uses
editable regions only where marketers need control. For troubleshooting, it
uses the specific error or rendered behavior to select the appropriate
reference instead of guessing from Marketo's generic approval message.

The result may be template code, a focused patch, an explanation of a platform
behavior, or a step-by-step correction inside Design Studio. Finished template
files should be checked by the bundled validator before being pasted into
Marketo.

### Included files

```text
marketo/
|-- SKILL.md
|-- references/
|   |-- common-errors.md
|   |-- forms-integration.md
|   |-- mkto-tags-reference.md
|   `-- template-types.md
`-- scripts/
    `-- validate_template.py
```

- `SKILL.md` contains the core workflow and routes relevant requests.
- `template-types.md` explains Guided and Free-Form behavior.
- `mkto-tags-reference.md` documents Marketo tags, attributes, and examples.
- `common-errors.md` documents validation, DOM, CSS, and update problems.
- `forms-integration.md` covers Forms 2.0 styling and modal integration.
- `validate_template.py` checks a finished HTML template for common defects.

Run the validator with:

```bash
python3 marketo/scripts/validate_template.py path/to/template.html
```

### Dependencies and limitations

The validator detects smart quotes, zero-width spaces, duplicate IDs, missing
Marketo attributes, and unbalanced tags. It does not replace Design Studio's
own Validate and Approve actions. Template type cannot be changed after
creation, template approval does not automatically republish existing landing
pages, and saved page-level content may continue to override updated defaults.

## Social Persona

### Purpose

The `twitter` directory contains the `social-persona` skill. It writes and
edits X and LinkedIn content in Subash Dharel's established public voice. The
goal is concise, opinionated social writing that sounds specific to Subash,
DesignerDuo, and his community work instead of generic founder copy.

### When it activates

Use the skill when Subash asks for:

- An X post, tweet, thread, reply, quote post, or profile bio
- A LinkedIn post, reply, or profile description
- A hot take or social post about design, CRO, Nepal tech, or AI tools
- Content about DesignerDuo, AI Conf Asia, or WWKTM
- A review or rewrite that should sound more like him
- A punchier, shorter, or more human version of an existing social draft

The user does not need to say "in my voice" when the topic and requested format
clearly fit the persona.

### What it covers

The voice is witty, sharp, direct, and concrete. Sentences are short with varied
rhythm. Humor is dry rather than self-deprecating. Credentials and client names
are used only when they materially support the point.

The skill removes common AI and corporate-writing patterns. It prohibits em
dashes, generic LinkedIn announcements, "not X but Y" constructions, vague
importance claims, fake-profound endings, rhetorical setups, unsupported expert
attribution, synonym cycling, and unnecessary formatting. It also maintains a
specific banned-word list.

Threads are limited to two or three posts. Nepali code-switching is optional and
restricted to a small approved vocabulary used sparingly. For AI Conf Asia
threads, the `#AIConfAsia` hashtag appears only in the anchor post.

The main content pillars are:

- DesignerDuo, conversion optimization, and design criticism
- Nepal's technology ecosystem
- AI Conf Asia and WWKTM community building
- Practical opinions about AI tools without hype

### Workflow and output

The skill first drafts around the relevant content pillar. It then asks whether
a sharp person would actually say each line aloud, removes generic copy, scans
for hard voice violations, checks the banned patterns, and applies a portability
test. Any sentence that could be pasted unchanged into another founder's post
must become more specific or be removed.

The final output is a ready-to-publish post, short thread, reply, or bio. The
skill expects iteration and treats Subash's corrections as the authoritative
source for future voice decisions.

### Included files

```text
twitter/
`-- SKILL.md
```

`SKILL.md` is self-contained. It includes the persona, background context,
content pillars, hard constraints, banned language, editing workflow, and a
reference bio. No external scripts or reference files are required.

### Dependencies and limitations

The skill has no external skill dependency. It writes copy but does not publish
it to a social platform unless a separate connected tool is explicitly used and
the user authorizes publishing. Subash remains the final authority on whether a
draft matches his voice.
