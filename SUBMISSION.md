# DesignerDuo Agent Skills submission guide

This file contains the materials needed to submit the skills-only plugin to the
OpenAI Plugin Directory. Account permissions, identity verification, policy
URLs, country availability, and final attestations must be completed by the
verified publisher in the OpenAI Platform.

## Package

- **Plugin ID:** `designerduo-agent-skills`
- **Version:** `0.1.0`
- **Submission type:** Skills only
- **Bundle:** `dist/designerduo-agent-skills-0.1.0.zip`
- **Manifest:** `plugins/designerduo-agent-skills/.codex-plugin/plugin.json`
- **Source:** `https://github.com/nepdud/skills`

## Listing copy

### Name

DesignerDuo Agent Skills

### Short description

Launch audits, Marketo development, and social writing in Subash's voice.

### Long description

DesignerDuo Agent Skills bundles three reusable workflows. DuoReview performs
phase-by-phase pre-launch audits across technical readiness, SEO, AEO/GEO,
social sharing, code quality, and conversion. Marketo helps build and debug
Adobe Marketo Engage landing-page templates and Forms 2.0 integrations. Social
Persona writes and edits X and LinkedIn content in Subash Dharel's established
voice. The plugin contains instructions, reference material, and one local
validation script. It does not connect to an MCP server or external account.

### Category

Productivity

### Website and support

- **Website:** `https://github.com/nepdud/skills`
- **Support:** `https://github.com/nepdud/skills/issues`

The publisher must add public privacy-policy and terms-of-service URLs before
submission. Those URLs should accurately state that this skills-only plugin has
no MCP server, authentication flow, or independent data collection.

## Starter prompts

1. Run a complete pre-launch review of this site.
2. Help me build or troubleshoot a Marketo landing page.
3. Rewrite this social post in my voice.

## Positive test cases

The portal requires at least five positive cases. Expected behavior should be
specific enough for a reviewer to confirm that the correct skill activated.

### 1. Complete launch audit

**Prompt:** Review this landing page before I launch it and give me the fixes in
the order I should make them.

**Expected:** Activates `duo-review`, evaluates all six phases, identifies
launch blockers, and returns a phase-by-phase checklist plus an ordered plan.

### 2. SEO-only audit

**Prompt:** Run the SEO phase of DuoReview on this page.

**Expected:** Activates `duo-review`, loads the master checklist and SEO
reference, limits findings to SEO, and returns a focused action list.

### 3. Marketo template architecture

**Prompt:** Build a responsive two-column Adobe Marketo landing-page template
with editable text, images, colors, and a native form.

**Expected:** Activates `marketo`, recommends a Guided template, uses valid
`mkto*` declarations with unique IDs, and supplies testable template code.

### 4. Marketo validation problem

**Prompt:** My Marketo template says "Invalid tags" and the editor reports a
missing `mktoContent` element. Help me fix it.

**Expected:** Activates `marketo`, recognizes the Free-Form requirement,
explains where `mktoContent` belongs, and recommends local and Design Studio
validation.

### 5. Social rewrite

**Prompt:** Rewrite this LinkedIn announcement in my voice: "I'm thrilled to
announce our next AI Conf Asia event and grateful for the journey."

**Expected:** Activates `social-persona`, removes generic LinkedIn language,
uses Subash's concise voice, and avoids prohibited constructions and wording.

### 6. Short X thread

**Prompt:** Write an X thread about why polished visual design cannot rescue a
confusing conversion path.

**Expected:** Activates `social-persona`, produces no more than three posts,
uses concrete CRO reasoning, and passes the skill's voice and slop checks.

## Negative test cases

### 1. General programming task

**Prompt:** Write a Python function that sorts a list of integers.

**Expected:** None of the bundled skills activates because the task does not
involve a launch audit, Marketo, or Subash's social voice.

### 2. Generic Adobe application question

**Prompt:** How do I crop an image in Adobe Photoshop?

**Expected:** The `marketo` skill does not activate merely because Adobe is
mentioned.

### 3. Long-form private document

**Prompt:** Draft a formal internal HR policy for employee leave.

**Expected:** The `social-persona` skill does not activate because the request
is neither social content nor a request to write in Subash's voice.

## Release notes

Initial release. Bundles DuoReview, Marketo, and Social Persona as a validated
skills-only plugin for ChatGPT and Codex. Includes launch-audit references,
Marketo implementation and troubleshooting references, and a Marketo template
validator. No MCP server, external authentication, or third-party data
connection is included.

## Publisher checklist

- [ ] Confirm Apps Management: Write access in the publishing organization.
- [ ] Complete individual or business identity verification.
- [ ] Provide a production-ready square logo.
- [ ] Publish a support page or confirm the GitHub Issues URL.
- [ ] Publish an accurate privacy policy and copy its HTTPS URL.
- [ ] Publish terms of service and copy its HTTPS URL.
- [ ] Select the intended countries or regions.
- [ ] Review all required policy attestations.
- [ ] Upload the ZIP under a Skills only submission.
- [ ] Run the positive and negative test cases in the portal.
- [ ] Submit the draft for OpenAI review.
