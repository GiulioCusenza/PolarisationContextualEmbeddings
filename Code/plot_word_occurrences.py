from settings import *

import matplotlib.pyplot as plt
import math
from string import punctuation
import regex as re

def count_occurrences(topic):
    n_occurrences = 0
    sessions = set()
    yearly_occurrences = list()
    for year in YEARS:
        count = 0
        for entry in open(f"{UTTERANCES_DIR}/{year}/{topic}.tsv", encoding="utf-8"):
            session, _, _, text = entry.split("\t")
            sessions.add(session)
            for word in re.sub(f"[{punctuation}]", " ", text).split():
                if topic == word:
                    count += 1
        n_occurrences += count
        yearly_occurrences.append(count)
    return n_occurrences, len(sessions), yearly_occurrences

def plot_occurrences():
    print("topic,\toccurrences,\tsessions,\toccurrences/session")
    n_cols = 3
    fig, axs = plt.subplots(
        nrows=math.ceil((len(TOPICS) // n_cols)),
        ncols=n_cols,
        sharex=True,
        sharey=True
        )
    for i, topic in enumerate(TOPICS):
        ax = axs[i // n_cols][i % n_cols]
        ax.set_title(topic)
        n_occurrences, n_sessions, yearly_occurrences = count_occurrences(topic)
        print(topic, n_occurrences, n_sessions, n_occurrences / n_sessions, sep="\t")
        ax.plot(YEARS, yearly_occurrences, marker='o', linestyle=':', color='#aa0000')
    fig.tight_layout()
    plt.show()


if __name__ == "__main__":
    plot_occurrences()