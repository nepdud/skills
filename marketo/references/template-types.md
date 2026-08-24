# Guided vs Free-Form Landing Page Templates

## Why this matters more than anything else in this skill

This single distinction caused a fully-coded, well-structured landing page
design (multi-column hero, CSS Grid pricing cards, gradient section
backgrounds) to render as a blank white page with a handful of floating text
boxes scattered at seemingly random coordinates. The code was correct. The
template *type* was wrong for the design.

## How Free-Form actually works

Free-Form landing pages in Marketo are built on an absolute-position canvas
system, similar in spirit to a standalone drag-and-drop page builder. When a
landing page is created from a Free-Form template:

- Every element carrying an `mktoText`/`mktoImg`/`mktoForm`/etc. class is
  extracted and converted into an independently draggable object with its
  own explicit `left`/`top` pixel coordinates.
- The structural HTML around those elements -- `<div>` and `<section>`
  wrappers, CSS Grid/Flexbox rules, `background` on a parent container -- is
  **not** carried over as a rendering concern. Only the tagged elements
  themselves survive as canvas objects.
- This is confirmed by Adobe's own documentation: guided landing pages
  "include sections defined by their template," while free-form pages "do
  not include predefined sections, so add their content before editing it."
- It's also a long-standing, independently reported behavior -- one Marketo
  community member years ago described building an HTML template where "the
  elements (rich text, forms etc) are off when I preview it... the elements
  don't stay within the CSS divs," and the confirmed answer was: that's how
  Free-Form works; Guided templates behave differently.

### What this looks like when it goes wrong

Telltale signs in a screenshot of a broken Free-Form page:
- Text content is present and correct, but has no background color, no
  gradient, no grid/column alignment
- Elements that should sit side-by-side are stacked vertically with large,
  inconsistent gaps
- Small decorative elements (like a floating card meant to overlap a hero
  image) appear at odd, seemingly unrelated coordinates, disconnected from
  the element they were supposed to be positioned relative to
- The editor's right-hand panel shows "Insert Elements" (Rich Text, Image,
  Rectangle, Form, HTML, Snippet, Conversational Flow) plus a "View: Layers"
  / "Segment By" toolbar -- this UI is the canvas-based Free-Form editor

## How Guided actually works

Guided templates keep the real HTML document structure intact. The template
author declares specific regions as editable (same `mkto*` tag syntax as
Free-Form -- there is no syntax difference), and everything else -- layout,
grids, flexbox, backgrounds, responsive breakpoints -- stays exactly as
coded. The marketer editing the resulting landing page can only change what
was explicitly exposed; they can't rearrange the page structure, which is
the tradeoff for the layout actually holding.

## Practical decision rule

If the design has **any** of the following, it needs a Guided template:
- More than one column at any point in the layout
- A CSS Grid or Flexbox arrangement of sibling elements
- A background color, image, or gradient on a section that isn't the full
  page background
- Cards, a pricing table, a feature grid, or anything with repeated
  visually-grouped components

If the design is genuinely just a single-column stack of full-width blocks
(headline, one image, one form, done), Free-Form's canvas approach is fine
and its drag-and-drop flexibility is arguably a plus for that marketer.

## Switching between types

Template type is set at creation and is **not** changeable afterward on an
existing template asset. If a Free-Form template needs to become Guided:

1. Create a brand-new template in Design Studio, explicitly choosing the
   Guided type in the creation flow (naming/location of this option varies
   slightly by Marketo instance version -- if it's not obvious, ask the user
   to screenshot the template-creation dialog).
2. Paste in the same HTML/CSS/mkto-tag code -- no code changes needed, since
   the syntax is identical between the two types.
3. Approve the new Guided template.
4. Build a **new** landing page from it. Don't try to point an existing
   Free-Form-derived LP at the new Guided template; rebuild fresh.
