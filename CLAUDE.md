# Groundbreaker Branding — Git Workflow (Claude Code: follow this automatically)

These are standing instructions for **Claude Code**. 
This repo lives in the **`Groundbreaker-Marketing`** GitHub org and we collaborate by
pushing/pulling to it, so never let local work clobber a teammate's.

There is a helper script at `~/apps/playbooks/git-workflow/flow.sh` (usually aliased as `flow`).
Prefer it; if it's missing, run the equivalent git/gh commands shown in parentheses.

## Before you change ANY files in this repo
1. Get on the latest default branch: `flow sync`  (≈ `git checkout main && git pull --ff-only`).
2. **Create a working branch before editing** — never edit or commit on `main`:
   `flow start <short-description>`  (≈ `git checkout -b <user>/<short-description>`).
   If the user starts asking for changes while you're still on `main`, make the branch FIRST,
   then proceed — and briefly tell them you did.

## While working
- Commit logical chunks: `flow save "message"`  (≈ `git add -A && git commit -m "message"`).

## When the work is ready
- Open a PR, then merge it: `flow ship` then `flow land`
  (≈ push the branch, `gh pr create`, then `gh pr merge --squash --delete-branch`).
- `flow ship` automatically syncs the branch with `main` first, so the PR shows only real changes.

## Hard rules (never violate)
- **Never commit directly to `main`.** Always work on a branch and merge via a PR.
- **Never `git push --force` / `-f`** on a shared branch (especially `main`).
- **Never discard a teammate's work.** On a merge conflict, stop and resolve it carefully
  (or ask the user) — never `reset --hard` away changes you didn't create.
- If a pull won't fast-forward, stop and reconcile; don't force it.

## Note
Branch protection on `main` is **ENABLED** for every org repo: GitHub rejects direct
pushes and force-pushes to `main` — all changes must land via a Pull Request. The workflow above
isn't just convention; it's enforced.


## Copywriting standards (Claude: apply to ALL client-facing copy, every client)

Standing rules from Josh (2026-08-19). They apply to every piece of client-facing
text we write anywhere: site pages, navigation labels, meta titles and
descriptions, photo alt text, strings in data files, GBP posts, and review
replies. Follow them without being asked.

- **No em dashes ( — ) in copy.** Rewrite the sentence with a period, colon,
  comma, or semicolon instead; for label-price pairs use a middot
  (e.g. "Specialty Bar · $23/guest").
- **US spellings only.** organized, license, honored, personalized, favorites,
  centerpiece, canceled/canceling. Never organised, licence, honoured, colour,
  favourite, centrepiece, cancelled.
- **Exemption: verbatim material.** Quoted customer reviews, published owner
  replies, and carrier-registered SMS legal text stay exactly as published even
  when they break the rules above. Code comments are out of scope.
