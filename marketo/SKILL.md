---
name: marketo
description: Build, fix, and troubleshoot Adobe Marketo Engage Design Studio landing page templates and Marketo Forms. Use this whenever the user mentions Marketo, Design Studio, Adobe Marketo Engage, landing page templates, mktoText/mktoImg/mktoForm/mktoColor/mktoBoolean/mktoString or any other mkto* tag, Free-Form vs Guided landing pages, "Invalid tags" or "missing mktoContent" validation errors, or embedding/styling a Marketo form (including popup/modal forms). Also trigger for general Marketo landing page coding tasks even if the user doesn't say "template" -- e.g. "make my Marketo LP mobile responsive," "add a popup form to my landing page," "why did my Marketo page's layout fall apart after I built it," "update the pricing section on my LP." Covers writing custom HTML/CSS templates with correct mkto tag syntax, diagnosing why a page's layout collapsed on preview, and reskinning Marketo's native Forms 2.0 output.
---

# Marketo Design Studio & Landing Pages

This skill captures hard-won, non-obvious knowledge about how Marketo's Design
Studio actually behaves in practice -- the kind of thing that isn't obvious
from the tag syntax alone and that caused real, confusing failures the first
time through. Read the relevant reference file before writing code; the
mechanics below aren't guessable from HTML/CSS knowledge alone.

## The single most important decision: Guided vs Free-Form

Before writing a single line of code, find out which template type this is
for, or steer the user toward Guided if they're starting fresh. This is the
decision that determines whether a custom design will actually render.

**Free-Form landing pages do not preserve your CSS layout.** When a landing
page is built from a Free-Form template, Marketo converts every `mkto*`
element into an individually positioned, absolute-coordinate draggable object
on a canvas. The surrounding structural HTML -- your `<div>`/`<section>`
wrappers, flexbox rows, CSS Grid, section backgrounds -- gets dropped in
translation. A perfectly valid, perfectly balanced multi-column design will
render as floating text boxes with huge random gaps and no background, and it
is *not* a code bug. This is confirmed, current Adobe documentation behavior,
not a guess: guided pages "include sections defined by their template," while
free-form pages "do not include predefined sections."

**Guided landing page templates preserve the actual document structure.**
Only the specific regions you tag as editable become editable; everything
else (grids, flexbox, backgrounds, layout) stays locked in place exactly as
coded. If the design has more than one column, a background image/gradient on
a section, or any layout that isn't "stack of full-width blocks," it needs a
**Guided** template, not Free-Form.

The syntax (`mktoText`, `mktoImg`, `mktoColor`, etc.) is identical between the
two -- only the template type chosen at creation time differs, and that type
can't be changed after creation. If someone already has a broken Free-Form
page with a design that has grids/columns/backgrounds, the fix is to create a
**new Guided template** with the same code and rebuild the page from that,
not to keep patching the Free-Form one.

Read `references/template-types.md` for the full explanation and how to spot
which type you're dealing with from a screenshot (the "Insert Elements" +
"Layers" panel with Rich Text/Image/Rectangle/Form/HTML/Snippet/Conversational
Flow is the canvas-based Free-Form editor).

## Core mkto tag syntax, in brief

Two categories of tags, and knowing which to use where saves a lot of back
and forth:

**Meta-level tokens** (declared once in `<head>`, then referenced via
`${tokenName}` anywhere in CSS or HTML attributes -- this is the *only* way
to get a value into a `style` block or an `href`):
- `mktoColor` -- color-picker fields
- `mktoBoolean` -- show/hide toggles, with `true_value`/`false_value`/`default`
- `mktoString` -- short reusable text (button labels, links, anything
  referenced via `${}` in an attribute)

**Body-level editable regions** (self-contained where they appear, no `<head>`
declaration needed):
- `mktoText` -- text content. Add `allow_html="true"` for anything that
  should be a rich-text WYSIWYG block (paragraphs with bold, bullet lists);
  omit it for simple single-line text.
- `mktoImg` -- images
- `mktoVideo` -- video embeds
- `mktoForm` -- a placeholder that a marketer binds a real Marketo Form asset
  to inside the landing page editor

Every `mkto*` element needs three things at minimum: a matching `class`, a
**unique** `id` (unique across the *entire* document, head and body
combined), and a `mktoName` (the human-readable label shown in the editor).
Missing any of these is one of the most common causes of vague validation
failures.

Full attribute reference, defaults, and copy-paste patterns:
`references/mkto-tags-reference.md`.

## Building a new template: recommended workflow

1. Confirm Guided vs Free-Form first (see above) if the design has any
   multi-column layout, grid, or section background.
2. Write the HTML with CSS custom properties fed once from `${}` tokens at
   the top (`:root { --accent: ${accentColor}; }`), then reference `var()`
   everywhere else -- much easier to read and maintain than repeating `${}`
   substitutions inline throughout a large stylesheet.
