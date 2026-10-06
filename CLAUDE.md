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

## Finish the job: ship and land without being asked

This holds on every machine (company Mac, Windows Cloud PC, contractor laptop, Claude Code on
the web) and overrides any default to commit or push only when asked. When a piece of work is
complete and verified, **take it all the way to GitHub without asking**: commit, push, open the
PR, merge it once the required checks pass, then confirm it merged and the deploy run started.
Do not stop at "ready to commit" or "ready to merge", and do not ask "want me to push?" The
answer is yes. Work that exists only on one computer is work the team cannot see.

- **Never leave work unpushed.** If the session stops before the work is done, push the branch
  anyway and open a draft PR (`flow ship`, or `git push -u origin <branch>` then
  `gh pr create --draft --fill`), so it is on GitHub by the end of the session.
- **No `flow` on this machine?** (Claude Code on the web, or a computer that hasn't run the
  setup in `git-workflow/ONBOARD.md` or `ONBOARD-WINDOWS.md`.) Run the raw commands in
  parentheses above. Same outcome, no need to ask.
- **Waiting on an approval is not a reason to hold back.** A PR that needs a staff approval
  (`exec-guard`, `roster-approval`) still gets pushed and opened; say it is waiting.
- **Still stop and ask:** a merge conflict; `git push --force`; `git reset --hard`,
  `git clean -fd`, or deleting a branch someone else pushed; a required check that is failing
  (fix the cause, never bypass the check); anything beyond the repo, such as DNS or emailing a
  client.

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
- **US phrasing, not just US spelling.** Two correctly spelled words can still
  read as British. Write "right away", "different from", "parking lot", "zip
  code", "on the weekend", "drain field". The us-spellings check carries the
  full list and fails a PR that reintroduces one.
- **Exemption: verbatim material.** Quoted customer reviews, published owner
  replies, and carrier-registered SMS legal text stay exactly as published even
  when they break the rules above. Code comments are out of scope.
