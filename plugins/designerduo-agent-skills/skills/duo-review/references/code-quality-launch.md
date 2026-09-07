# Code quality at launch

Distinct from `technical-cro.md`'s speed/Core Web Vitals focus in the cro-review skill. This is broader pre-launch code hygiene, the kind of thing that's easy to forget in the rush to ship.

## Debug artifacts and leftovers
- No `console.log` statements or commented-out dead code left in production files.
- No `TODO` markers describing unfinished work that quietly shipped anyway.
- No test/staging API keys, endpoints, or payment sandbox credentials still wired in instead of production values, an easy, easy-to-miss launch-day mistake.
- No placeholder content: lorem ipsum text, `$000`-style placeholder prices, "Company Name" text, or stock example data left in a live page. This slips through most often when a page ships straight from a template without a final content pass.

## Build hygiene
- CSS/JS minified and bundled for production, not serving unminified dev builds.
- No exposed secrets or internal API keys visible in client-side source, since anything shipped to the browser is public regardless of intent.
- HTML validates: no unclosed tags, no duplicate IDs. Broken markup causes inconsistent rendering across browsers and confuses assistive tech and crawlers alike.

## Mixed content and protocol issues
- No `http://` assets loaded on an `https://` page. Browsers block or warn on this silently, and the resource may simply fail to load with no obvious error to the visitor.
- All domain variants (www, non-www, http) 301 redirect cleanly to the one canonical production URL. A redirect that 404s or soft-404s instead of forwarding correctly quietly kills a share link or an old bookmark.

## Third-party embeds
- Maps, calendars, chat widgets, and video embeds actually load in the production environment, not just in local development. Check they aren't pointed at a dev-only domain or blocked by a Content Security Policy that wasn't updated for production.

## Pre-launch link and asset sweep
- Crawl every internal and outbound link right before launch. Links referenced during development can go stale by the time the page actually ships, and outbound links to third-party sites can rot even faster.
- Confirm caching headers/CDN are configured so repeat visits and asset delivery are genuinely fast, not just the first load during testing.

## How to use this during an audit
Treat this as a pre-flight check, mostly pass/fail rather than a judgment call. Anything found here (a leftover placeholder, an exposed key, a broken redirect) is a launch blocker, not a nice-to-have polish item, since these are the kinds of bugs that are invisible until a real visitor or a real crawler hits them.
