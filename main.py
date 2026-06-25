import pandas as pd
import glob
import re
import json
import os

notes_file = open('notes.json')
notes = json.load(notes_file)

# Strip lookahead/lookbehind constructs (incl. their contents) before
# we keep the text of normal capturing groups.
lookaround = re.compile(r"\(?\?[:!=<][^)]*\)?")


def name_from_regex(regex):
    name = regex
    name = name.replace("(?i)", "")          # case-insensitive flag
    name = lookaround.sub(" ", name)          # drop (?!...) / (?=...) etc.
    name = re.sub(r"\.[*+]|[\^$()]", " ", name)  # drop .* .+ ^ $ ( )
    name = re.sub(r"\s+", " ", name).strip()
    return name


def texture_path(model_path):
    """Resolve a model's layer0 texture to an on-disk png path."""
    if not os.path.exists(model_path):
        return None
    with open(model_path) as f:
        model = json.load(f)
    layer0 = model.get("textures", {}).get("layer0")
    if not layer0:
        return None
    layer0 = layer0.split(":", 1)[-1]          # strip "minecraft:"
    path = f"assets/minecraft/textures/{layer0}.png"
    return path if os.path.exists(path) else None


def variant_rules(transform):
    """Yield (regex, substitution) pairs from a transform list, flattening
    `alternative` functions that bundle many regex/substitution rules."""
    for t in transform:
        if not isinstance(t, dict):
            continue
        if "regex" in t:
            yield t["regex"], t.get("substitution", "elytra")
        if t.get("function") == "alternative":
            for alt in t.get("alternatives", []):
                if isinstance(alt, dict) and "regex" in alt:
                    yield alt["regex"], alt.get("substitution", "elytra")


def compute(path):
    with open(path, "r") as file:
        data = json.load(file)

    model_prefix = data.get("modelPrefix")
    if not model_prefix:
        return []

    # modelPrefix looks like "elytras/color_elytra/red_elytra/"
    parts = [p for p in model_prefix.split("/") if p]
    if len(parts) < 2:
        return []
    category = parts[1].replace("_", " ")

    rows = []
    for regex, substitution in variant_rules(data.get("parameters", {}).get("transform", [])):
        name = name_from_regex(regex)
        # substitution resolves the model id, e.g. "black/elytra" -> ".../black/elytra.json"
        model = f"assets/minecraft/models/item/{model_prefix}{substitution}.json"
        image_path = texture_path(model)
        if not image_path:
            continue
        broken_path = texture_path(model[:-len("elytra.json")] + "elytra_broken.json") \
            if model.endswith("elytra.json") else None
        if not broken_path:
            broken_path = image_path

        note = notes[name] if name in notes else ""

        rows.append([
            name,
            f"<img src=\"{image_path}\" style=\"width: 100px; max-width:none; image-rendering: pixelated;\">",
            f"<img src=\"{broken_path}\" style=\"width: 100px; image-rendering: pixelated;\">",
            category,
            note,
        ])
    return rows


paths = sorted(glob.glob('./assets/minecraft/variants-cit/item/elytras/**/*.json', recursive=True))
rows = []
for path in paths:
    rows.extend(compute(path))
df = pd.DataFrame(rows, columns=['name', 'image', 'broken_image', 'category', 'notes'])

df['name'] = df['name'].astype(str).str.lower()
df.drop_duplicates(subset=['name'], keep="last", inplace=True)

df.reset_index(inplace=True, drop=True)
df.index += 1

categories = df["category"].unique()

style = "<head><link rel=\"stylesheet\" href=\"https://cdn.jsdelivr.net/npm/sakura.css/css/sakura.css\"></head>"
navbar = "<a href=\"index.html\">All</a>"
for category in categories:
    short = category.split(" ")
    short = short[0]
    navbar += f"<a href=\"{category}.html\" style=\"margin-left: 1em;\">{short}</a>"
print(df)
html = df.to_html(escape=False, border=0)
html = f"{style}\n<body>{navbar}\n{html}</body>"
output = open(f"index.html", "w")
output.writelines(html)
output.close()

for category, df in df.groupby('category'):
    df.reset_index(inplace=True, drop=True)
    df.index += 1
    html = df.to_html(escape=False, border=0)
    html = f"{style}\n<body>{navbar}\n{html}</body>"
    output = open(f"{category}.html", "w")
    output.writelines(html)
    output.close()
