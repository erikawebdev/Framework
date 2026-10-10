# LolaBella Digital CSS Framework

A variable-driven CSS framework for Bricks Builder sites, modeled on Automatic.css (ACSS) naming. It gives you fluid type, spacing and radius scales, a color system, buttons, links, grid templates and a set of small utilities. You set it up per client in a browser-based guide.

## Files

| File | What it is |
| --- | --- |
| `framework.css` | The **defaults**. This is the starting point for every project. The guide reads it but never writes to it. |
| `framework-guide.html` | The visual guide and editor. It loads `framework.css`, shows every setting live, lets you change them, and downloads the result as a **new file you name** (e.g. `client-name.css`). |
| `build.py` | A helper script that serves the guide locally and checks or rebuilds `framework.css`. |
| `framework.css.bak` | The previous `framework.css`, saved automatically by `build.py --write`. |

## Quick start: CSS for a new client

1. Open a terminal in this folder and run:
   ```sh
   python3 build.py serve
   ```
   The guide opens at `http://127.0.0.1:8765/framework-guide.html`. (It has to be served this way, because a double-clicked HTML file isn't allowed to read `framework.css`.) Leave the terminal running, and press Ctrl-C when you're done.
2. Work through the guide's pages (Color, Typography, Spacing, Layout, Radius, Focus, Buttons, Links) and set them up for the client.
3. Type a file name in the box at the top (e.g. `acme-plumbing.css`) and click **Download CSS**. If no download is available, the CSS is copied to the clipboard instead.
4. Add that file to the client's Bricks site.

`framework.css` stays untouched, so the next project starts from the same defaults.

## Importing into Bricks natively

Instead of loading the CSS file, you can put the framework into Bricks' own Style Manager. Type a file name as above and click **Download for Bricks**. You get two files, named after the CSS file:

- `acme-plumbing-global.css`: element rules Bricks has no control for (resets, focus ring, links, header breakpoints). Paste it into **Bricks > Settings > Custom code > Custom CSS**.
- `acme-plumbing-bricks.json`: everything else, for an AI agent with the Bricks MCP connection to import. It contains:

| Key | Becomes in Bricks |
| --- | --- |
| `styleManager`, `breakpoints` | Style Manager root font size and fluid viewport range; the breakpoint widths |
| `scales` | Typography and spacing scale categories (headings, text, space, section space), from their inputs, so Bricks generates the steps. Each scale also lists the framework's own `clamp()` values, and any step pinned with `override`. |
| `palette` | A color palette: each color's base, light and dark steps (as shades) and hover |
| `variables` | Every other variable, grouped by category (transparencies, bridges, grids, button tokens and so on) |
| `classes` | One global class per framework class, with its CSS |
| `themeStyle` | Body and h1–h6 typography and section padding, for a site-wide theme style |

Your browser may ask once whether this site can download multiple files; allow it to get both.

Use one or the other on a site, not both, or every rule is defined twice.

## Changing the defaults

- **To change a value:** edit `framework.css` directly, then reload the guide to see the change.
- **To change the generator** (for example, adding a section or a setting in `framework-guide.html`), bring `framework.css` up to date afterwards:
  ```sh
  python3 build.py            # preview: shows what a rebuild would change, writes nothing
  python3 build.py --write    # applies it; the old file is saved as framework.css.bak
  ```
  If you didn't change the generator and `python3 build.py` still reports differences, the guide failed to read a setting back from `framework.css`. That's a bug in the guide.

The rebuild commands need Playwright:
```sh
pip install playwright && python3 -m playwright install chromium
```
`serve` doesn't need anything beyond Python 3.

## What's in framework.css

The sections appear in this order. Each one opens with a comment block that explains it.

| Section | Highlights |
| --- | --- |
| **Guide settings** | `--fw-*` inputs (viewport range, base sizes, ratios, breakpoints, gutters) that the guide rebuilds the scales from. They don't style anything directly. Unitless numbers are px, except ratios and multipliers. |
| **Header** | `--header-height-{xl,l,m,s}` and `--header-z-index` (these are only set in the CSS; the guide has no fields for them). `#brx-header.header-transparent` overlays the hero, `.hero-offset` keeps hero content clear of it, and anchor links clear a sticky header. |
| **Color** | `--primary`, `--secondary`, `--tertiary`, `--accent`, `--base`, `--neutral`, plus the status colors `--success`, `--warning`, `--danger` and `--info`. Each has hand-entered `-l-1…` / `-d-1…` steps, a `-hover`, and `-trans-10…90`. `--white`/`--black` also have trans steps. |
| **Typography** | Fluid `--h1…--h6` (anchored on h4) and `--text-xs…--text-xxl` (anchored on text-m), plus heading defaults, `.text--{size}` classes, text colors (`--text-dark`, `--text-light`, `-muted`) and `--text-width-xs…xl` (ch). |
| **Spacing** | Fluid `--space-xs…xxl`, `--section-space-xs…xxl`, `--gutter`, and bridge variables like `--space-l-to-s`. Contextual `--container-gap`, `--content-gap` and `--grid-gap`. |
| **Automatic spacing** | Applies a gap to `section` and `div` with zero specificity. Set `--auto-container-gap: 0` or `--auto-content-gap: 0` to turn it off. |
| **Layout** | `--content-width`, `--grid-1…12`, ratio grids (`--grid-1-2`, `--grid-3-1`, …) and responsive `--grid-auto-2…12`. Tune them with `--auto-grid-aggressiveness`. |
| **Utilities** | `.aspect-ratio-{1,4-3,3-4,3-2,2-3,16-9,9-16}` and `.list--none`. |
| **Radius** | Fluid `--radius-xs…xl`, `--radius-full`, and a contextual `--radius`. |
| **Smart spacing** | Spacing for content inside `.smart-spacing` (WYSIWYG or blog content): paragraphs, headings, lists, figures and blockquotes. |
| **Focus** | A `:focus-visible` ring set with `--focus-color`, `--focus-width` and `--focus-offset`. |
| **Clickable parent** | Put `.clickable-parent` on a card's link (or its heading) and the whole card becomes clickable, the same way it works in ACSS. |
| **Buttons** | `.btn--{color}`, `-light` and `-dark` for each brand color (not the status colors), combinable with `.btn--outline` and the size classes `.btn--xs…xxl`. Shared settings use `--btn-*` tokens. |
| **Links** | Styles every `<a>` with `--link-*` variables. `.link--{color}` (status colors included) works on the link itself or on any wrapper. |

## Conventions

- **Fluid values** use `clamp()` and scale between `--fw-viewport-min` (320px) and `--fw-viewport-max` (1366px).
- **Pinning a step:** to keep one generated value (e.g. `--h2`) from being recalculated, add a comment containing just the word `override` at the end of its line:
  ```css
  --h2: 2.5rem; /* override */
  ```
- **Low specificity:** sitewide defaults use `:where()`, so any class or ID set in Bricks overrides them.
- **Breakpoints** (`1366 / 992 / 768 / 480`, max-width) are written directly into media queries. CSS can't use variables there, so changing a breakpoint in the guide only shows up in the downloaded file, not in the guide's own preview.
