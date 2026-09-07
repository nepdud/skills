# Common Marketo Validation Errors and Fixes

## "Invalid tags. Run code validation and try again"

This is the generic, unhelpful top-level error shown when approving a
template from the summary/actions view. It does **not** tell you what's
actually wrong. Don't guess from this message alone.

**First move:** open the template's code editor and look for a **Validate**
button separate from Approve/the outer "Landing page template actions"
dropdown. It's inside the code editing view itself. Running that gives a
specific, actionable error (like the mktoContent one below) instead of the
generic message.

**If you have to debug blind before that's available, check for, in order
of how often each has actually been the culprit:**

1. **Smart/curly quotes.** A straight `'` or `"` that got silently
   autocorrected into a curly `'` `'` `"` `"` somewhere in an attribute
   value, almost always from copy-pasting code through a word processor,
   Notion, Slack, or similar. Nearly invisible on a normal read-through.
   Search the raw file for `'` `'` `"` `"` characters specifically.
2. **Zero-width space characters** sitting on otherwise-blank lines --
   another copy-paste artifact, invisible in most editors.
3. **Duplicate `id` values.** Must be unique across the entire document,
   including between `<head>` meta tags and body elements.
4. **Missing `mktoName`, `class`, or `id`** on an `mkto*`-classed element.
5. **Malformed/unbalanced HTML** -- an unclosed `<div>`, mismatched
   quote in an attribute, etc.

Run `scripts/validate_template.py` on the file to check items 1-4
automatically before spending time hunting by eye.

## "Missing a body div.mktoContent element"

Free-Form-template-specific requirement. Fix by adding, anywhere in the
body:
```html
<div class="mktoContent" id="mktoContent"></div>
```
This is the canvas drop-zone Free-Form pages need to let a marketer drag in
additional modules. Guided templates don't require it. If a template needs
to serve either type at some point, it's harmless to leave in for a Guided
template even though it's not required there.

## Landing page layout completely collapsed / floating boxes / no backgrounds

This is not a validation error -- the template approves and the page
builds fine, but the rendered result looks structurally broken (see the
screenshot signature described in `template-types.md`). This means the
landing page was built from a **Free-Form** template but the design has
multi-column layout, grids, or section backgrounds that Free-Form's
canvas-based rendering doesn't preserve. The fix is switching to a Guided
template, not further code debugging -- see `template-types.md` for the
full explanation and fix steps.

## A landing page shows duplicated content in a newly-added field

If a template's code gets new `mkto*` fields added *after* landing pages
have already been built from it, an existing page may not automatically
pick up proper default content for that new field -- it can show blank, or
duplicate a neighboring field's saved value instead of falling back to the
template's true default text. This is a data/sync issue on that specific
landing page instance, not a bug in the updated template code.

**Fix:** open the landing page in the editor and manually type the correct
content directly into the new field(s). Don't expect it to self-correct by
re-approving the template again.

## A header/nav bar's contents are bunched together instead of spread across the full width

If a header uses `display: flex` with `justify-content: space-between` but
the actual row of content (logo group, nav, CTA button) sits inside a
`.container` div for max-width/centering, the `space-between` has to live
on `.container` itself, not on the outer header. And critically,
`.container` needs an explicit `width: 100%` in that spot -- as a flex item
with no `flex-grow` set, it defaults to shrinking to fit its own content
rather than stretching to fill the header, which makes the logo and button
end up bunched together in the middle-left instead of spanning edge to
edge. This only shows up where `.container` sits inside a flex parent
(typically just the header) -- everywhere else `.container`'s parent is a
plain block-level section, where it naturally fills 100% width by default,
so the bug is easy to miss until the header specifically looks wrong.

Fix: put `display: flex; justify-content: space-between; width: 100%;` on
the inner `.container` (the actual row), and keep the outer header wrapper
plain (just background/padding/border) rather than also making it a flex
container.

## A styled list (e.g. custom checkmark bullets) suddenly looks different in one spot but not others

Likely cause: that specific rich-text (`allow_html="true"`) region was
edited using Marketo's Rich Text Editor's built-in "checklist"/to-do-list
toolbar button at some point, which swaps in real `<input
type="checkbox">` elements and overrides custom CSS list-bullet styling
(`::before` pseudo-elements on `<li>`, for example) -- the checkbox markup
takes visual precedence.

**Fixes:**
- Preventive: add `.your-list-class input[type="checkbox"] { display:
  none; }` to the template CSS so any accidental checklist-button use gets
  neutralized rather than breaking the design.
