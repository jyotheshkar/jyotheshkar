> Retired 14 November 2026. These historical assets are no longer shown. The scheduled refresh workflow was removed when four qualitative skill circles replaced this layer. See [skill-circles.md](skill-circles.md).

# Contribution visuals

Two complementary repository-hosted SVGs show the past year of activity:

- `assets/contributions/contribution-3d.svg`: an isometric contribution calendar with contribution-type radar and language share, using [github-profile-3d-contrib](https://github.com/yoshi389111/github-profile-3d-contrib) at `e235d118909be71eb7edb05482a3de4e76156df3`.
- `assets/contributions/contribution-snake.svg`: an animated contribution trail, using [Platane/snk](https://github.com/Platane/snk) SVG-only at `d8f6715049803e982ee5ff501b6b9b7d5deeb09b` (v3).

The dark GitHub palette uses blue accents to match the portfolio canvas. The 3D landscape is static for clear reading; the snake respects reduced-motion preferences. Both carry accessible titles and descriptions. The snake is decorative, not a productivity score. The language share describes attributed commit contributions, not skill level.

## Data and refresh

The upstream actions query GitHub's contribution calendar and public profile data with the repository's automatic `GITHUB_TOKEN`. No personal access token or third-party image host is needed. The calendar reflects GitHub's own contribution rules and the account's public profile settings. It is a past-year window, not an all-time count; it may differ from a selected year in GitHub's native contribution display. Private repository names or contents are not exported.

The refresh workflow runs daily at 06:23 UTC, can be run manually, and runs when its workflow, configuration or SVG preparation script changes. Same-repository source-branch pushes can generate a preview before merging. Pull requests generate artifacts for review but cannot publish. Scheduled runs use the default branch. Only the two generated SVG paths are staged by the publishing job, and changes to those paths do not trigger another refresh.

Generation has read-only repository permission. A separate job, containing only pinned first-party checkout/download actions and the explicit two-file commit step, has write permission. Automated refresh commits use the GitHub Actions bot identity. They are maintenance updates rather than manual engineering contributions.

`scripts/prepare_contribution_visuals.py` rejects malformed SVGs, external resources, active content, duplicate IDs and unexpected dimensions before either asset is published. It adds a UTC capture date and accessibility metadata. If collection or validation fails, the publishing job does not run, leaving the previous successful visuals in place.

## Sources

The pinned upstream READMEs document token use, output names and color configuration:

- https://github.com/yoshi389111/github-profile-3d-contrib/blob/e235d118909be71eb7edb05482a3de4e76156df3/README.md
- https://github.com/Platane/snk/blob/d8f6715049803e982ee5ff501b6b9b7d5deeb09b/README.md

No upstream implementation is vendored. GitHub's built-in contribution graph remains available below the profile README.
