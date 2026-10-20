# Profile visual maintenance

The profile keeps its original section order, TypeScript introduction, project, technology collection, statistics, snake and achievements. Original `Banner.png` remains available; the profile now uses lightweight custom SVG artwork.

## Design

Midnight `#0d1729`, panel `#17263d`, line `#283e59`, cyan `#54d9ed`, periwinkle `#a5adff`, text `#eef4ff`. Verdana/system sans in artwork; Fira Code in the typing service; native GitHub code highlighting. SVGs use viewBox sizing, no scripts, external fonts or foreignObject. Header, divider and footer have slow opacity motion and a reduced-motion media query. GitHub's image proxy and viewer settings may affect animation. Dark artwork intentionally keeps its own contrast in either GitHub theme.

## Data and refresh

`scripts/generate-stats.py` uses only Python's standard library and the GitHub REST/GraphQL APIs. Run with `GH_TOKEN` set to an authenticated token; never commit a token. Public non-fork repositories determine stars and language bytes. Percentages use all returned language bytes; the six largest are shown. Contributions use GitHub's past-year calendar; the longest streak is limited to that window. A zero-contribution current UTC day does not prematurely end yesterday's streak. This is not an all-time or private-repository metric.

The workflow runs daily at 05:17 UTC, on manual dispatch, and when its source changes on main. It updates dated stats in main and publishes the two snake variants to output. Actions are pinned to immutable revisions; only the refresh job has contents write permission. No third-party service receives a personal token. GitHub branch protection or disabled Actions can prevent refresh: permit bot updates using repository policy, or run manually and commit generated assets. A stale snapshot retains its timestamp.

## Owner attention

- Email was `YOUR_EMAIL@gmail.com`; the visible badge explicitly says not set and has no mailto link. Replace it with a real address when ready.
- LinkedIn was verified from the public GitHub profile: `stefan-penchev-31b94a318`.
- The Book Next Door is retained as a project from the original profile, not asserted to be actively maintained. Confirm current status before changing that wording.
- Current work is described conservatively; repository push dates alone cannot establish personal priorities.
- Trophy and activity graph hosts returned HTTP 402; the streak host returned HTTP 403 during inspection. Native GitHub achievements replace trophies. Repository-owned charts replace hosted statistics, streak and activity services.
- Profile views count visits seen by Komarev, not GitHub's official traffic analytics.
- The workflow has not been dispatched or pushed by this redesign. Its first hosted run must be checked after publishing; the existing output snake remains available meanwhile.

## Rendering checks

Use GitHub's Markdown API to render the README for a local preview. Check desktop and mobile widths, anchors, all image responses, and SVG XML validity. Local rendering approximates GitHub's layout; recheck the actual profile after publishing because image caching and sanitization are controlled by GitHub. No JavaScript, custom README CSS, hover effects, iframes or proficiency bars are required.

Validation completed locally: GitHub Markdown API rendered successfully; Chrome/Playwright at 1100px and 390px showed no document overflow and all images loaded on the final pass. Navigation anchors resolved and the Stack link scrolled to its section in dark and light previews. Custom SVG XML, generator syntax, workflow YAML and `git diff --check` passed. The generator ran against authenticated live API data. Hosted workflow execution remains untested until publication. Browser skill/plugin was unavailable; bundled Playwright with installed Chrome was used. A transient profile-view image load failure cleared on the final pass; external badges and typing remain availability dependencies.
