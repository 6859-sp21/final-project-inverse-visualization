from absl import app
from absl import flags

import matplotlib.font_manager
import matplotlib.pyplot as plt
import numpy as np
import random
import string
import io
import os
import tqdm
import cv2
import ujson as json
from multiprocessing import Pool

from PIL import Image

flags.DEFINE_boolean("preview", True, "Preview generation.")
flags.DEFINE_boolean("generate", False, "Generate data.")
flags.DEFINE_string("data", "data", "Data output directory.")
flags.DEFINE_integer("num", 100000, "How many examples to generate.")
flags.DEFINE_integer("seed", 1337, "RNG Seed.")
FLAGS = flags.FLAGS

FONTS = [f.name for f in matplotlib.font_manager.fontManager.ttflist]


def set_seed(seed):
    """Set seed for both Python's Random and Numpy's random.
    """

    random.seed(seed)
    np.random.seed(seed)


def random_text(l=7):
    letters = string.ascii_letters + string.digits
    length = random.randint(3, l)
    return "".join(random.choice(letters) for i in range(length))


def random_sentence(w=10):
    num_words = random.randint(3, w)
    return " ".join(random_text() for _ in range(num_words))


def random_color(solids=None, solid_prob=0.3):
    if solids is not None and random.random() < solid_prob:
        return random.choice(solids)

    return tuple(np.random.random(size=3))


def random_number_text():
    num = random.randint(0, 300)
    return str(num)


import matplotlib.pyplot as plt
from matplotlib.path import get_path_collection_extents


# From: https://stackoverflow.com/a/55007838
def getbb(sc, ax):
    """ Function to return a list of bounding boxes in data coordinates
        for a scatter plot """
    transform = sc.get_transform()
    transOffset = sc.get_offset_transform()
    offsets = sc._offsets
    paths = sc.get_paths()
    transforms = sc.get_transforms()

    if not transform.is_affine:
        paths = [transform.transform_path_non_affine(p) for p in paths]
        transform = transform.get_affine()
    if not transOffset.is_affine:
        offsets = transOffset.transform_non_affine(offsets)
        transOffset = transOffset.get_affine()

    if isinstance(offsets, np.ma.MaskedArray):
        offsets = offsets.filled(np.nan)

    bboxes = []

    if len(paths) and len(offsets):
        if len(paths) < len(offsets):
            # for usual scatters you have one path, but several offsets
            paths = [paths[0]] * len(offsets)
        if len(transforms) < len(offsets):
            # often you may have a single scatter size, but several offsets
            transforms = [transforms[0]] * len(offsets)

        for p, o, t in zip(paths, offsets, transforms):
            result = get_path_collection_extents(
                transform.frozen(), [p], [t], [o], transOffset.frozen()
            )
            bboxes.append(result)

    return bboxes


