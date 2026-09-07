# SEO fundamentals

Traditional search-engine readiness checks. These are on/off checks, mostly. A page either has them correctly or it doesn't, unlike the judgment-call findings in cro-review.

## Title tags and meta descriptions
- Every page has a unique title tag, roughly 50 to 60 characters so it doesn't truncate in search results.
- Every page has a unique meta description, roughly 150 to 160 characters, that actually describes the page and includes a reason to click, not just a keyword list.
- Title tag states what the page is about in plain language, ideally with the primary keyword near the front.

## URL structure
- Clean, descriptive, lowercase, hyphenated URLs. Avoid query-string-only URLs for pages that should be indexable.
- Canonical URL set correctly on every page, and it points at the real production domain, not a placeholder or staging domain left over from development.
- One canonical version of the site (www vs non-www, http vs https) with the others 301 redirecting to it, not serving duplicate content on both.

## Heading structure
- One H1 per page that states what the page is about.
- Logical H2/H3 nesting that reflects actual content hierarchy, not headings chosen for font size (see `information-architecture.md` in cro-review for the full reasoning).

## Images
- Alt text on every meaningful image, describing what the image actually shows or does, not "image1.jpg" or a keyword-stuffed string. Decorative images get empty alt (`alt=""`), not a meaningless placeholder.
- Image file names are descriptive where practical, since some search surfaces still weight this lightly.

## Structured data
- Add schema.org markup relevant to the page type: `Organization`, `Product`, `Course`, `Event`, `FAQPage`, `Review`/`AggregateRating`, `LocalBusiness`, `BreadcrumbList`.
- Structured data must match the visible content exactly. Mismatched or fabricated structured data (a review count in schema that doesn't match what's shown on the page) risks a manual action from Google, not just a missed opportunity.
- Validate the structured data actually parses correctly before launch, a typo in the JSON-LD silently voids the whole block.

## Crawlability and indexing
- `robots.txt` allows the real pages to be crawled. Check for a leftover `Disallow: /` from a staging environment, this is one of the most common accidental launch-day mistakes and it's invisible unless you actually check the file.
- XML sitemap exists, lists the real production URLs, and gets submitted to Google Search Console and Bing Webmaster Tools after launch.
- `meta name="robots"` tags are `index, follow` on pages meant to be found, not left on `noindex` from a staging config.
- No broken internal links, and internal anchor text is descriptive ("see our pricing") rather than generic ("click here"), since anchor text carries some topical signal.

## Mobile-first indexing
- Google indexes the mobile version of a page as the primary version. If the mobile layout hides content that the desktop layout shows, that hidden content may not count for indexing purposes. Check content parity between mobile and desktop, not just that mobile "looks fine."

## Page speed as a ranking factor
- Speed affects both user experience and search ranking. Cross-reference `technical-cro.md` in the cro-review skill for the Core Web Vitals detail, it's the same underlying metric feeding both conversion and SEO outcomes.

## How to use this during an audit
Check each item as a pass or fail, not a judgment call, since these are largely binary technical facts about the page rather than opinions. Report any fail as a launch blocker if it affects indexing (robots.txt, canonical, noindex tags) and as a high-priority fix otherwise (title/description length, alt text, structured data).
