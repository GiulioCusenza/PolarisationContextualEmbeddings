from settings import *

import xml.etree.ElementTree as ET
import os, shutil, re

def tag(tag):
    return "{http://www.tei-c.org/ns/1.0}" + tag

def load_affiliations(file):
    affiliations = dict()
    tree = ET.parse(file)
    root = tree.getroot()
    for person in root.findall(tag("person")):
        name = person.get("{http://www.w3.org/XML/1998/namespace}id")
        for affiliation in person.findall(tag("affiliation")):
            group_tag = "#party." if DATASET == "GB" else "#group."
            if affiliation.get("ref") and affiliation.get("ref").startswith(group_tag):
                group = (affiliation.get("ref")[7:], affiliation.get("from"), affiliation.get("to"))
                if name not in affiliations:
                    affiliations.update({name: [group]})
                else:
                    affiliations[name].append(group)
    return affiliations
                    
def get_affiliation(name, date, affiliations):
    if name in affiliations:
        for affiliation, start, end in affiliations[name]:
            if (start < date and not end) or start < date < end:
                return affiliation

def extract(file, topics, affiliations):
    texts = list()
    tree = ET.parse(file)
    root = tree.getroot()
    date = root.find(f"./{tag('teiHeader')}/{tag('fileDesc')}/{tag('sourceDesc')}/{tag('bibl')}/{tag('date')}").get("when")
    for u in root.findall(f"{tag('text')}/{tag('body')}/{tag('div')}/{tag('u')}"):
        if u.get("ana") == "#regular" and u.get("who"):
            affiliation = get_affiliation(u.get("who")[1:], date, affiliations)
            if affiliation in GROUP2ID:
                for seg in u.findall(tag("seg")):
                    text = seg.text
                    for topic in topics:
                        if topic.lower() in text.lower():
                            text = re.sub(r"^((\w+ ){1,3})\([\w'-]+\)\. ", "", text)
                            texts.append((date, topic, GROUP2ID[affiliation], u.get("who")[1:], text))
    return sorted(texts)


if __name__ == "__main__":
    print("Running on", DATASET)
    affiliations = load_affiliations(PEOPLE_FILE)
    shutil.rmtree(UTTERANCES_DIR)
    for year in YEARS:
        print(year, end="\r")
        dir = UTTERANCES_DIR+year+"/"
        os.makedirs(dir)
        topic2entries = {t: list() for t in TOPICS}
        for file in os.listdir(os.fsencode(PARLAMINT_DIR+year)):
            if DATASET != "GB" or "commons" in os.fsdecode(file):
                for entry in extract(PARLAMINT_DIR+year+"/"+os.fsdecode(file), TOPICS, affiliations):
                    topic2entries[entry[1]].append(entry)
        for topic, entries in topic2entries.items():
            open(dir+topic+".tsv", "w", encoding="utf-8").writelines(["\t".join(e[0:1]+e[2:])+"\n" for e in entries])
    