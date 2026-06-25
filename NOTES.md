# Developer / maintenance notes

## CIT format migration (important)

This pack originally used **OptiFine CIT** — `.properties` files under
`assets/minecraft/optifine/cit/elytras/`. It has since migrated to the newer
**`variants-cit`** JSON format under
`assets/minecraft/variants-cit/item/elytras/`.

`main.py` was rewritten to read the new format. The old version globbed for
`**/cit/elytras/**/*.properties`, which now matches nothing — that's the cause
of the historical `KeyError: 'name'` (the DataFrame ended up empty).

## How `main.py` resolves each elytra

For every variant JSON it reads:

- **`modelPrefix`** — e.g. `elytras/color_elytra/red_elytra/`.
  - **Category** = the first folder after `elytras/` (`color_elytra` → "color elytra").
- **`parameters.transform`** — the rename rules. Two shapes exist:
  1. **Simple** — a single object with a `regex` and a `substitution`
     (substitution is usually just `elytra`).
  2. **`function: "alternative"`** — a list of `alternatives`, each its own
     `regex` + `substitution`. Used by the **shulker** and **wool** sets, where
     one file maps every color (e.g. `(?i).*(black).*shulker.*` → `black/elytra`).
     Each alternative becomes its own gallery row — early versions dropped these.
- **Name** — derived from the regex by stripping `(?i)`, `.*`/`.+`/`^`/`$`,
  lookaheads like `(?!...)`, and parentheses. So `(?i)?!(pan).*cake elytra.*`
  correctly yields `cake elytra` (not `pancake`).
- **Image** — resolved by reading the model file
  (`models/item/<modelPrefix><substitution>.json`) and following its
  `layer0` texture. **Don't guess the PNG filename** — texture files are
  inconsistently named (`o_wings_icon.png`, `elytra_item.png`, and even typos
  like `elyta.png` / `eltra_item.png`). Going through the model avoids all that.
- **Broken image** — the sibling `elytra_broken.json` model's `layer0`, falling
  back to the normal image if absent.

A variant is skipped if its model/texture can't be resolved on disk.

## Notes

`notes.json` maps a **lowercased** elytra name to a note string shown in the
gallery. Names not present get a blank note.

## Output

`main.py` writes `index.html` plus one page per category. These are generated
artifacts and are **gitignored** — they are not committed. On every push to
`main`, `build_and_run.yml` rebuilds them and deploys to GitHub Pages
(`upload-pages-artifact` + `deploy-pages`), copying the HTML and
`assets/minecraft/textures` into the published `_site`.

The repo's Pages source must be set to **GitHub Actions** (Settings → Pages →
Build and deployment → Source), not "Deploy from a branch".

## Gotchas

- HTML filenames contain spaces (e.g. `block elytras.html`) — quote them in the
  shell.
- `main.py` requires `pandas`.
