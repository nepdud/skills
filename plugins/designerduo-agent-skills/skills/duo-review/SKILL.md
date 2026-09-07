---
name: duo-review
description: "DuoReview: the full pre-launch readiness audit for a landing page, sales page, or site before it goes live. Covers technical foundation, SEO, AEO/GEO (AI answer-engine readiness), social share readiness (OG images, favicons, titles), code/performance hygiene, and the complete cro-review conversion audit, all in one pass. Produces a phase-by-phase go-live checklist plus an ordered step-by-step action plan, not just a list of findings. Trigger: /duo-review"
---

# DuoReview

The master pre-launch skill. Run this before a page or site goes live, not after. It answers "what am I missing before I ship this" across every dimension: is it technically sound, will search engines and AI answer engines find and understand it, will it look right when shared, is the code clean, and will it actually convert once people arrive.

This is broader than `cro-review`, which only covers conversion/CRO. DuoReview includes the full cro-review audit as one phase, on top of everything cro-review doesn't touch: technical launch blockers, SEO, AEO/GEO, social share readiness, and code hygiene.

## Usage

```
/duo-review                      # full pre-launch audit of the site/page in the current directory
/duo-review path/to/page.html    # audit a specific file
/duo-review https://example.com  # audit a live URL
/duo-review --phase seo          # narrow to one phase (technical, seo, aeo, social, code, conversion)
```

Default is the full phase-by-phase pass. Only narrow scope if the user asks for a specific phase.

`--phase` maps directly to one phase and its reference file, nothing else needs to load:

| `--phase` value | Phase | Reference file(s) |
|---|---|---|
| `technical` | 1 | (checklist only, no dedicated reference file) |
| `seo` | 2 | `seo-fundamentals.md` |
| `aeo` | 3 | `aeo-geo.md` |
| `social` | 4 | `social-share-readiness.md` |
| `code` | 5 | `code-quality-launch.md` |
| `conversion` | 6 | the full `cro-review` skill |

## Reference library

- **`pre-launch-checklist.md`** - the master ordered checklist tying every phase together. Read this first, it's the spine of the whole audit and defines the report structure.
- **`seo-fundamentals.md`** - title/meta description, canonical URLs, robots.txt, sitemap, heading structure, alt text, structured data, mobile-first indexing.
- **`aeo-geo.md`** - Answer Engine Optimization and Generative Engine Optimization: direct-answer formatting, FAQ schema, llms.txt, AI crawler access decisions, entity clarity, making content citable.
- **`social-share-readiness.md`** - Open Graph tags, Twitter Card tags, the full favicon/icon set, and how to actually test share previews instead of assuming the tags are correct.
- **`code-quality-launch.md`** - pre-launch code hygiene: debug artifacts, leftover placeholder content, exposed secrets, mixed content, redirects, third-party embed checks.
- **`humanize-copy.md`** - style rules for any copy suggested or rewritten during the audit. No em-dashes, no AI-tell phrasing, specific over vague, sounds like a person. Apply this to every copy suggestion across every phase, not as an afterthought.
- **The entire `cro-review` skill** (`~/.claude/skills/cro-review/`) - loaded in full as Phase 6. Read its `SKILL.md` and its full `references/` directory (checklist, converts-vs-doesnt, psychology, copywriting-formulas, benchmarks, page-type-playbooks, technical-cro, marketer-perspective, design-polish-tradeoffs, layout-eye-tracking, information-architecture, ads-platform-perspective, unbounce-specifics). Don't duplicate that logic here, run it and fold its tiered output into this report as its own phase.

## Process

1. **Identify the target.** Same as cro-review: find the real page/site in the current directory, or use the given path/URL. Read full source, not excerpts. Ask which page if there are multiple candidates.

2. **Load `pre-launch-checklist.md` first.** It defines the phase structure everything else plugs into. Always load this, even for a single-phase run, since it's the spine and is small.

3. **If `--phase` was passed, only load and run that one phase**, using the table above to know which single reference file (or, for `conversion`, which full skill) to load. Skip every other phase's reference file entirely, skip loading cro-review unless the phase is `conversion`, and skip step 4 below if the phase isn't `conversion`. Go straight to reporting that phase's checklist status plus a short action list scoped to it, no cross-phase action plan needed since there's only one phase in scope.

4. **Otherwise (full run), work through Phases 1 to 5** (technical foundation, SEO, AEO/GEO, social share, code/performance) using their matching reference files. For each checklist item: mark it done, missing, or needs-verification, and state the concrete next action for anything not done. Ground every check in what's actually in the source (quote the actual `robots.txt` line, the actual missing meta tag, the actual broken link), don't assume.

5. **Run Phase 6, the full cro-review audit**, by loading and following `~/.claude/skills/cro-review/SKILL.md`'s complete process against its complete reference library. Fold its tiered findings (quick-fix / more-work / polish) into this report as the Phase 6 section rather than re-deriving CRO logic independently.

6. **Apply `humanize-copy.md`** to every rewritten headline, CTA, or copy suggestion produced in any phase, including ones cro-review would normally produce. No em-dashes, no AI-tell phrasing, ever, in anything suggested to the user. This applies to single-phase runs too.

7. **Report as a phase-by-phase checklist** (full runs only, see step 3 for single-phase reporting), not a flat list of severity tiers. Structure:
   - Phase 1 through 5: checklist status per item, grouped by phase, blockers called out explicitly as "must fix before launch."
   - Phase 6: the cro-review tiered findings (quick-fix / more-work / polish), presented in cro-review's own format.
   - **A final ordered action plan**: pull the actual blockers and high-priority items from every phase into one single sequence, "do these in this order," so the user has one concrete next step instead of six separate checklists to mentally merge themselves. This is the "step by step strategy" the user asked for, don't skip it.

8. **Offer to apply fixes.** After reporting, ask whether to start executing the action plan directly, starting with the launch blockers.

## Notes

- This skill exists specifically so nothing gets missed before something goes live: a broken form, a missing OG image, a `noindex` tag left on from staging, or a weak headline can all sink a launch, and they're each invisible in a different way (only shows up when crawled, only shows up when shared, only shows up when a real visitor tries to convert). Check all of them in one pass rather than assuming any single check covers it.
- Never use em-dashes in any part of the report or in any suggested copy. See `humanize-copy.md`.
- If the user hasn't said what tool the page is built in or whether it'll run paid traffic, check cro-review's own process step 1 for those questions, this skill doesn't duplicate that logic, it inherits it by running cro-review's process in Phase 6.
- Keep the phase checklists concrete and grounded. "robots.txt line 3 has `Disallow: /`, remove it" beats "check your robots.txt."
