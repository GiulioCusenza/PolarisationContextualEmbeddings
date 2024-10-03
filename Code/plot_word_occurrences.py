from settings import *

import matplotlib.pyplot as plt
import math

def count_occurrences(topic):
    occurrences = list() # n occurrences each year
    for year in YEARS:
        count = 0
        for entry in open(f"{UTTERANCES_DIR}/{year}/{topic}.tsv", encoding="utf-8"):
            text = entry.split("\t")[3]
            for word in text.split():
                if topic in word:
                    count += 1
        occurrences.append(count)
    return occurrences

def plot_occurrences():
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
        ax.plot(YEARS, count_occurrences(topic), marker='o', linestyle=':', color='#aa0000')
    fig.tight_layout()
    plt.show()


if __name__ == "__main__":
    plot_occurrences()