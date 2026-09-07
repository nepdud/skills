# Marketo Forms Integration

## On-platform vs external embedding -- pick the right pattern

**If the landing page is hosted natively on Marketo's own infrastructure**
(built from a Design Studio template, standard case), all you need in the
template is an empty placeholder:
```html
<div class="mktoForm" id="offerForm" mktoName="Offer Popup Form"></div>
```
Marketo's own landing page rendering engine automatically handles loading
Forms 2.0 JS and binding the form once a marketer attaches a real Form asset
to that region via the editor's **Insert Elements > Form**. No manual script
tags needed.

**Only if embedding a Marketo form on an external, non-Marketo website**
would you need to manually write:
```html
<form id="mktoForm_1234"></form>
<script src="//app-xxx.marketo.com/js/forms2/js/forms2.js"></script>
<script>
  MktoForms2.loadForm("//app-xxx.marketo.com", "123-ABC-456", 1234);
</script>
```
Don't add this pattern to an on-platform LP template -- it's unnecessary and
can conflict with Marketo's own automatic handling.

## What has to happen in Marketo's UI (can't be done from template code)

1. Build an actual **Form asset** in Marketo's Form Editor with the needed
   fields.
2. Any field beyond Marketo's standard set (First Name, Last Name, Email
   Address, Phone Number, etc.) -- e.g. a custom dropdown like "Are you a
   member?" -- has to be created first in Marketo's field management, then
   added to the form. This is a manual step; no template code can create
   Marketo data fields.
3. Set the form's post-submit behavior (thank-you page, redirect, email)
   as normal.
4. In the landing page editor, bind the real Form asset to the placeholder
   region.

Flag this clearly to the user -- it's easy to assume a "working form" is
purely a coding task, but the actual field definitions and lead-capture
wiring live in Marketo's data model, not in the template HTML.

## Styling Marketo's rendered form output

Once a real form is bound, Marketo renders it using a fairly stable, well-
known set of Forms 2.0 CSS classes. Marketo's own default stylesheet is
assertive, so overrides typically need `!important`:

| Element | Class |
|---|---|
| Form wrapper | `.mktoForm` |
| Each field's row | `.mktoFormRow`, `.mktoFormCol`, `.mktoFieldDescriptor` |
| Field label | `.mktoLabel` |
| Required-field asterisk | `.mktoAsterix` |
| Spacer between label and field (often needs hiding for a stacked layout) | `.mktoGutter`, `.mktoOffset` |
| Field wrapper | `.mktoFieldWrap` |
| The actual input/select/textarea | `.mktoField` |
| Submit button row/wrapper | `.mktoButtonRow`, `.mktoButtonWrap` |
| Submit button | `.mktoButton` |
| Validation error text | `.mktoErrorMsg` |
| Helper/instruction text | `.mktoInstruction` |

Example reskin to a rounded, single-column, brand-colored form:
```css
.mktoForm { width: 100% !important; font-family: inherit !important; }
.mktoFormRow, .mktoFormCol, .mktoFieldDescriptor {
  width: 100% !important; float: none !important; margin-bottom: 18px !important;
}
.mktoLabel {
  width: auto !important; float: none !important; display: block !important;
  font-weight: 700 !important; margin-bottom: 6px !important;
}
.mktoAsterix { color: #e0483e !important; }
.mktoGutter, .mktoOffset { display: none !important; width: 0 !important; }
.mktoFieldWrap { width: 100% !important; float: none !important; }
.mktoField {
  width: 100% !important; box-sizing: border-box !important;
  padding: 12px 14px !important; border: 1px solid #d7d9e3 !important;
  border-radius: 8px !important;
}
.mktoField:focus { outline: none !important; border-color: var(--accent) !important; }
.mktoButtonRow, .mktoButtonWrap { width: 100% !important; margin: 0 !important; }
.mktoButton {
  width: 100% !important; border: none !important; border-radius: 50px !important;
  padding: 14px !important; font-weight: 700 !important; cursor: pointer;
}
```

**Note:** exact class names are stable across most accounts but can vary
slightly by Marketo instance/theme version. If a specific field doesn't pick
up styling once a real form is bound, have the user open browser dev tools,
inspect the actual rendered class on that element, and adjust the selector
accordingly.

## Popup/modal pattern (button click opens a form modal)

Key design decisions and why:

- **Trigger with a `data-*` attribute, not an href-based selector.** CTA
  button hrefs are often tokenized (`href="${ctaHref}"`) and a marketer may
  repoint them to a real URL later -- an href-matching click listener would
  silently stop working. A `data-modal-trigger="offer"` attribute on the
  button keeps the open behavior independent of whatever the href is set to.
