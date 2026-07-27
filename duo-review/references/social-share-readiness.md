# Social share and browser-chrome readiness

What a page looks like when it's shared as a link, or pinned as a tab, or added to a home screen. Easy to get wrong because it's invisible during normal browsing, it only shows up at the moment someone shares or bookmarks the page.

## Open Graph tags
- `og:title`, `og:description`, `og:image`, `og:url`, `og:type`, `og:site_name` present on every page meant to be shared.
- `og:image` should be an absolute URL (not a relative path), publicly accessible without authentication, and roughly 1200x630 pixels, the standard size most platforms expect for a large preview card.
- The image itself should show real, specific content (the actual offer, a real product shot, real branding), not a generic stock photo or a broken/placeholder image.
- Keep `og:title` under roughly 60 characters and `og:description` under roughly 155 to 160 characters so preview cards don't cut off mid-sentence.

## Twitter/X card tags
- `twitter:card` (usually `summary_large_image`), `twitter:title`, `twitter:description`, `twitter:image`. Modern X largely falls back to Open Graph tags if Twitter-specific ones are missing, but explicit tags are more reliable and worth having.

## Favicon and browser-chrome icons
A full set, not just one file:
- `favicon.svg` or `.ico` for the browser tab.
- 16x16 and 32x32 PNG fallbacks for browsers or contexts that don't support SVG favicons.
- `apple-touch-icon` at 180x180 for iOS "Add to Home Screen."
- Android Chrome icons at 192x192 and 512x512, referenced from a `site.webmanifest` for "Add to Home Screen"/PWA-style behavior on Android.
- A Safari pinned-tab mask icon (SVG) if supporting Safari's pinned tab feature.
- A `theme-color` meta tag so the mobile browser chrome matches the brand color.

## Actually test it, don't just assume the tags are right
- Use the platform's own preview/debug tools before launch (Meta's Sharing Debugger, LinkedIn's Post Inspector, a Twitter Card Validator) rather than trusting that the tags in the HTML will render as expected.
- Platforms cache previous crawls. If a tag was broken and then fixed, the old broken preview may still show until the platform is told to re-scrape the URL, worth checking after any fix, not just after the first deploy.

## How to use this during an audit
Check that every tag exists, that `og:image` actually resolves to a real image at the right size, and that the favicon set is complete rather than just a single default icon. Flag a missing or broken `og:image` as a launch blocker level finding, since it's one of the most visible, most embarrassing failures the moment someone actually shares the link.
