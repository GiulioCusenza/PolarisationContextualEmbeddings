# Replace #regular with #guest where wrong.
# Only for Italian dataset.

import re, os
from settings import *

if DATASET == "IT":
    print("Correcting tags for guest speakers...")
    for year in YEARS:
        dir = PARLAMINT_DIR + "/" + year + "/"
        for file in os.listdir(os.fsencode(dir)):
            f = open(dir+os.fsdecode(file), "r", encoding="utf-8").read()
            for guest in re.findall(r"(?<=ana=\"#guest\" who=\"#)[^\"]+", f):
                f = re.sub(f"ana=\"#regular\" who=\"#{guest}\"",
                        f"ana=\"#guest\" who=\"#{guest}\"", f)
            open(dir+os.fsdecode(file), "w", encoding="utf-8").write(f)
    print("Tags for guest speakers corrected.")
else:
    print("This script is intended for the Italian data only.")