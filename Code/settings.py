# Select "GB" for House of Commons or "IT" for Italian Senate:
DATASET = "IT"

if DATASET == "GB":
    MODEL = "bert-base-uncased"
    PARLAMINT_DIR = "./data/ParlaMint/ParlaMint-GB.TEI/"
    PEOPLE_FILE = PARLAMINT_DIR + "ParlaMint-GB-listPerson.xml"
    UTTERANCES_DIR = "./data/utterances/"
    EMBEDDINGS_DIR = "./data/embeddings/"
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
    PARLAMINT_DIR = "./data/ParlaMint/ParlaMint-IT.TEI/"
    PEOPLE_FILE = PARLAMINT_DIR + "ParlaMint-IT-listPerson.xml"
    UTTERANCES_DIR = "./data/utterances/"
    EMBEDDINGS_DIR = "./data/embeddings/"
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