// Builds dist/ from src/ and ../logos. Run after any change: node dashboard-kit/build.mjs
// dist/gbm-dash.css  for static dashboard pages: page tokens + the bar (link it, or paste it into a <style>)
// dist/gbm-bar.css   the bar alone, for pages that keep their own palette (client-facing pages)
// dist/gbm-dash.js   for Workers and Pages Functions that render HTML strings (no browser JS)
// dist/gbm-favicon.svg, gbm-favicon-32.png, gbm-touch-icon.png   the GM favicon, for static pages
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const appsRoot = join(here, '../..'); // ~/apps: every gate file is a path under it
const kit = JSON.parse(readFileSync(join(here, 'kit.json'), 'utf8'));
const read = (p) => readFileSync(join(here, p), 'utf8').trim();
const dataUri = (p, type) => `data:${type};base64,${readFileSync(join(here, p)).toString('base64')}`;
const min = (css) => css.replace(/\/\*[\s\S]*?\*\//g, '').replace(/\n\s*/g, '\n').replace(/\n+/g, '\n').trim();
// Inline copies: no role/label (the link around them carries the name), a class for CSS.
const inline = (file, cls) => read(file).replace(' role="img" aria-label="Groundbreaker Marketing"', ` class="${cls}" aria-hidden="true" focusable="false"`);

// ── App picker: who sees each app, read from that app's own gate config ──────────────────
// A value is a JSON array ('["a@x","b@x"]') or a comma list ("a@x,b@x"), on one line.
function readVar(file, name) {
  const text = readFileSync(join(appsRoot, file), 'utf8');
  const m = text.match(new RegExp(`^\\s*${name}\\s*=\\s*(['"])(.*?)\\1\\s*(#.*)?$`, 'm'));
  if (!m) throw new Error(`${file}: ${name} not found (the app picker reads it to decide who sees the app)`);
  return m[2];
}
const list = (v) => (v.trim().startsWith('[') ? JSON.parse(v) : v.split(',')).map((s) => String(s).trim().toLowerCase()).filter(Boolean);
const registry = JSON.parse(readFileSync(join(here, 'apps.json'), 'utf8')).apps;
const apps = registry.map((a) => {
  let who = a.who || {};
  if (a.gate) {
    who = {};
    if (a.gate.emails) who.emails = list(readVar(a.gate.file, a.gate.emails));
    if (a.gate.domain) who.domain = readVar(a.gate.file, a.gate.domain).trim().toLowerCase();
  }
  return { id: a.id, name: a.name, url: a.url, who };
});

const banner = `Groundbreaker dashboard kit v${kit.version}. Generated from groundbreaker-branding/dashboard-kit; do not edit here. Change the kit, then run its sync.`;
const barCss = `${min(read('src/bar.css'))}\n${min(read('src/chrome.css'))}`;
const css = `${min(read('src/tokens.css'))}\n${barCss}`;
// The GM favicon. Workers carry it inline (data: URIs, so it needs no route and works under every
// dashboard's CSP: each allows img-src data:); static pages link the files sync.mjs copies beside them.
// The PNG is for browsers without SVG favicons; the touch icon is for an iPhone home screen.
const favicon = (svg, png, touch) => `<link rel="icon" href="${png}" sizes="32x32"><link rel="icon" href="${svg}" type="image/svg+xml"><link rel="apple-touch-icon" href="${touch}">`;
const faviconInline = favicon(dataUri('../logos/gbm-favicon.svg', 'image/svg+xml'), dataUri('../logos/gbm-favicon-32.png', 'image/png'), dataUri('../logos/gbm-touch-icon.png', 'image/png'));
const faviconFiles = favicon('/gbm-favicon.svg', '/gbm-favicon-32.png', '/gbm-touch-icon.png');
const fonts = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,400..800&display=swap">';

const js = `// ${banner}

export const KIT_VERSION = ${JSON.stringify(kit.version)};
export const FONT_LINKS = ${JSON.stringify(fonts)};
// The GM favicon for a page's <head>, inline. FAVICON_FILE_LINKS points at the synced files instead.
export const FAVICON_LINKS = ${JSON.stringify(faviconInline)};
export const FAVICON_FILE_LINKS = ${JSON.stringify(faviconFiles)};
export const DASH_CSS = ${JSON.stringify(css)};
export const BAR_CSS = ${JSON.stringify(barCss)};
export const LOGO_REVERSE = ${JSON.stringify(inline('../logos/gbm-logo-reverse.svg', 'gbm-logo'))};
export const MARK_REVERSE = ${JSON.stringify(inline('../logos/gbm-mark-reverse.svg', 'gbm-mark'))};
export const LOGO_COLOR = ${JSON.stringify(inline('../logos/gbm-logo.svg', 'gbm-logo'))};

// Who may open each app, read from each app's own allowlist when the kit was built.
export const APPS = ${JSON.stringify(apps)};

// The apps this email can open, in picker order. \`current\` (the app rendering the page) always
// stays in: the viewer is already inside it.
export function appsFor(email, current = '') {
  const e = String(email || '').trim().toLowerCase();
  const ok = (w) => !!e && (((w.emails || []).includes(e)) || (!!w.domain && e.endsWith('@' + w.domain)));
  return APPS.filter((a) => a.id === current || ok(a.who));
}

const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

// The Forest Bar. \`right\` is trusted HTML from the app (filters, buttons); everything else is escaped.
// Pass \`current\` (this app's id in APPS) and the signed-in \`email\` to add the app picker: an
// Apps menu in the bar and a rail after it (place the returned HTML as a direct child of <body>).
// It lists only the apps that email can open, and only when there are two or more.
// Pass the page's section \`tabs\` here too (the items for tabs(), or HTML tabs() already made) so
// the bar and tabs stick to the top of the screen together while the page scrolls.
export function bar({ app, home = '/', user = '', signOut = '', signOutLabel = 'Sign out', right = '', current = '', email = '', tabs: sections = '' }) {
  const who = user ? \`<span class="gbm-user">\${esc(user)}</span>\` : '';
  const out = signOut ? \`<a href="\${esc(signOut)}">\${esc(signOutLabel)}</a>\` : '';
  const side = right || who || out ? \`<div class="gbm-right">\${right}\${who}\${out}</div>\` : '';
  const mine = current ? appsFor(email, current) : [];
  const links = mine.map((a) => \`<a class="gbm-app-link\${a.id === current ? ' on" aria-current="page' : ''}" href="\${esc(a.url)}"><i></i>\${esc(a.name)}</a>\`).join('');
  const picker = mine.length > 1;
  const menu = picker ? \`<details class="gbm-apps"><summary>Apps</summary><nav class="gbm-apps-menu" aria-label="Groundbreaker apps">\${links}</nav></details>\` : '';
  const rail = picker ? \`<nav class="gbm-rail" aria-label="Groundbreaker apps"><div class="gbm-rail-in"><span class="gbm-rail-h">Apps</span>\${links}</div></nav>\` : '';
  const strip = Array.isArray(sections) ? tabs(sections) : sections;
  return \`<div class="gbm-top"><header class="gbm-bar"><a class="gbm-brand" href="\${esc(home)}" aria-label="Groundbreaker Marketing \${esc(app)}, home">\${LOGO_REVERSE}\${MARK_REVERSE}<span class="gbm-sep"></span><span class="gbm-app">\${esc(app)}</span></a>\${menu}\${side}</header>\${strip}</div>\${rail}\`;
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
for (const f of ['gbm-logo.svg', 'gbm-logo-reverse.svg', 'gbm-mark.svg', 'gbm-mark-reverse.svg', 'gbm-favicon.svg']) writeFileSync(join(here, 'dist', f), read(`../logos/${f}`) + '\n');
for (const f of ['gbm-favicon-32.png', 'gbm-touch-icon.png']) writeFileSync(join(here, 'dist', f), readFileSync(join(here, '../logos', f)));
console.log(`built dashboard kit v${kit.version}: dist/gbm-dash.css (${css.length} B), dist/gbm-dash.js`);
console.log('app picker (read from each gate):');
for (const a of apps) console.log(`  ${a.name.padEnd(15)} ${[a.who.domain ? '@' + a.who.domain : '', ...(a.who.emails || [])].filter(Boolean).join(', ') || 'nobody'}`);
