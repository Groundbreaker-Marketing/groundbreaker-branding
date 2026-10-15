# Dashboard kit

One look for every internal Groundbreaker dashboard: the same colors, the same type, and the
same header with our logo. Josh picked the "Forest Bar" direction on 2026-10-14; the app
picker rail (the "Suite Rail" idea) comes next, on top of this.

## What is in it

| File (in `dist/`) | What it is | Who uses it |
|---|---|---|
| `gbm-dash.js` | ES module for Workers and Pages Functions that render HTML strings: `DASH_CSS`, `BAR_CSS`, `FONT_LINKS`, the inline logos, `bar()` and `tabs()` | Ops, Finance, Leads, Onboarding and Access functions |
| `gbm-dash.css` | Page tokens (light and dark) plus the bar and tabs | Onboarding's static page |
| `gbm-bar.css` | The bar and tabs alone, with namespaced `--gbm-*` tokens, for a page that keeps its own palette | Access (client-facing) |
| `gbm-logo*.svg`, `gbm-mark*.svg` | Copies of `../logos` | Reviews |

Sources live in `src/` (`tokens.css`, `bar.css`, `chrome.css`) and `../logos/`. `dist/` is built,
not committed (`sync.mjs` builds it first). Never edit a consumer's copy by hand.

## The header

```js
import { DASH_CSS, FONT_LINKS, bar, tabs } from './gbm-dash.js';

const html = `<!doctype html><html lang="en"><head>…${FONT_LINKS}<style>${DASH_CSS}${APP_CSS}</style></head><body>
${bar({ app: 'Ops', user: user.name, signOut: '/cdn-cgi/access/logout' })}
${tabs([{ href: '/', label: 'My work', on: true }, { href: '/triage', label: 'Triage', badge: 3 }])}
<main>…</main></body></html>`;
```

- `bar({ app, home, user, signOut, signOutLabel, right })`. `right` is trusted HTML from the
  app (filters, a refresh button); everything else is escaped.
- The logo is inline SVG, so it works under a strict CSP (`img-src` does not need to allow
  anything). Below 560px wide the full logo swaps to the GM mark.
- Fonts: DM Sans from Google Fonts, the same face as groundbreakermarketing.com. A page's CSP
  needs `style-src https://fonts.googleapis.com` and `font-src https://fonts.gstatic.com`.

Static page, same markup by hand: copy the `<header class="gbm-bar">…</header>` that `bar()`
returns (run `node -e "import('./dist/gbm-dash.js').then(m=>console.log(m.bar({app:'Name'})))"`).

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
