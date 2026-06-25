# Elytras+

A Minecraft resource pack that adds **380+ custom elytras** to the game. Each
elytra is applied by renaming a vanilla elytra (via an anvil) to a specific
name — the pack swaps in the matching texture and model using the resource
pack CIT (Custom Item Textures) system.

This pack was inspired by *Itembound*, and was built with reference to its
files to learn how the system works.

> Part of the **Elytras+ / Textures+** project.
> Discord: https://discord.gg/WCvwtzW

## Contents

Currently **387 elytras** across these categories:

| Category        | Count |
| --------------- | ----- |
| Block elytras   | 81    |
| Bug elytra      | 61    |
| Misc elytras    | 54    |
| Modeled elytras | 51    |
| Color elytra    | 36    |
| Mojang elytras  | 29    |
| Pride elytras   | 25    |
| Shulker elytras | 15    |
| Glider elytras  | 13    |
| Zelda elytras   | 6     |
| Parrot wings    | 5     |

17 of the elytras are official Mojang/Minecraft cape designs (the icons for
those were made by this project).

## How it works

Elytra variants live under `assets/minecraft/variants-cit/item/elytras/`. Each
variant is a JSON file that maps a custom item name (matched by a regex) to a
model under `assets/minecraft/models/item/elytras/...`, which in turn points at
a texture under `assets/minecraft/textures/item/elytras/...`.

### Building the gallery

`main.py` scans every variant, resolves its name, category, item texture, and
broken-elytra texture, and generates a browsable HTML gallery:

- `index.html` — every elytra
- one page per category (e.g. `block elytras.html`)

To regenerate locally:

```sh
pip install pandas        # or: conda install pandas
python3 main.py
```

Notes shown next to an elytra come from `notes.json` (keyed by the lowercased
elytra name).

See [NOTES.md](NOTES.md) for developer/maintenance details.

## Automation

- **`.github/workflows/build_and_run.yml`** — on every push to `main`, runs
  `main.py` and deploys the generated gallery to GitHub Pages. The HTML is built
  in CI and published directly, so it is **not** committed to the repo.
- **`.github/workflows/sync.yml`** — every 3 hours, fast-forwards `main` from
  the upstream repo (`dbrighthd/elytras`).

## Credits

Textures by:

- The **Textures+** team — dbrighthd, SwiftShadowFox, Fishysalmon
- **xshot_99**
- Pride elytras by **SixFootBlue** — https://www.curseforge.com/members/sixfootblue/followers
- Cape elytras: **Minecraft / Mojang**
