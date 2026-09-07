# Agent skills

Reusable skills for Codex and Claude Code. Each skill lives in its own directory
and uses `SKILL.md` as its entry point. Supporting documentation is kept in
`references/`, while reusable validation or automation tools are kept in
`scripts/`.

## Installation

Install a skill by copying its complete directory into the skills directory for
the agent you use:

```bash
# Codex
cp -R marketo ~/.codex/skills/marketo

# Claude Code
cp -R marketo ~/.claude/skills/marketo
```

Restart the agent or begin a new session after installation so the new skill is
discovered. Do not copy only `SKILL.md`; references and scripts are part of the
skill and must remain beside it with the same directory structure.

## Marketo

The `marketo` skill helps an agent build, fix, and troubleshoot Adobe Marketo
Engage Design Studio landing-page templates and native Marketo Forms 2.0
integrations. It contains practical implementation knowledge for issues that
cannot be solved reliably with generic HTML and CSS guidance alone.

### When it activates

The skill is intended for requests involving:

- Adobe Marketo Engage or Design Studio landing pages
- Guided and Free-Form landing-page templates
- `mktoText`, `mktoImg`, `mktoForm`, `mktoVideo`, `mktoColor`, `mktoBoolean`,
  `mktoString`, and other `mkto*` declarations
- Template validation failures such as `Invalid tags` or a missing
  `mktoContent` element
- Responsive layout problems in Marketo landing pages
- Embedded, inline, modal, or popup Marketo forms
- Styling Marketo Forms 2.0 output and its generated DOM
- Pages whose structure or content changes after being created from a template

### What it covers

#### Guided versus Free-Form templates

The skill treats template type as the first architectural decision. Guided
templates preserve the authored HTML structure, including grids, columns,
section backgrounds, and responsive layout. Free-Form templates convert Marketo
elements into independently positioned canvas objects and do not preserve the
same surrounding layout structure.

For multi-column layouts, grids, background treatments, or other structured
designs, the skill recommends creating a Guided template. It also explains how
to recognize the Free-Form editor from its canvas-oriented interface and why a
broken Free-Form design normally needs to be rebuilt as Guided instead of being
patched repeatedly.

#### Marketo element and variable syntax

The skill distinguishes between the two main kinds of Marketo customization:

- Head-level variables such as `mktoColor`, `mktoBoolean`, and `mktoString`,
  which are referenced through `${tokenName}` values in CSS or attributes.
- Body-level editable regions such as `mktoText`, `mktoImg`, `mktoVideo`, and
  `mktoForm`, which define editable content directly in the document.

It documents the required unique `id`, matching class, and `mktoName`
attributes, plus common defaults and copy-ready declaration patterns.

#### Template validation and troubleshooting

The included guidance covers common validation and rendering failures,
including:

- Missing `mktoContent` in Free-Form templates
- Duplicate IDs and incomplete Marketo element declarations
- Smart quotes, zero-width characters, and unbalanced tags
- Invalid nesting of one editable Marketo element inside another
- Form spacing caused by stacked margins on generated wrapper elements
- Native select controls rendering at a different height from text inputs
- Browser-native validation appearing instead of Marketo's styled errors
- Floating labels that require JavaScript because of Marketo's generated DOM
- Overflow rules unexpectedly creating scroll containers or clipping content
- Container widths becoming smaller because padding is included in `max-width`
- Existing landing pages retaining saved field content after template defaults
  have changed
- The separate approval steps for templates and landing pages

#### Forms 2.0 integration

The skill explains the difference between native on-platform form placeholders
and forms embedded on external sites. On a Marketo-hosted landing page, a
`mktoForm` placeholder is normally sufficient. A manual
`MktoForms2.loadForm()` call is reserved for external pages.

It also provides patterns for popup and modal forms, including reliable button
triggers, overlay behavior, close controls, post-submit handling, and CSS
selectors for Marketo's generated form markup. The guidance notes that custom
fields must exist in Marketo and be added to the Form asset before template code
can display them.

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

- `SKILL.md` is the entry point. It routes the agent to the correct reference
  and contains the core implementation workflow and constraints.
- `references/template-types.md` explains Guided versus Free-Form behavior and
  how to identify the template type from the editor.
- `references/mkto-tags-reference.md` contains Marketo tag syntax, attributes,
  defaults, and reusable examples.
- `references/common-errors.md` documents validation errors, DOM and CSS traps,
  and content-update behavior observed in real Marketo workflows.
- `references/forms-integration.md` covers Forms 2.0 classes, styling, and a
  popup/modal integration pattern.
- `scripts/validate_template.py` performs deterministic checks on a completed
  HTML template before it is pasted into Design Studio.

### Using the validator

Run the bundled validator against a finished Marketo template:

```bash
python3 marketo/scripts/validate_template.py path/to/template.html
```

It checks for smart quotes and zero-width spaces, duplicate IDs, missing
attributes on Marketo elements, and unbalanced HTML tags. A successful local
check does not replace Marketo Design Studio's own Validate and Approve actions;
Marketo performs additional platform-specific validation, including checks that
the local script cannot fully reproduce.

### Important operational notes

- A template's type cannot be changed after creation. Moving a design from
  Free-Form to Guided requires creating a new Guided template and rebuilding
  the landing page from it.
- Updating and approving a template does not automatically publish every
  landing page created from it. The landing page may need to accept the template
  update and be approved again.
- Once a marketer edits a field on a landing page, that saved value can override
  later changes to the field's template default. Correct the value on the
  landing page itself when this occurs.
- Real company logos and wordmarks should be supplied through an image asset or
  `mktoImg` region rather than recreated in template code.
- Final validation should always include Marketo's own Design Studio validator
  and a visual test of the created landing page.

## Other skills

- **duo-review** — performs a full pre-launch readiness audit covering
  technical quality, SEO, AEO/GEO, social sharing, code hygiene, and conversion.
  It depends on `cro-review` at `~/.claude/skills/cro-review` for its conversion
  phase; the other phases can run without that dependency.
- **twitter** (`social-persona`) — writes X and LinkedIn posts, threads, replies,
  and bios in Subash's voice using a draft, hard-question, and humanizing review
  workflow.
