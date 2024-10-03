from settings import *

import numpy as np
from numpy.linalg import norm
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os, math

def cos(x, y):
    return np.dot(x, y) / (norm(x)*norm(y))

def semantic_polarity(group1, group2=None):
    # SP between the groups
    if group2:
        return 1 - (sum([cos(w1, w2) for w1 in group1 for w2 in group2]) / (len(group1) * len(group2)))
    # SP within the group
    else:
        total_cosines = 0
        count = 0
        for i in range(len(group1)):
            for j in range(len(group1)):
                if i != j:
                    total_cosines += cos(group1[i], group1[j])
                    count += 1
        return 1 - (total_cosines / count) if count else 0

def polarity_matrix(groups):
    n = len(groups)
    matrix = np.zeros((n, n))
    # SP within each group
    for d in range(n):
        matrix[d,d] = semantic_polarity(groups[d])
    # SP between different groups
    for i in range(n):
        for j in range(i):
            matrix[i,j] = semantic_polarity(groups[i], groups[j])
    return matrix

def load_word_data(dir):
    embeddings = list()
    for e in open(dir+"/embeddings.txt", encoding="utf-8"):
        embeddings.append([float(x) for x in e.strip().split("\t")])
    groups = [g.strip() for g in open(dir+"/groups.txt", encoding="utf-8")]
    group2embeddings = {g: list() for g in set(groups)}
    for e, g in zip(embeddings, groups):
        group2embeddings[g].append(e)
    return group2embeddings, len(embeddings)

def save_polarity_matrices():
    for year in YEARS:
        out_dir = POLMAT_DIR+"/"+year+"/"
        os.makedirs(out_dir, exist_ok=True)
        for topic in TOPICS:
            in_dir = EMBEDDINGS_DIR+year+"/"+topic
            group2embeddings, n_embeddings = load_word_data(in_dir)
            print(f"{in_dir}\t{n_embeddings}")
            polarity_mat = polarity_matrix(list(group2embeddings.values()))
            labels = list(group2embeddings.keys())
            polarity_df = pd.DataFrame(polarity_mat, columns=labels, index=labels)
            file = out_dir+topic+".csv"
            polarity_df.to_csv(file)

def plot_polarity_matrices(n_cols=4):
    for topic in TOPICS:
        fig, axs = plt.subplots(nrows=math.ceil(len(YEARS) / n_cols), ncols=n_cols)
        for i, year in enumerate(YEARS):
            ax = axs[i // n_cols][i % n_cols]
            polarity_matrix = pd.read_csv(f"{POLMAT_DIR}/{year}/{topic}.csv", index_col=0)
            print(topic, year)
            print(polarity_matrix)
            mask = np.triu(np.ones_like(polarity_matrix, dtype=bool), k=1)
            sns.heatmap(
                polarity_matrix,
                mask=mask,
                ax=ax,
                annot=True,
                robust=True,
                cmap=sns.cm.rocket_r,
                vmax=.5,
                vmin=.13,
                cbar=False)
            ax.set_title(year)
        for j in range(i+1, len(axs.flat)):
            axs[j // n_cols][j % n_cols].axis('off')
        fig.suptitle(topic)
        fig.set_layout_engine("tight")
        plt.show()


if __name__ == "__main__":
    # save_polarity_matrices()
    plot_polarity_matrices()