- Reactive: in the Rich Text Editor, clear formatting on that block and
  re-apply as a plain bulleted list instead of using the checklist button.

## "A mkto element is nested inside another"

An `mkto*`-classed element (most often `mktoText`) placed inside the
editable content of *another* `mkto*`-classed element. Easy to hit by
accident when a section is built as one big `allow_html="true"` rich-text
region (e.g. a feature list `<ul>`) and a later request asks for one line
inside it (e.g. a "setup fee" row) to be independently
toggleable/editable -- tagging that inner line with its own `mktoText`
`id`/`mktoName` creates exactly this violation, since it's still physically
inside the parent's own `mktoText` container.

**Fix:** the inner content stays as plain HTML (no `mktoText` class, no
`id`, no `mktoName`) -- it's still editable, just as part of the parent
region's rich text rather than as its own separate field. Only tag it
independently if you first move it *outside* the parent's mkto element
entirely (as a true sibling, not nested).

**Note:** the bundled `validate_template.py` does **not** catch this class
of error -- it checks smart quotes, duplicate ids, missing
mktoName/class/id, and tag balance, but not nesting. Marketo's own
Design Studio validator is the one that will actually catch it. Don't treat
a clean run of the local script as proof nesting is fine.

## overflow-x and overflow-y can't be mixed between hidden/visible -- one silently overrides the other

