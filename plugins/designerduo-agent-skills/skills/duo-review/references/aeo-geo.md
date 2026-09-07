# AEO and GEO: being found by answer engines and AI

Two newer categories on top of traditional SEO. AEO (Answer Engine Optimization) is about getting pulled into featured snippets, People Also Ask boxes, and voice assistant answers. GEO (Generative Engine Optimization) is about getting cited, quoted, or summarized correctly by AI answer engines and chat assistants (ChatGPT, Perplexity, Google AI Overviews, Claude, and similar). Both reward clarity and structure over persuasion, since a machine is parsing the page, not just a person scrolling it.

## Direct-answer formatting
- Near the top of any section that answers a real question, state the direct answer in two or three plain sentences before going deeper. This is what gets lifted into a featured snippet or read back by a voice assistant, and it's also the easiest thing for an AI system to extract and summarize accurately.
- Don't bury the actual answer under three paragraphs of scene-setting first. Lead with it, then explain.

## FAQ and Q&A structure
- Genuine FAQ content should use `FAQPage` schema markup. This feeds Google's rich results and gives AI crawlers a clean, structured signal for what question maps to what answer.
- Write each FAQ answer so it stands alone and makes sense without the surrounding page context, since it may get pulled out and shown independently.

## llms.txt
- A plain-text file at the site root (`/llms.txt`) describing what the site or organization is and pointing to the key pages worth reading. This is an emerging convention some AI crawlers and agents use to quickly understand a site instead of parsing the whole thing.
- If one exists already, check it's accurate and not describing an old version of the offer or business. If none exists and the business wants AI visibility, it's a cheap, quick addition.

## AI crawler access is a decision, not a default
- Check `robots.txt` for how it treats AI-related crawlers (GPTBot, ClaudeBot, PerplexityBot, Google-Extended, CCBot, and others). Whatever the current setting is, it should be a deliberate choice, not whatever a template or CMS defaulted to.
- Allowing these crawlers means the content can be summarized or quoted by AI answer engines, sometimes without a click back to the site. Blocking them means the content likely won't show up in those answers at all. Neither is automatically right, it's a real trade-off between visibility and traffic capture, worth surfacing explicitly rather than deciding by accident.

## Entity clarity
- State clearly, in plain language near the top of the page, who this is, what it does, and who it's for. Structured data (`Organization` or `Person` schema) reinforces this for machine parsing.
- If there's a physical presence, keep name, address, and phone number (NAP) consistent everywhere they appear, since inconsistency undermines entity recognition for both search and AI systems.

## Make content citable
- Specific numbers, named case studies, and direct attributed quotes work better as citation material than vague marketing language, since answer engines tend to quote or cite concrete, well-attributed claims over generic ones. This is the same specificity principle from `psychology.md`, doing double duty here.
- A visible last-updated date or clearly dated content can factor into how confidently some answer engines treat information as current.

## Don't hide the important content behind JavaScript
- If key facts only render after heavy client-side JavaScript execution, some crawlers, including some AI crawlers, may never see them. Server-rendered or static HTML for the core facts (what the offer is, the price, who it's for) is the safer bet.

## Off-page signals still matter
- Being mentioned or cited on other authoritative sites (press coverage, review platforms, industry directories) feeds both traditional SEO authority and the corpus AI systems draw from. This is slower to build than on-page fixes, but worth naming as its own category rather than assuming on-page work alone covers it.

## How to use this during an audit
Check whether the page states its core facts in clear, extractable, machine-parseable form near the top of relevant sections, whether FAQ content has schema, whether llms.txt exists and is accurate, and whether the robots.txt stance on AI crawlers was a real decision. Flag JavaScript-hidden critical content as a specific risk for both AEO and GEO visibility.
