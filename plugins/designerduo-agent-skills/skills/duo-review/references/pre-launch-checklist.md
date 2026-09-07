# The master go-live checklist

This is the actual sequence to run through before a page goes live. It's ordered: earlier phases are blockers (fix these or don't launch), later phases are quality/optimization work that can, if needed, ship slightly after launch without real damage. Report progress against this exact structure, phase by phase, with a status per item (done, missing, needs verification) and the concrete next action, not just a list of problems.

## Phase 1: Technical foundation (launch blockers)
- [ ] HTTPS/SSL valid, no mixed-content warnings
- [ ] Every form actually submits and reaches a real destination, no dead-end CTAs (a CTA that fires but goes nowhere is invisible until a real visitor hits it, so click every one during the audit)
- [ ] No broken links or dead anchors, internal or outbound
- [ ] 404 page exists and is on-brand, not a blank server default
- [ ] Mobile responsive across common breakpoints, no horizontal scroll
- [ ] No console errors in browser dev tools
- [ ] No exposed API keys, secrets, or leftover staging credentials (see `code-quality-launch.md`)
- [ ] No placeholder content shipped live: lorem ipsum, `$000`-style broken prices, example/stock data
- [ ] Cross-browser check: Chrome, Safari, Firefox, mobile Safari at minimum

## Phase 2: SEO fundamentals (see `seo-fundamentals.md`)
- [ ] Unique, real title tag and meta description on every page, correct length
- [ ] Canonical URL set correctly, points at the real production domain
- [ ] `robots.txt` allows the real pages, no leftover staging `Disallow: /`
- [ ] XML sitemap exists, accurate, ready to submit to Search Console
- [ ] One clear H1 per page, logical heading hierarchy
- [ ] Alt text on every meaningful image
- [ ] Structured data present, matches real content, validates without errors

## Phase 3: AEO/GEO readiness (see `aeo-geo.md`)
- [ ] llms.txt present and accurate, if the business wants AI-answer-engine visibility
- [ ] robots.txt stance on AI crawlers (GPTBot, ClaudeBot, PerplexityBot, etc.) is a deliberate choice
- [ ] FAQ content marked up with FAQPage schema where genuine Q&A exists
- [ ] Key facts stated clearly near the top of relevant sections, not buried under marketing language
- [ ] Critical content isn't hidden behind JS-only rendering

## Phase 4: Social share readiness (see `social-share-readiness.md`)
- [ ] `og:image` present, correct size, shows real content, not broken or placeholder
- [ ] Twitter Card tags present
- [ ] Full favicon set present (16x16, 32x32, apple-touch-icon, manifest, theme-color)
- [ ] Title/description tested in an actual platform preview tool, not just assumed correct

## Phase 5: Code and performance (see `code-quality-launch.md` here, and `technical-cro.md` in cro-review)
- [ ] Images optimized and correctly formatted
- [ ] CSS/JS minified for production
- [ ] Core Web Vitals in an acceptable range
- [ ] Analytics and conversion tracking installed, firing on the real conversion event, not just pageviews
- [ ] Redirects (www/non-www/http variants) all resolve cleanly to one canonical URL

## Phase 6: Conversion readiness (the full cro-review audit)
Run the complete process from `~/.claude/skills/cro-review/SKILL.md`, including its full reference library (checklist, converts-vs-doesnt, psychology, copywriting-formulas, benchmarks, page-type-playbooks, technical-cro, marketer-perspective, design-polish-tradeoffs, layout-eye-tracking, information-architecture, ads-platform-perspective, unbounce-specifics as applicable). Report its tiered findings as this phase's output rather than duplicating that logic here.

## Phase 7: Copy humanization pass (see `humanize-copy.md`)
Apply this to every piece of copy touched or suggested across every phase above, not as a separate pass at the end. Any rewritten headline, CTA, or FAQ answer proposed during phases 1 through 6 should already follow these rules by the time it's reported.

## Reporting this checklist
Don't just list problems. For each unchecked item, give the concrete next action needed to check it off. At the end, produce a short, ordered "do these in this order" action plan pulling the actual blockers from every phase into one sequence, since a phase-by-phase checklist alone doesn't tell someone which single next thing to do first.