- **Use `opacity`/`visibility` instead of `display` for the overlay
  transition**, so it can actually animate in/out (display can't be
  transitioned) while still being non-interactive and hidden from screen
  readers/tab order when closed.
- **Auto-close on successful submit** via `MktoForms2.whenReady()` +
  `form.onSuccess()`, so the marketer doesn't need to build that logic
  separately. Don't close immediately, though -- swap in a brief thank-you
  confirmation panel first so the visitor knows the submission actually
  went through, *then* close after a few seconds. An abrupt close with no
  acknowledgment reads as broken, not fast.
- Return `false` from `onSuccess()` if showing a custom confirmation --
  that tells Forms 2.0 to skip its own default follow-up (like a configured
  redirect), since the modal is handling confirmation itself. Only return
  `true`/omit the return if the marketer explicitly wants Marketo's own
  configured follow-up to also fire.
- Reset the modal back to the form state every time it's reopened (not just
  on page load), in case a visitor submits, closes, and reopens later in
  the same session -- otherwise they'd see a stale success message instead
  of a fresh form.

```html
<div class="offer-modal-overlay" id="offerModalOverlay">
  <div class="offer-modal" role="dialog" aria-modal="true">
    <button type="button" class="offer-modal-close" id="offerModalClose" aria-label="Close">&times;</button>
    <div class="offer-modal-header"> ... badge / title / subtext ... </div>
    <div class="offer-modal-body">
      <div class="mktoForm" id="offerForm" mktoName="Offer Popup Form"></div>
    </div>
  </div>
</div>
```

```css
.offer-modal-overlay {
  position: fixed; inset: 0; background: rgba(15,16,30,0.55); z-index: 9999;
  display: flex; align-items: center; justify-content: center; padding: 24px;
  overflow-y: auto; opacity: 0; visibility: hidden;
  transition: opacity 0.2s ease, visibility 0.2s ease;
}
.offer-modal-overlay.is-open { opacity: 1; visibility: visible; }
.offer-modal {
  background: #fff; width: 100%; max-width: 520px; border-radius: 16px;
  overflow: hidden; max-height: 90vh; display: flex; flex-direction: column;
  transform: translateY(12px) scale(0.98); transition: transform 0.25s ease;
}
.offer-modal-overlay.is-open .offer-modal { transform: translateY(0) scale(1); }
```

```js
(function () {
  var overlay = document.getElementById('offerModalOverlay');
  var closeBtn = document.getElementById('offerModalClose');
  var formWrap = document.getElementById('offerFormWrap');
  var successPanel = document.getElementById('offerSuccess');
  if (!overlay) return;

  function showSuccess() {
    if (formWrap) formWrap.classList.add('is-hidden');
    if (successPanel) successPanel.classList.add('is-visible');
  }
  function resetToForm() {
    if (formWrap) formWrap.classList.remove('is-hidden');
    if (successPanel) successPanel.classList.remove('is-visible');
  }

  function openModal(e) {
    if (e) e.preventDefault();
    resetToForm(); // always start on a fresh form, even after a prior successful submit
    overlay.classList.add('is-open');
    document.body.style.overflow = 'hidden';
  }
  function closeModal() { overlay.classList.remove('is-open'); document.body.style.overflow = ''; }

  document.querySelectorAll('[data-modal-trigger="offer"]').forEach(function (t) {
    t.addEventListener('click', openModal);
  });
  closeBtn.addEventListener('click', closeModal);
  overlay.addEventListener('click', function (e) { if (e.target === overlay) closeModal(); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeModal(); });

  if (window.MktoForms2) {
    window.MktoForms2.whenReady(function (form) {
      form.onSuccess(function () {
        showSuccess();
        setTimeout(closeModal, 3500);
        return false; // skip Marketo's own default follow-up -- we show our own confirmation
      });
    });
  }
})();
```

The success panel is a sibling of the form wrapper inside `.offer-modal-body`,
toggled via an `is-hidden`/`is-visible` class pair rather than removed from
the DOM, so the form instance (and Marketo's binding to it) stays intact
across opens/closes in the same session:

```html
<div class="offer-modal-body">
  <div class="offer-form-wrap" id="offerFormWrap">
    <div class="mktoForm" id="offerForm" mktoName="Offer Popup Form"></div>
  </div>
  <div class="offer-success" id="offerSuccess">
    <div class="offer-success-icon"><!-- checkmark svg --></div>
    <h4 class="mktoText" id="modalSuccessTitle" mktoName="Modal Success Title">Thank You!</h4>
    <p class="mktoText" id="modalSuccessText" mktoName="Modal Success Text">We've received your information and will be in touch soon.</p>
  </div>
</div>
```
```css
.offer-form-wrap.is-hidden { display: none; }
.offer-success { display: none; flex-direction: column; align-items: center; text-align: center; }
.offer-success.is-visible { display: flex; }
```
