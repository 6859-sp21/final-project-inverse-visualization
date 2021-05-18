from absl import app
from absl import flags

import numpy as np

from . import data_gen
import tensorflow as tf
import matplotlib.pyplot as plt
import io

from PIL import Image, ImageDraw

FLAGS = flags.FLAGS


def empty_plot():
    plt.clf()
    plt.bar([], [])
    plt.xticks([])
    plt.yticks([])

    io_buf = io.BytesIO()
    plt.savefig(io_buf, format="raw", dpi=100, transparent=True)
    io_buf.seek(0)
    img_arr = np.reshape(
        np.frombuffer(io_buf.getvalue(), dtype=np.uint8),
        newshape=(int(plt.gcf().bbox.bounds[3]), int(plt.gcf().bbox.bounds[2]), -1),
    )
    io_buf.close()
    return Image.fromarray(img_arr)


_CLASS_MAP = {1: "bar", 2: "point"}


def color_dist(c1, c2):
    return np.linalg.norm(c2 - c1)


class EncodingDerenderEngine(object):
    def __init__(self, box_model_path="box_model"):
        self.box_model = tf.saved_model.load(box_model_path)
        self.detect_thresh = 0.2

    def derender(self, img):
        h, w, _ = img.shape

        input_tensor = tf.convert_to_tensor(img)
        input_tensor = input_tensor[tf.newaxis, ...]
        detections = self.box_model(input_tensor)
        boxes = detections["detection_boxes"]
        classes = detections["detection_classes"]
        scores = detections["detection_scores"]

        boxes = boxes[scores > self.detect_thresh]
        classes = classes[scores > self.detect_thresh]

        final_boxes = []
        colors = []

        for i, (class_, box) in enumerate(zip(classes, boxes)):
            class_index = int(class_.numpy())
            class_name = _CLASS_MAP[class_index]

            ymin, xmin, ymax, xmax = box

            ymin *= h
            ymax *= h
            xmax *= w
            xmin *= w

            cx = int((xmax + xmin) / 2)
            cy = int((ymax + ymin) / 2)

            xmax = int(xmax)
            ymax = int(ymax)
            xmin = int(xmin)
            ymin = int(ymin)

            color = tuple(int(x) for x in img[cy, cx])
            color_array = np.array(color)

            if color_dist(np.array([255, 255, 255]), color_array) < 5:
                continue

            skip = False
            for c in colors:
                if color_dist(c, color_array) < 10:
                    skip = True

            if not skip:
                colors.append(color_array)

        for i, (class_, box) in enumerate(zip(classes, boxes)):
            class_index = int(class_.numpy())
            class_name = _CLASS_MAP[class_index]

            ymin, xmin, ymax, xmax = box

            ymin *= h
            ymax *= h
            xmax *= w
            xmin *= w

            cx = int((xmax + xmin) / 2)
            cy = int((ymax + ymin) / 2)

            xmax = int(xmax)
            ymax = int(ymax)
            xmin = int(xmin)
            ymin = int(ymin)

            color = tuple(int(x) for x in img[cy, cx])
            color_array = np.array(color)

            if color_dist(np.array([255, 255, 255]), color_array) < 5:
                continue

            closest = tuple(
                min(
                    [(c, color_dist(c, color_array)) for c in colors],
                    key=lambda x: x[-1],
                )[0]
            )
            closest = tuple(int(x) for x in closest)

            if class_name == "bar":
                final_boxes.append(
                    # TODO(shreyask): ymax baseline.
                    {
                        "id": i,
                        "type": class_name,
                        "box": (xmin, ymin, xmax, 428),
                        "color": closest,
                    }
                )
            else:
                r = int(min(xmax - xmin, ymax - ymin) / 2)

                final_boxes.append(
                    # TODO(shreyask): ymax baseline.
                    {
                        "id": i,
                        "type": class_name,
                        "box": (cx - r, cy - r, cx + r, cy + r),
                        "color": closest,
                    }
                )

        return {
            "layer": "encodings",
            "entities": final_boxes,
            "width": w,
            "height": h,
        }

    def render(self, meta):
        empty = Image.open("empty.png")
        img = empty.copy()
        draw = ImageDraw.Draw(img)

        for entity in meta["entities"]:
            if entity["type"] == "bar":
                draw.rectangle(entity["box"], fill=tuple(entity["color"]))

            if entity["type"] == "point":
                draw.ellipse(entity["box"], fill=tuple(entity["color"]))

        img.paste(empty, (0, 0), empty)

        return img


def main(_):
    empty = empty_plot()
    empty.save("empty.png")

    d = EncodingDerenderEngine()

    data_gen.set_seed(1339)
    img, b = data_gen.generate_plot()
    meta = d.derender(img[:, :, ::-1])

    final = d.render(meta)
    final.save("final.png")


if __name__ == "__main__":
    app.run(main)
