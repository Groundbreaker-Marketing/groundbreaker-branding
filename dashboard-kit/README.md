# Dashboard kit

One look for every internal Groundbreaker dashboard: the same colors, the same type, and the
same header with our logo. Josh picked the "Forest Bar" direction on 2026-10-14, then the app picker
rail from the "Suite Rail" idea on top of it (v1.1.0).

## What is in it

| File (in `dist/`) | What it is | Who uses it |
|---|---|---|
| `gbm-dash.js` | ES module for Workers and Pages Functions that render HTML strings: `DASH_CSS`, `BAR_CSS`, `FONT_LINKS`, `FAVICON_LINKS`, the inline logos, `APPS`, `appsFor()`, `bar()` and `tabs()` | Ops, Finance, Leads, Website & SEO, Social & Video, Contracts, Security, Onboarding and Access functions |
| `gbm-dash.css` | Page tokens (light and dark) plus the bar and tabs | Onboarding's static page |
| `gbm-bar.css` | The bar and tabs alone, with namespaced `--gbm-*` tokens, for a page that keeps its own palette | Access (client-facing) |
| `gbm-logo*.svg`, `gbm-mark*.svg` | Copies of `../logos` | Reviews |
| `gbm-favicon.svg`, `gbm-favicon-32.png`, `gbm-touch-icon.png` | The GM favicon as files, for static pages (`FAVICON_FILE_LINKS` links them) | Onboarding and Access static pages |

Sources live in `src/` (`tokens.css`, `bar.css`, `chrome.css`) and `../logos/`. `dist/` is built,
not committed (`sync.mjs` builds it first). Never edit a consumer's copy by hand.

## The header

```js
import { DASH_CSS, FONT_LINKS, FAVICON_LINKS, bar } from './gbm-dash.js';

const html = `<!doctype html><html lang="en"><head>…${FAVICON_LINKS}${FONT_LINKS}<style>${DASH_CSS}${APP_CSS}</style></head><body>
${bar({ app: 'Ops', user: user.name, signOut: '/cdn-cgi/access/logout',
        tabs: [{ href: '/', label: 'My work', on: true }, { href: '/triage', label: 'Triage', badge: 3 }] })}
<main>…</main></body></html>`;
```

- `bar({ app, home, user, signOut, signOutLabel, right, current, email, tabs })`. `right` is trusted
  HTML from the app (filters, a refresh button); everything else is escaped.
- **The header is sticky** (v1.2.0, Josh 2026-10-17): the logo, the Apps menu and the section tabs
  stay on screen while the page scrolls. Pass the tabs to `bar()` as `tabs` (the items `tabs()`
  takes, or the HTML it returned when you need its second argument) rather than printing `tabs()`
  after the bar: `bar()` wraps both in one `<div class="gbm-top">`, so they stick together whatever
  height the bar wraps to. `--gbm-top-h` is about the header's height: the kit sets
  `scroll-padding-top` from it so `#anchor` jumps land below the header, and a page's own sticky
  element sits under it with `top: calc(var(--gbm-top-h) + 12px)`. Sticky needs the page itself to
  scroll, so never set `overflow` on both `html` and `body`.
- **Favicon**: `FAVICON_LINKS` goes in every page's `<head>`. It is the GM mark (the G turns white on
  a dark browser theme) inline as `data:` URIs, so it needs no route and works under each
  dashboard's CSP (each allows `img-src data:`). Static pages use `FAVICON_FILE_LINKS`, which links
  the three files `sync.mjs` copies beside them.
- The logo is inline SVG, so it works under a strict CSP (`img-src` does not need to allow
  anything). Below 560px wide the full logo swaps to the GM mark.
- Fonts: DM Sans from Google Fonts, the same face as groundbreakermarketing.com. A page's CSP
  needs `style-src https://fonts.googleapis.com` and `font-src https://fonts.gstatic.com`.

## The app picker

Pass `current` (the app's id in `apps.json`) and the signed-in `email` to `bar()` and it adds the
picker: a rail down the left on screens 900px and wider, an "Apps" menu in the bar on narrower
ones. Put what `bar()` returns directly inside `<body>`: the rail is a fixed column, and
`body:has(> .gbm-rail)` pads the page right by its width, so no wrapper and no script (Ops' CSP
forbids scripts). Keep `<body>` free of horizontal padding of its own; give it to the content.

**Who sees what is read from each app's own gate.** `apps.json` names the file and variable that
gate each app (Finance's `ALLOWED_EMAILS`, Leads' `ADMIN_EMAILS`, and so on) and the build reads
them, so the picker can never offer an app its gate would refuse. The gates stay the security; the
picker only hides links. The build prints who sees each app. Ops is the exception: its gate is
Cloudflare Access plus its People page, neither a file, so `apps.json` declares the domain.

When someone changes an allowlist, rebuild and sync: `node dashboard-kit/sync.mjs --check` lists
every dashboard whose copy is now behind. Adding an app: an entry in `apps.json` with its gate,
then sync and ship every consumer so the new link shows up everywhere.

Static page, same markup by hand: copy the `<header class="gbm-bar">…</header>` that `bar()`
returns (a bare bar is sticky too), plus `FAVICON_FILE_LINKS` in the `<head>` (run `node -e "import('./dist/gbm-dash.js').then(m=>console.log(m.bar({app:'Name'})))"`).

## Rules

- The bar is forest in both themes (`--gbm-bar`). `--forest` itself turns lime in dark mode,
  because pages use it as the accent and link color.
- Lime is a fill. Lime text only on forest or in dark mode; on light screens use `--lime-ink`.
- Good, warning, critical and info mean state only. Brand colors never signal status.
- The bar and tabs never carry page content: titles, KPIs and filters that belong to the page
  stay in the page.

## Changing the kit

1. Branch, edit `src/` or `../logos/`, bump `version` in `kit.json`.
2. `node dashboard-kit/build.mjs` rebuilds `dist/` if you want to look at it.
3. PR, merge.
4. `node dashboard-kit/sync.mjs` writes the new files into every consumer listed in
   `kit.json` (`--only=<repo>` for one, `--check` to see who is behind without writing). Then
   ship each consumer the normal way: branch, PR, merge, and its deploy (the `deploy` field in
   `kit.json` says how; Ops, Finance and Leads deploy by hand with wrangler).