3. Use plain straight quotes (`"`/`'`) consistently. Mixed or "smart" curly
   quotes from a paste out of Docs/Notion/Slack are a common, nearly
   invisible cause of validation failures -- see below.
4. Never reproduce a real company's actual logo/wordmark in code. Leave an
   empty `mktoImg` placeholder and let the marketer upload the real asset.
5. Run `scripts/validate_template.py` on the finished file before telling the
   user to paste it in (see Validation section below).
6. If it's a Free-Form template, it needs a `<div class="mktoContent"
   id="mktoContent"></div>` somewhere in the body or approval fails with
   "Missing a body div.mktoContent element." This requirement is specific to
   Free-Form (it's the canvas drop-zone); Guided templates don't need it, but
   leaving it in is harmless.

## Validation & the "Invalid tags" error

Marketo's approval flow gives a genuinely unhelpful top-level error
("Invalid tags. Run code validation and try again") that doesn't say what's
wrong. Don't guess from that message alone -- the code editor has its own
**Validate** button, separate from Approve, that gives a specific error (like
the mktoContent one above). Always point the user to that first if they hit a
vague failure.

Before that, run a quick self-check -- this is exactly what
`scripts/validate_template.py` automates:
- No smart/curly quotes (`'` `'` `"` `"`) or zero-width spaces anywhere in the
  file (common from pasting out of a word processor or chat app)
- Every `id` is unique across the whole document
- Every `mkto*`-classed element has `mktoName`
- Tags balance (`<div>`/`</div>`, `<script>`/`</script>`, etc.)

Full list of error messages encountered and their fixes:
`references/common-errors.md`.

## Popups and forms

For a landing page hosted natively on Marketo's own infrastructure, an empty
`<div class="mktoForm" id="..." mktoName="...">` placeholder is enough --
Marketo's own LP renderer handles loading Forms 2.0 JS and binding the form
automatically once a marketer attaches a real Form asset to it via the
editor's Insert Elements > Form. Don't hand-write a `MktoForms2.loadForm()`
script for an on-platform LP; that pattern is only for embedding a Marketo
form on an external, non-Marketo website.

To build a popup/modal that opens on button click and holds a real form:
- Trigger it with a `data-*` attribute on the button, not a href-based
  selector -- hrefs are often tokenized (`${ctaHref}`) and a marketer could
  point them anywhere later, which would silently break a href-matching
  listener.
- Style the eventual rendered form with Marketo's standard Forms 2.0 CSS
  classes (`mktoForm`, `mktoFormRow`, `mktoLabel`, `mktoField`,
  `mktoButton`, etc.) -- Marketo's own stylesheet is assertive, so most
  overrides need `!important`.
- Custom fields (anything beyond standard fields like First Name/Email) must
  be created in Marketo's field management and added to the Form asset
  *before* they'll appear -- this is a manual step in Marketo's UI that no
  amount of template code can automate.

Full CSS class reference and a copy-paste modal pattern (open/close JS,
overlay, auto-close on successful submit):
`references/forms-integration.md`.

## Visual polish: icons, hover states, matching a reference design

Treat visual refinement (icons in badges, hover interactions on card grids,
matching a reference design's exact colors/weights) as its own pass after
the structural build works, not something to get perfect on the first draft.
A few non-obvious things came up doing this in practice -- a CSS technique
for icons that survive content edits, a specificity gotcha when a utility
class meets a component's own styling, and why fetching a *live* Marketo LP
URL for comparison doesn't work the way it seems like it should. All in
`references/styling-patterns.md`.

## A gotcha worth flagging proactively

Editing a template's code *after* landing pages already exist from it does
not retroactively update those pages' structure. A newly added field can
show blank, or -- as observed firsthand -- silently duplicate a neighboring
field's saved content instead of falling back to the template's true
default. If someone reports a landing page showing duplicated or wrong
content right after a template update, this is the first thing to check:
have them manually re-populate that specific field on that specific LP
rather than assuming the template code is wrong.

## Reference files

- `references/template-types.md` -- Guided vs Free-Form in depth, how to
  visually identify which one you're looking at from a screenshot
- `references/mkto-tags-reference.md` -- complete tag syntax, every
  attribute, copy-paste patterns for color/boolean/string/text/image/form
- `references/common-errors.md` -- every validation error message
  encountered so far and its fix
- `references/forms-integration.md` -- Forms 2.0 CSS class reference, popup
  modal HTML/CSS/JS pattern
- `references/styling-patterns.md` -- icon-in-badge CSS technique, a
  specificity gotcha with shared utility classes, and hover-interaction
  patterns for card grids
- `scripts/validate_template.py` -- run on any finished template file before
  telling the user to paste it into Design Studio
