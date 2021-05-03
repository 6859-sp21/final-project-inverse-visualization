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


if __name__ == "__main__":
    app.run(main)