def generate_plot(seed=None, preview=False):
    plt.clf()
    if seed is not None:
        set_seed(seed)

    kinds = ["bar", "scatter"]
    kind = random.choice(kinds)

    background_color = random_color(solids=["white"])

    if kind == "scatter":
        num_cat = random.randint(1, 4)

        scatters = []

        for cat_index in range(num_cat):
            num_points = random.randint(3, 14)
            color = random_color()
            X = np.random.uniform(low=10, high=300, size=num_points)
            Y = np.random.uniform(low=10, high=300, size=num_points)

            scatter = plt.scatter(X, Y, color=color)
            scatters.append(scatter)

        plt.yticks(fontname=random.choice(FONTS), color=random_color(solids=["black"]))
        plt.xticks(fontname=random.choice(FONTS), color=random_color(solids=["black"]))

        plt.title(
            random_sentence(),
            fontname=random.choice(FONTS),
            color=random_color(solids=["black"]),
            pad=random.randint(0, 50),
        )

        plt.gcf().canvas.draw()

        io_buf = io.BytesIO()
        plt.savefig(io_buf, format="raw", dpi=100)
        io_buf.seek(0)
        img_arr = np.reshape(
            np.frombuffer(io_buf.getvalue(), dtype=np.uint8),
            newshape=(int(plt.gcf().bbox.bounds[3]), int(plt.gcf().bbox.bounds[2]), -1),
        )
        io_buf.close()
        img_arr = img_arr[:, :, :3]

        h, w, _ = img_arr.shape

        box_coords = []

        for scatter in scatters:
            bboxes = getbb(scatter, plt.gca())
            for bbox in bboxes:
                box_coords.append(
                    {
                        "x1": int(bbox.xmin),
                        "y1": h - int(bbox.ymin),
                        "x2": int(bbox.xmax),
                        "y2": h - int(bbox.ymax),
                        "encoding": "point",
                    }
                )

        if preview:
            plt.show()
            return img_arr, box_coords
        else:
            return img_arr, box_coords

    if kind == "bar":
        num_cat = random.randint(3, 10)
        cat_names = [random_text() for _ in range(num_cat)]
        cat_values = [random.randrange(10, 300) for _ in range(num_cat)]
        x_pos = np.arange(num_cat)

        width = random.random()
        if random.random() < 0.5:
            width = np.random.random(size=num_cat) * 0.8 + 0.2

        bars = plt.bar(
            x_pos,
            cat_values,
            width=width,
            color=[random_color() for _ in range(num_cat)],
        )
        plt.xticks(
            x_pos,
            cat_names,
            fontname=random.choice(FONTS),
            color=random_color(solids=["black"]),
        )
        plt.yticks(fontname=random.choice(FONTS), color=random_color(solids=["black"]))
        plt.title(
            random_sentence(),
            fontname=random.choice(FONTS),
            color=random_color(solids=["black"]),
            pad=random.randint(0, 50),
        )

        plt.gcf().canvas.draw()

        box_coords = []

        io_buf = io.BytesIO()
        plt.savefig(io_buf, format="raw", dpi=100)
        io_buf.seek(0)
        img_arr = np.reshape(
            np.frombuffer(io_buf.getvalue(), dtype=np.uint8),
            newshape=(int(plt.gcf().bbox.bounds[3]), int(plt.gcf().bbox.bounds[2]), -1),
        )
        io_buf.close()
        img_arr = img_arr[:, :, :3]

        h, w, _ = img_arr.shape

        for bar in bars.patches:
            bbox = bar.get_bbox().transformed(plt.gca().transData)
            box_coords.append(
                {
                    "x1": int(bbox.xmin),
                    "y1": h - int(bbox.ymin),
                    "x2": int(bbox.xmax),
                    "y2": h - int(bbox.ymax),
                    "encoding": "bar",
                }
            )

        if preview:
            plt.show()
            return img_arr, box_coords
        else:
            return img_arr, box_coords


def g(i):
    FLAGS.read_flags_from_files("--flagfile=temp.flags")
    FLAGS.mark_as_parsed()

    img, boxes = generate_plot()

    save_path = os.path.join(FLAGS.data, str(i) + ".png")
    if not os.path.exists(save_path):
        Image.fromarray(img).save(save_path)

    return boxes


def main(argv):
    if os.path.exists("temp.flags"):
        os.remove("temp.flags")

    FLAGS.append_flags_into_file("temp.flags")
    if FLAGS.preview and not FLAGS.generate:
        img, box_coords = generate_plot(preview=True)

        img = np.copy(img[:, :, ::-1])

        for box in box_coords:
            sp, ep = (box["x1"], box["y1"]), (box["x2"], box["y2"])
            img = cv2.rectangle(img, sp, ep, (0, 0, 0), 3)

        cv2.imshow("a", img)
        cv2.waitKey(0)

    if FLAGS.generate:
        meta = {}

        ids = list(range(FLAGS.num))

        with Pool(10) as p:
            try:
                res = list(tqdm.tqdm(p.imap(g, ids), total=len(ids)))
            except KeyboardInterrupt:
                p.terminate()
                p.join()
                exit()

        for i, r in zip(ids, res):
            meta[i] = r

        with open(os.path.join(FLAGS.data, "meta.json"), "w") as f:
            json.dump(meta, f)


if __name__ == "__main__":
    app.run(main)
