# Groundbreaker Branding

The comprehensive brand design system for Groundbreaker Marketing. This package contains design tokens, React components, and brand guidelines used across all marketing materials — websites, banners, signs, flyers, handouts, business cards, and more.

## Usage with Claude Design

To sync this design system with Claude Design:

```bash
cd /path/to/groundbreaker-branding
claude
/design-sync
```

Once synced, the design system will appear in **Design systems for everyone in your org** and can be used to generate branded materials in Claude Design.

## Structure

- **`tokens/`** — Design tokens (colors, typography, spacing, shadows, etc.)
- **`components/`** — React components that use the tokens
  - `Button` — CTA buttons (primary, secondary, tertiary variants)
  - `Card` — Content containers
  - `Typography` — Text components (headings, body, captions)

## Brand Colors

- **Primary**: #1c352b (Dark Forest Green)
- **Accent**: #cdec60 (Lime)
- **Supporting**: Gray scale (50–900)
- **Semantic**: Success, Warning, Error, Info

## Customization

To update fonts, colors, or other brand elements:

1. Edit `tokens/index.ts` with new values
2. Sync with Claude Design: `cd /path/to/groundbreaker-branding && claude && /design-sync`
3. Create a PR and merge via `flow ship` + `flow land`

## Logo Assets

Add logo files to a `logos/` directory. Provide variations:
- Primary lockup (horizontal and stacked)
- Icon/symbol only
- Monochrome versions (for single-color applications)
- Minimum clear space and sizing guidelines

_(Logos to be added by Ashley)_
