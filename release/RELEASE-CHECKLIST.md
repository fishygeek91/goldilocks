# Release checklist — Goldilocks + TunnelVision go public

State on 2026-09-13: paper polished, novelty-cleared (NOVELTY-CHECK-03),
secret-scanned clean, MIT licensed both repos. Three commits unpushed.

## 1. Push (you, from your terminal)
- [ ] `cd goldilocks && git push`   (3ca3b63 polish, 851dc08 license, c7a37e3 cite, + release-prep commit)

## 2. Zenodo deposit with reserved DOI (you, ~15 min, zenodo.org)
- [ ] Log in (GitHub login works) → New upload
- [ ] Click "Reserve DOI" — copy the DOI (10.5281/zenodo.XXXXXXX)
- [ ] Fill metadata from `.zenodo.json` in the repo root (title, description,
      creator, keywords, related identifiers, license MIT, type: preprint)
- [ ] Do NOT publish yet — save draft
- [ ] Tell Claude the reserved DOI → Claude puts it in main.tex data
      availability, rebuilds, commits
- [ ] Upload files: paper/main.pdf (rebuilt with DOI),
      goldilocks-vX.zip + tunnelvision-vX.zip (Claude builds these:
      `git archive` of each repo at the release tag)
- [ ] Publish the deposit — DOI goes live

## 3. Tag + flip public (either of us with your approval)
- [ ] Tag both repos v1.0.0, push tags
- [ ] READMEs: result stated in first paragraph, DOI badge, cross-links
      (Claude drafts)
- [ ] GitHub → Settings → change visibility → Public (both repos)

## 4. GitHub Pages landing page (Claude builds; serve from goldilocks)
- [ ] docs/ or gh-pages branch: abstract, key figure, PDF link, Zenodo DOI,
      repo links, BibTeX snippet; enable Pages in repo settings
- [ ] Later: QMCMC-Bench gets its own Pages site (protocol, instances,
      reference results, audit checklist)

## 5. PRX Quantum submission (you, journals.aps.org)
- [ ] New submission → PRX Quantum; upload main.tex, refs.bib/bbl, figures
- [ ] Popular summary: paper/popular_summary.txt (already written)
- [ ] Cover letter: Claude drafts
- [ ] Suggested referees: qe-MCMC citers (Claude proposes a list)
- [ ] Data availability now points at the live DOI — consistent

## Parallel, optional
- [ ] Endorsement email to a qe-MCMC follow-up author (Claude drafts);
      if arXiv unlocks within a week, post there before journal submission
      and add the arXiv ID everywhere
