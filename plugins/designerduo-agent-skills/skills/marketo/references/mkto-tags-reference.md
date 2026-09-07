# mkto* Tag Syntax Reference

Applies identically to both Guided and Free-Form templates -- syntax doesn't
change between the two; only how the resulting landing page renders does
(see `template-types.md`).

## The universal rule

Every `mkto*`-classed element needs, at minimum:
- `class` -- one of the mkto classes below
- `id` -- unique across the **entire document** (head meta tags and body
  elements share the same id-uniqueness requirement; a body `id="heroImg"`
  conflicting with anything else anywhere in the file will fail validation)
- `mktoName` -- the human-readable label the marketer sees in the editor

Missing any of these three on any element is one of the most common,
least-descriptive causes of a failed "Invalid tags" validation.

## Meta-level tokens (declare in `<head>`, use via `${tokenName}`)

These are the only mechanism for getting an editable value into a CSS
property or an HTML attribute (like `href`) -- you cannot put a `mktoText`
span inside a `style` block or an `href` value directly.

### mktoColor

```html
<meta class="mktoColor" id="accentColor" mktoName="Accent Color" default="#f5921e">
```
Reference anywhere with `${accentColor}`. Typical pattern: define once in a
CSS custom property block, then use `var()` everywhere else:
```css
:root { --accent: ${accentColor}; }
.btn { background: var(--accent); }
```

### mktoBoolean

```html
<meta class="mktoBoolean" id="showHero" mktoName="Show Hero Section?"
      true_value="block" false_value="none" default="true">
```
`true_value`/`false_value` are literal strings substituted wherever
`${showHero}` appears -- commonly used directly as a CSS `display` value:
```css
#hero { display: ${showHero}; }
```
Good practice: add one of these per major section so a marketer can hide a
whole section without needing template edits.

### mktoString

```html
<meta class="mktoString" id="heroCtaHref" mktoName="Hero Button Link" default="#offer">
```
Use for anything referenced via `${}` in an attribute (button hrefs) or for
short text reused in multiple spots. For a button's text + link, declare a
matching pair and reference both:
```html
<meta class="mktoString" id="heroCtaText" mktoName="Hero Button Label" default="Get Started">
<meta class="mktoString" id="heroCtaHref" mktoName="Hero Button Link" default="#offer">
...
<a class="btn" href="${heroCtaHref}">${heroCtaText}</a>
```
Give each distinct CTA location (nav, hero, pricing, footer, etc.) its own
pair rather than sharing one globally -- marketers usually want to point
different buttons at different destinations.

## Body-level editable regions (no `<head>` declaration needed)

These are self-contained wherever they appear in the body.

### mktoText

```html
<span class="mktoText" id="heroEyebrow" mktoName="Hero Eyebrow Label">Exclusive Offer</span>
```
For anything that should be rich-text editable (paragraphs with bold text,
bullet lists with a variable number of items), add `allow_html="true"` and
wrap real markup inside:
```html
<div class="mktoText" id="heroDescription" mktoName="Hero Description" allow_html="true">
  <p>Some copy with <strong>bold emphasis</strong> in it.</p>
</div>
```
`allow_html="true"` matters specifically for variable-length content like a
feature list inside a pricing card -- one `mktoText` field wrapping a `<ul>`
is far more practical than one field per list item, since plan tiers often
have a different number of features.

### mktoImg

```html
<div class="mktoImg" id="heroImage" mktoName="Hero Image"></div>
```
Leave empty in the template code -- the marketer uploads the actual image
through the editor. **Never hardcode a real company's logo or trademarked
asset into the template code itself**; always leave this as an empty
placeholder for a real, licensed asset to be uploaded into.

### mktoVideo

```html
<div class="mktoVideo" id="youtubeVideo" mktoName="YouTube Video"></div>
```

### mktoForm

```html
<div class="mktoForm" id="mainForm" mktoName="Main Form"></div>
```
Placeholder only -- see `forms-integration.md` for how this gets bound to a
real Marketo Form asset and styled.

## Free-Form-only requirement: mktoContent

Free-Form templates additionally require at least one:
```html
<div class="mktoContent" id="mktoContent"></div>
```
somewhere in the body. This is the free-canvas drop zone that lets a
marketer drag in additional modules. Without it, template approval fails
with "Missing a body div.mktoContent element." Guided templates don't
require this, but including it does no harm if the same code needs to serve
either type at some point.

## Quick pre-flight checklist

Before calling a template file done, confirm:
- [ ] Every `mkto*` element has `class` + unique `id` + `mktoName`
- [ ] Every `${token}` used in CSS/attributes has a matching `<meta>`
      declaration in `<head>`
- [ ] No duplicate `id` values anywhere in the file (head or body)
- [ ] Straight quotes only, no smart/curly quotes from a paste
- [ ] Free-Form templates have a `mktoContent` div somewhere

`scripts/validate_template.py` automates the mechanical parts of this list.
