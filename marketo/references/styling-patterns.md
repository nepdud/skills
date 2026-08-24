# Styling Patterns: Icons, Interactions, and a CSS Gotcha

Patterns from doing a dedicated visual-polish pass on a finished template
(matching a reference design more closely, adding hover states) -- distinct
from the initial build, and worth treating as its own step rather than
something to get perfect on the first pass.

## Comparing a live landing page against a reference design

Don't expect to `fetch` a live, Marketo-hosted landing page URL and get its
real rendered HTML/CSS back. In practice this returns only page metadata and
whatever plain text happens to survive (e.g. a footer copyright line) --
Marketo pages render most content in a way that a readability-style content
extractor strips out as boilerplate. Trying this once is fine to confirm,
but don't burn multiple fetch attempts expecting a different result.

The reliable path is: work from the reference design image directly (re-read
it carefully rather than relying on a summary from earlier in the
conversation) plus a rigorous line-by-line review of the actual template
source you already have. That combination is more accurate than a live pixel
diff would be anyway, since you have exact knowledge of every CSS rule in
the source.

## Icon-in-badge technique: icons that survive content edits

Small icon badges/pills ("Member Exclusive", "10% Off", eyebrow labels) in a
design often need a small icon before the text. The icon should **not** live
inside the `mktoText` span itself -- if it's inline with the editable text, a
marketer editing that field in the Rich Text Editor can accidentally delete
it. Keep the icon entirely in CSS instead, using `mask-image` with
`background-color: currentColor` so it automatically matches whatever text
color it sits next to, in both light and dark contexts, without needing a
separate color variant per placement:

```css
.badge-icon { display: inline-flex; align-items: center; gap: 6px; }
.badge-icon::before {
  content: "";
  width: 12px;
  height: 12px;
  flex-shrink: 0;
  background-color: currentColor;
  -webkit-mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2'%3E%3Ccircle cx='12' cy='8' r='5'/%3E%3Cpath d='M8.5 13 6 22l6-3 6 3-2.5-9'/%3E%3C/svg%3E");
  mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2'%3E%3Ccircle cx='12' cy='8' r='5'/%3E%3Cpath d='M8.5 13 6 22l6-3 6 3-2.5-9'/%3E%3C/svg%3E");
  -webkit-mask-repeat: no-repeat;
  mask-repeat: no-repeat;
  -webkit-mask-size: contain;
  mask-size: contain;
}
```
Apply `class="badge-icon"` alongside the component's own class on the
element (e.g. `class="hero-eyebrow badge-icon mktoText"`). Because it's
`stroke`-based rather than filled, the mask renders as a clean outline icon
consistent with other outline-style icons in a design (feature-grid icons,
included-item icons, etc.) -- reuse the same SVG shape across multiple icon
spots in a template for visual consistency rather than sourcing a different
icon per instance.

## Watch for `display` conflicts when a utility class meets a component class

If a reusable utility class like `.badge-icon` sets `display: inline-flex`
and a specific component's own class (e.g. `.offer-modal-badge`) *also*
declares `display` (commonly `inline-block`, left over from before the badge
needed an icon), both selectors have equal specificity (one class each), so
**source order** decides the winner -- not which one seems more "specific"
to the situation. This is an easy, easy-to-miss bug: the icon renders but
sits misaligned or on its own line, because the component's own `display`
declaration silently won.

Fix by making the component's own rule declare the full flex layout directly
(`display: inline-flex; align-items: center; gap: 6px;`) rather than relying
on a utility class to supply it from elsewhere in the stylesheet. Whenever
adding a shared utility class (icon, badge, animation) to several existing
elements that already have their own styling, grep each target element's
existing CSS rule for a conflicting `display` (or any other property the
utility also sets) before assuming the utility's rule will simply apply.

## Hover interactions: treat as a dedicated pass, not part of the initial build

Marketo landing pages are static HTML/CSS -- there's no framework handling
interactivity, so every hover effect is a hand-written CSS transition. It's
easy to ship the initial build with zero interactivity and only add it when
asked, but a few cheap, tasteful additions consistently read as "polish"
worth doing proactively on any card-style grid (pricing tiers, feature
cards, testimonial cards):

```css
.card {
  transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
}
.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 14px 28px rgba(20,20,50,0.10);
  border-color: var(--accent-or-teal);
}
```
For a card that's already visually "featured" with a permanent lift (e.g. a
highlighted "Most Popular" pricing tier using `transform: translateY(-8px)`
at rest), don't just add a generic `:hover` -- give that specific card a
combined `.featured:hover` rule that lifts *further* from its own resting
position (e.g. `translateY(-14px)`), otherwise the hover style might
visually undo the featured card's distinguishing lift.

Icons inside a hovered card can react too, cheaply, for extra feedback:
```css
.card:hover .card-icon { background: var(--teal); color: #fff; }
```
None of this needs `cursor: pointer` unless the card itself is a link --
these are presentational hover cues on non-interactive containers, which is
a common and expected pattern in marketing page design (it doesn't imply
clickability the way cursor changes do).
