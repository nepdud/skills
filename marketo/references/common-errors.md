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