Setting `overflow-x: hidden` on an element (e.g. to contain a decorative
graphic's horizontal bleed) while leaving `overflow-y` at its default
`visible` does **not** actually keep the y-axis visible. Per spec, if
either axis is non-`visible`, the browser is required to force the *other*
axis to compute as `auto` -- even if you explicitly author
`overflow-y: visible` yourself, the authored value gets silently
overridden. The element becomes a real scroll container on both axes.

Symptoms this causes, which look unrelated to overflow at first:
- The page won't scroll normally while the cursor is over that section
  (the section scrolls itself instead of the page).
- An element meant to visually break out of that section (e.g. via a large
  negative margin) gets clipped at the section's edge instead, because
  it's now trapped inside a scroll container.

**How to confirm:** in DevTools, select the suspect element in the
Elements panel -- Chrome puts a grey `scroll` badge next to any element
that's a real scroll container, even ones that only scroll on one axis in
practice. If that badge is present despite `overflow-y: visible` being
declared in the Styles panel, this is the bug.

**Fix:** don't set an overflow value on the section at all if you can avoid
it. Move the containment down to just the element that actually needs
clipping (e.g. give the decorative image itself `overflow: hidden` and
remove whatever offset was making it bleed past its own box in the first
place), rather than clipping at the section level.

## Native `<select>` renders a different height than text `<input>`s despite identical CSS

Same `padding`, `font-size`, and `border` on both `.mktoField` inputs and
`select.mktoField` still doesn't produce the same rendered height. Native
`<select>` elements carry their own OS/browser-level chrome around the
dropdown arrow that isn't part of the box model you're controlling, and it
varies by browser.

**Fix:** strip the native chrome with `appearance: none; -webkit-appearance:
none; -moz-appearance: none;` on the select, then draw a custom arrow via
an inline SVG `background-image` (positioned with `background-position` /
`background-size`, with matching `padding-right` so text doesn't run under
it). With the native chrome gone, identical padding/font-size/line-height
between the input and select actually does produce matching heights.
Also explicitly set `background-color` and `margin` on the select for
mobile -- some mobile browsers (older Android WebViews especially) apply a
default gray fill or margin to `<select>` that isn't present on inputs,
even with `appearance: none`.

## `.mktoFormRow`, `.mktoFormCol`, and `.mktoFieldDescriptor` all getting `margin-bottom` doubles/triples the gap between fields

These three are nested inside each other in Marketo's actual rendered DOM
(`FormRow` > `FormCol` > `FieldDescriptor`). If more than one of them has
its own `margin-bottom`, the margins stack additively instead of
collapsing, since they're not true adjacent siblings -- the visible gap
between fields ends up 2-3x larger than intended.

**Fix:** pick exactly ONE of the three to own the margin (`.mktoFormRow` is
the natural choice, being the outermost per-field wrapper) and explicitly
zero the other two:
```css
.mktoForm .mktoFormRow { margin-bottom: 14px !important; }
.mktoForm .mktoFormCol,
.mktoForm .mktoFieldDescriptor { margin-bottom: 0 !important; }
```

## The native browser "please fill this field" validation bubble shows instead of Marketo's own styled error

If a field still has the native HTML `required` attribute and Marketo's
own JS-driven validation loses the race against the browser's built-in
constraint validation, the browser's native tooltip renders instead --
solid color, sharp corners, completely unstylable via CSS since it's
rendered outside the DOM/CSSOM entirely. Any custom `.mktoError`/
`.mktoErrorMsg` styling in the template CSS has zero effect on it, which
can look like the CSS "isn't working" when actually a different, invisible
element is winning.

**Fix:** disable native validation on the form entirely once Marketo's own
form JS is ready, so only Marketo's own (stylable) error markup can ever
show:
```javascript
MktoForms2.whenReady(function (form) {
  form.getFormElem().get(0).setAttribute('novalidate', 'novalidate');
});
```

**Also note:** Marketo's default error tooltip often has a small pointed
"tail"/arrow rendered as a CSS pseudo-element (`::before`/`::after`) on the
error container itself, not as a separate child element -- `display: none`
on a guessed `.mktoErrorArrow` class alone may not remove it. Cover both
possibilities:
```css
.mktoForm .mktoErrorArrow,
.mktoForm .mktoError:before,
.mktoForm .mktoError:after { display: none !important; content: none !important; }
```

## Floating labels on Marketo form fields need JS, not pure CSS

The common CSS-only floating-label trick relies on a `:placeholder-shown`
sibling selector, which needs the `<label>` to come *after* the `<input>`
in the DOM. Marketo generates each field's `.mktoLabel` as a sibling
*before* its field wrapper, so that trick doesn't apply. It needs real
JS-driven state: a class toggled on the field's `.mktoFormCol` based on
focus/blur/input/change, with CSS keyed off that class for the resting vs.
floated position. A `<select>` additionally needs to be treated as
permanently "floated" regardless of focus/value, since it always renders
its own selected text inside the control and can't share space with a
resting-size label the way a text input can.

## Trust-badge / logo marquee: a single clone isn't enough on wide screens

A common pure-CSS marquee pattern clones the scrolling content once and
animates `translateX(-50%)` for a seamless loop. With a short badge list,
two copies can fall short of covering the full screen width on anything
wider than ~1100px, which shows up as a visible gap or a jerky jump at the
loop point -- it's fine on narrow viewports and breaks specifically on wide
monitors, which is easy to miss if you only test at typical laptop widths.

**Fix:** measure the actual content and viewport width at runtime and
clone enough repeats to cover at least 2x the viewport width, keeping the
total repeat count even so `translateX(-50%)` always lands exactly on a
repeat boundary. Recalculate on window resize. Set the animation duration
proportional to the actual content width (not a fixed seconds value) so
the scroll speed feels consistent regardless of how many repeats a given
screen needed.

## `.container`'s `max-width` renders narrower than expected (e.g. asked for 1140px, only getting ~1060px)

If the page uses a global `* { box-sizing: border-box; }` reset (common),
`.container`'s own `padding` gets subtracted from its `max-width` instead
of sitting outside it -- the actual content column ends up
`max-width - (padding * 2)` wide, not the full `max-width`.

**Fix:** override `box-sizing` back to `content-box` specifically on
`.container`:
```css
.container {
  max-width: 1140px;
  padding: 0 24px;
  box-sizing: content-box; /* padding sits OUTSIDE the 1140px content width */
}
```

## Content changes keep "reverting" / re-pasting the template doesn't seem to fix a text change

Before assuming the template code is wrong or the wrong file was pasted,
check for the actual most common cause: **a Landing Page's individual
field content is saved independently of the template's default text once
a marketer has touched that field.** Editing the template's code and
re-approving it only changes what a *never-edited* field falls back to --
it cannot overwrite a value someone already typed into that field on a
specific Landing Page. This is easy to mistake for a sync/caching bug,
especially when the same "changes are gone" report recurs across multiple
rounds on the same fields.

**How to tell the difference:**
- Re-check the actual template code file for the change -- if it's
  genuinely present in the file that was supposed to be pasted, the
  template side is not the problem.
- If it's present in the template but not showing live, the fix is
  editing that specific field directly in the Landing Page editor, not
  more template code changes.
- Separately: a template's own **Validate/Approve** and a Landing Page's
  **Approve** are two different actions. Editing template code and
  re-approving the template does not auto-republish Landing Pages already
  built from it -- watch for a "template updated" banner on the Landing
  Page itself that needs to be accepted too.
- If genuinely stuck across several rounds, it's worth checking there
  isn't a duplicate/old template still active that's being edited or
  approved by mistake instead of the current one.
