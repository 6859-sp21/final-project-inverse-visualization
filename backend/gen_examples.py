from absl import app
from absl import flags

import matplotlib.pyplot as plt
import numpy as np

FLAGS = flags.FLAGS

DATA = [
    ("0-9", 51.1),
    ("10-19", 117.3),
    ("20-29", 401.6),
    ("30-39", 491.6),
    ("40-49", 541.6),
    ("50-59", 550.5),
    ("60-69", 478.4),
    ("70-79", 464.2),
    ("80+", 902),
]


def main(argv):
    values = [x[-1] for x in DATA]
    labels = [x[0] for x in DATA]
    x_pos = np.arange(len(values))

    plt.bar(x_pos, values, color="lightgrey")
    plt.xticks(x_pos, labels, fontname="Arial")
    plt.yticks(fontname="Arial")
    plt.title("COVID-19 Incedence Rate By Age", fontname="Arial")
    plt.savefig("examples/covid.png")

    plt.clf()
    np.random.seed(1337)

    Ms = [1.2, 3.2]
    Cs = [10, 1]
    colors = ["red", "#fc6203"]

    for m, c, color in zip(Ms, Cs, colors):
        X = np.linspace(3, 20, 20)
        Y = m * X + c
        Y += np.random.normal(0, scale=6, size=len(Y))

        plt.scatter(X, Y, color=color)

    plt.xticks(fontname="Arial")
    plt.yticks(fontname="Arial")
    plt.xlabel("THR2 Gene Response", fontname="Arial")
    plt.title("Protein Site First and Second", fontname="Arial")
    plt.savefig("examples/gene.png")


if __name__ == "__main__":
    app.run(main)
