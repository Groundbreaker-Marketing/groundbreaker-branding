// Builds dist/ from src/ and ../logos. Run after any change: node dashboard-kit/build.mjs
// dist/gbm-dash.css  for static dashboard pages: page tokens + the bar (link it, or paste it into a <style>)
// dist/gbm-bar.css   the bar alone, for pages that keep their own palette (client-facing pages)
// dist/gbm-dash.js   for Workers and Pages Functions that render HTML strings (no browser JS)
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const kit = JSON.parse(readFileSync(join(here, 'kit.json'), 'utf8'));
const read = (p) => readFileSync(join(here, p), 'utf8').trim();
const min = (css) => css.replace(/\/\*[\s\S]*?\*\//g, '').replace(/\n\s*/g, '\n').replace(/\n+/g, '\n').trim();
// Inline copies: no role/label (the link around them carries the name), a class for CSS.
const inline = (file, cls) => read(file).replace(' role="img" aria-label="Groundbreaker Marketing"', ` class="${cls}" aria-hidden="true" focusable="false"`);

const banner = `Groundbreaker dashboard kit v${kit.version}. Generated from groundbreaker-branding/dashboard-kit; do not edit here. Change the kit, then run its sync.`;
const barCss = `${min(read('src/bar.css'))}\n${min(read('src/chrome.css'))}`;
const css = `${min(read('src/tokens.css'))}\n${barCss}`;
const fonts = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,400..800&display=swap">';

const js = `// ${banner}

export const KIT_VERSION = ${JSON.stringify(kit.version)};
export const FONT_LINKS = ${JSON.stringify(fonts)};
export const DASH_CSS = ${JSON.stringify(css)};
export const BAR_CSS = ${JSON.stringify(barCss)};
export const LOGO_REVERSE = ${JSON.stringify(inline('../logos/gbm-logo-reverse.svg', 'gbm-logo'))};
export const MARK_REVERSE = ${JSON.stringify(inline('../logos/gbm-mark-reverse.svg', 'gbm-mark'))};
export const LOGO_COLOR = ${JSON.stringify(inline('../logos/gbm-logo.svg', 'gbm-logo'))};

const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

// The Forest Bar. \`right\` is trusted HTML from the app (filters, buttons); everything else is escaped.
export function bar({ app, home = '/', user = '', signOut = '', signOutLabel = 'Sign out', right = '' }) {
  const who = user ? \`<span class="gbm-user">\${esc(user)}</span>\` : '';
  const out = signOut ? \`<a href="\${esc(signOut)}">\${esc(signOutLabel)}</a>\` : '';
  const side = right || who || out ? \`<div class="gbm-right">\${right}\${who}\${out}</div>\` : '';
  return \`<header class="gbm-bar"><a class="gbm-brand" href="\${esc(home)}" aria-label="Groundbreaker Marketing \${esc(app)}, home">\${LOGO_REVERSE}\${MARK_REVERSE}<span class="gbm-sep"></span><span class="gbm-app">\${esc(app)}</span></a>\${side}</header>\`;
}

// Section tabs. items: [{ href, label, on, badge }]
export function tabs(items, label = 'Sections') {
  const a = (t) => \`<a href="\${esc(t.href)}"\${t.on ? ' class="on" aria-current="page"' : ''}>\${esc(t.label)}\${t.badge ? \` <span class="badge">\${esc(t.badge)}</span>\` : ''}</a>\`;
  return \`<nav class="gbm-tabs" aria-label="\${esc(label)}">\${items.map(a).join('')}</nav>\`;
}
`;

mkdirSync(join(here, 'dist'), { recursive: true });
writeFileSync(join(here, 'dist/gbm-dash.css'), `/* ${banner} */\n${css}\n`);
writeFileSync(join(here, 'dist/gbm-bar.css'), `/* ${banner} */\n${barCss}\n`);
writeFileSync(join(here, 'dist/gbm-dash.js'), js);
for (const f of ['gbm-logo.svg', 'gbm-logo-reverse.svg', 'gbm-mark.svg', 'gbm-mark-reverse.svg']) writeFileSync(join(here, 'dist', f), read(`../logos/${f}`) + '\n');
console.log(`built dashboard kit v${kit.version}: dist/gbm-dash.css (${css.length} B), dist/gbm-dash.js`);
