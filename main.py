import pandas as pd
import glob
import re
import json
import os

notes_file = open('notes.json')
notes = json.load(notes_file)

nameex = re.compile(r"nbt\.display\.Name=(?:ipattern:)?(.*)")
typeex = re.compile(r"type=(.*)")
textureex = re.compile(r"texture.*=(.*)")

def compute(path):
    with open(path, "r") as file:
        folders = path.split("/")
        content = file.read()
        type = typeex.findall(content)
        name = nameex.findall(content)
        texture = textureex.findall(content)
        name = name[0]
        type=type[0]
        texture=texture[0]
        
        if type != "item":
            return
        if texture == "broken_elytra":
            return

        image_path = folders[1:-1]
        image_path = "/".join(image_path)
        
        image_name = folders[-1]
        image_name = image_name.split(".")
        image_name = image_name[0]
        
        category = folders[6]
        category = category.replace("_"," ")
        
        note = notes[name] if (name in notes)  else ""
        elytra_image_path = f"{image_path}/{image_name}.png"
        if not os.path.exists(elytra_image_path):
            return
        
        data = [[name,f"<img src=\"{elytra_image_path}\" style=\"width: 100px; max-width:none; image-rendering: pixelated;\">",f"<img src=\"{image_path}/broken_elytra.png\" style=\"width: 100px; image-rendering: pixelated;\">",category,note]]
        df = pd.DataFrame(data, columns=['name','image','broken_image','category','notes'])
        return df


paths = sorted(glob.glob('./**/cit/elytras/**/*.properties', recursive=True))
df = pd.DataFrame()   
for path in paths:                                                 
    df = pd.concat([df, compute(path)], ignore_index=True, sort=False)
    
df['name'] = df['name'].astype(str).str.lower()
df.drop_duplicates(subset=['name'],keep="last", inplace=True)

df.reset_index(inplace=True,drop=True)
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
    df.reset_index(inplace=True,drop=True)
    df.index += 1
    html = df.to_html(escape=False, border=0)
    html = f"{style}\n<body>{navbar}\n{html}</body>"
    output = open(f"{category}.html", "w")
    output.writelines(html)
    output.close()
        