# Script qui convertit les fichiers RLE de structure (trouvable sur internet) en json dans le catalogue

from json import dump, load
from os import path

if not path.exists("catalog.json"):
    with open("catalog.json", "x") as f:
        dump([], f)
    
converted = []
y = 0
x = 0

with open(input("Fichier RLE à convertir : "), "r") as f:
    for line in f:
        line = line.strip()
        if line[0] == "#" or line[0] == "x":
            continue
        i = 0
        j = 0
        while i < len(line):
            length = 1
            while line[j].isnumeric():
                j += 1
            if j > i:
                length = int(line[i:j])
                i = j
            match line[j]:
                case "o":
                    for _ in range(length):
                        converted.append([x, y])
                        x += 1
                case "b":
                    x += length
                case "$":
                    y += length
                    x = 0
                case "!":
                    print("Conversion terminée")
                    with open("catalog.json", "r") as f:
                        catalog = load(f)
                    catalog.append(converted)
                    with open("catalog.json", "w") as f:
                        dump(catalog, f, indent=4)
                    exit()
            i += 1
            j += 1
        