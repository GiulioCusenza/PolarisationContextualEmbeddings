# Select "GB" for House of Commons or "IT" for Italian Senate:
DATASET = "GB"

PARLAMINT_DIR = f"./data/{DATASET}/ParlaMint/"
PEOPLE_FILE = PARLAMINT_DIR + f"ParlaMint-{DATASET}-listPerson.xml"
UTTERANCES_DIR = f"./data/{DATASET}/utterances/"
EMBEDDINGS_DIR = f"./data/{DATASET}/embeddings/"

if DATASET == "GB":
    MODEL = "bert-base-uncased"

    YEARS = [str(y) for y in range(2015, 2023)]
    TOPICS = [
        "education",
        "energy",
        "Europe",
        "immigration",
        "Russia",
        "unemployment",
    ]
    GROUP2ID = {
        "LAB": "LAB",
        "CON": "CON"
        }

elif DATASET == "IT":
    MODEL = "dbmdz/bert-base-italian-uncased"
    YEARS = [str(y) for y in range(2013, 2023)]
    TOPICS = [
        "scuola",
        "energia",
        "Europa",
        "immigrazione",
        "Russia",
        "disoccupazione"
    ]
    GROUP2ID = {
        "FdI": "FdI",
        "LN-Aut": "LN",
        "L-SP": "LN",
        "L-SP-PSd'Az": "LN",
        "FI-PdL.XVII": "FI",
        "FI-BP": "FI",
        "FIBP-UDC": "FI",
        "M5S.1": "M5S",
        "M5S.2": "M5S",
        "PD": "PD"
        }