# Portfolio SEO and machine-readability audit

Audit date: 5 October 2026. Source baseline: `6531902`.

## Architecture and source of truth

The portfolio uses Jekyll/al-folio, Liquid layouts, Markdown pages, and a
`projects` collection. GitHub Actions builds static HTML and publishes `_site`
to GitHub Pages at https://adamkaniasty.com. No SPA conversion is necessary.
`assets/json/resume.json` is the current professional record; the latest commit
updates Google, Box, education, Mi-Crow, and xLungs. The live homepage inspected
during this audit still describes Box and undergraduate study. Deployment is
needed to reconcile the public site with the repository.

## Prioritized findings before changes

| Priority | Finding                                                                                                                                  | Resolution                                                                                       |
| -------- | ---------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| CRITICAL | Template news can publish placeholder claims; CV fallback contains Einstein's biography.                                                 | Exclude sample news, replace its landing page with real updates, remove fictional fallback data. |
| HIGH     | Old PDF calls APPI and Nokia current and the bachelor's degree expected.                                                                 | PDF and download presentation remain unchanged at Adam’s explicit request.                       |
| HIGH     | Open Graph and JSON-LD are disabled; the dormant schema reads identity links from inconsistent config and does not establish one Person. | Enable metadata and generate one connected entity graph from current data.                       |
| HIGH     | Homepage is a short biography with little technical evidence or project navigation.                                                      | Add a concise focus statement, selected projects, experience, research, and teaching links.      |
| HIGH     | Only three projects have pages, and Marketplace has a filename-derived URL.                                                              | Add supported case studies, explicit canonical slugs, and a legacy alias.                        |
| MEDIUM   | CV, home, project pages and publications are poorly cross-linked.                                                                        | Link résumé entries, project case studies, research and talks.                                   |
| MEDIUM   | Portrait alt text is a filename; cards nest links; CV headings skip levels.                                                              | Correct semantics, image dimensions, heading hierarchy, focus and skip navigation.               |
| MEDIUM   | 404 redirects to home; sitemap can include thin archives and sample pages.                                                               | Keep a genuine noindex error document; exclude duplicates and samples from the sitemap.          |
| MEDIUM   | Math, masonry and publication badge scripts load on pages that do not need them.                                                         | Gate optional scripts and use the existing responsive grid.                                      |
| LOW      | Empty verification tags and conflicting Kaggle identifiers are present.                                                                  | Emit verification only with a token; omit Kaggle until confirmed.                                |

## Evidence and unresolved content

- Current employment and education: latest repository résumé and homepage.
- Mi-Crow: [source](https://github.com/mi-crow-team/Mi-Crow) and
  [documentation](https://mi-crow-team.github.io/Mi-Crow/).
- Medical imaging paper: [AIS publication record](https://aisel.aisnet.org/isd2014/proceedings2025/transformation/28/),
  DOI 10.62036/ISD.2025.112; all authors and poster type verified. Published
  measurements describe the research team's system, not Adam's individual results.
- RL Doom: [repository](https://github.com/AdamKaniasty/RL-Doom), identifies Adam
  as project leader and describes PPO/A2C, scenarios, metrics and qualitative outcomes.
- CanSat: [repository](https://github.com/AdamKaniasty/Picture-Segmentation)
  says 2019/2020 and ResNet18; résumé/PDF say 2022 and ResNet12. New case study
  uses the repository implementation and omits competition dates and awards;
  historical résumé assertions need Adam's confirmation. The award is preserved without its disputed year.
- `MIFlow` appears in the résumé. Do not silently change it to MLflow without
  confirmation. Describe model registries generically in the case study.
- APPI and Nokia implementation descriptions are first-person portfolio records.
  No specific public repository, benchmark, confidential details or production
  outcome is inferred. Synapse and Marketplace remain distinct applications.
- Missing: APPI public links/screenshots; autoscaling evaluation and publishable
  architecture; talk event dates/slides; precise individual Mi-Crow contributions.
- Kaggle handles differ between `_config.yml` and `_data/socials.yml`; omit from
  identity markup and visible social links until ownership is confirmed.

## Crawler policy

The original wildcard policy already allowed crawling. Keep that policy and the
absolute sitemap reference rather than adding redundant bot-specific groups.
Googlebot, Bingbot and OAI-SearchBot are allowed. This also preserves the existing
GPTBot policy; search and training controls are independent. Robots rules are
not access controls. Source/internal audit files are excluded from the build.

Documentation checked on the audit date:
[OpenAI crawlers](https://developers.openai.com/api/docs/bots),
[Google robots specification](https://developers.google.com/crawling/docs/robots-txt/robots-txt-spec),
[Bing robots guidance](https://www.bing.com/webmasters/help/how-to-create-a-robots-txt-file-cb7c31ec).

## Implemented validation

The locked production build succeeds. The crawler checker verifies 21 generated
HTML pages and 16 indexable URLs, unique titles/descriptions, canonical URLs,
JSON-LD, project facts, local links and fragments, sitemap and robots permissions.
The existing navbar check verifies 20 home links. Ruby syntax, whole-repository
Prettier formatting and whitespace checks pass. CSS compression is handled by
Sass and the vendor styles; disabling redundant compression avoids a build stall.
The unused example notebook is excluded, and the existing search data template
is now explicitly included in the build. The Lighthouse workflow now targets
this portfolio rather than the al-folio demo.

Browser validation covers desktop, tablet and mobile layouts, navigation,
search, dark mode and keyboard skip navigation. Axe found no WCAG A/AA
violations on 12 pages, including every project case study. Initial homepage script references
fall from 26 to 18. Local loading measurements are only a lab smoke check;
real-user LCP, CLS and INP still require deployed field data. The PDF file and its
presentation remain unchanged at Adam's explicit request.

## External follow-through

Build with the locked bundle, run `_scripts/check_navbar_links.py` and
`_scripts/check_seo.py` against generated HTML, check formatting, and inspect
desktop/mobile layouts. This verifies static extraction, metadata, JSON-LD,
internal targets, crawler permissions and sitemap consistency; it cannot prove
ranking, AI citation frequency or real-user Core Web Vitals.

After deployment: submit `/sitemap.xml` in Google Search Console and Bing
Webmaster Tools; inspect/request indexing for the home, project and publication
URLs; verify the live 404 status and any host redirects. Add backlinks from
owned project READMEs/documentation and research profiles to their case studies.
Align LinkedIn's current role/education with the confirmed résumé. Check host/CDN
access for OAI-SearchBot if a firewall is added. Do not invent verification tokens.
