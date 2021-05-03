from absl import app
from absl import flags

import tensorflow as tf
import glob
import os
import cv2
import tqdm
import ujson as json

from object_detection.utils import dataset_util


flags.DEFINE_string("data", "data", "Data directory.")
flags.DEFINE_float("train_split", 0.9, "Training split.")
flags.DEFINE_string("output", "data", "Output directory.")
FLAGS = flags.FLAGS


def create_tf_example(example):
    fn, id_, w, h, img_data, xmins, xmaxs, ymins, ymaxs, ct, c = example

    height = h  # Image height
    width = w  # Image width
    filename = os.path.abspath(fn).encode(
        "ascii"
    )  # Filename of the image. Empty if image is not from file
    encoded_image_data = img_data  # Encoded image bytes
    image_format = b"png"  # b'jpeg' or b'png'

    classes_text = ct  # List of string class name of bounding box (1 per box)
    classes = c  # List of integer class id of bounding box (1 per box)

    tf_example = tf.train.Example(
        features=tf.train.Features(
            feature={
                "image/height": dataset_util.int64_feature(height),
                "image/width": dataset_util.int64_feature(width),
                "image/filename": dataset_util.bytes_feature(filename),
                "image/source_id": dataset_util.bytes_feature(filename),
                "image/encoded": dataset_util.bytes_feature(encoded_image_data),
                "image/format": dataset_util.bytes_feature(image_format),
                "image/object/bbox/xmin": dataset_util.float_list_feature(xmins),
                "image/object/bbox/xmax": dataset_util.float_list_feature(xmaxs),
                "image/object/bbox/ymin": dataset_util.float_list_feature(ymins),
                "image/object/bbox/ymax": dataset_util.float_list_feature(ymaxs),
                "image/object/class/text": dataset_util.bytes_list_feature(
                    classes_text
                ),
                "image/object/class/label": dataset_util.int64_list_feature(classes),
            }
        )
    )
    return tf_example


def filename_example(filename, meta):
    id_ = int(os.path.splitext(os.path.basename(filename))[0])
    img = cv2.imread(filename)
    h, w, _ = img.shape

    with open(filename, "rb") as f:
        data = f.read()

    boxes = meta[str(id_)]

    xmins = []
    xmaxs = []
    ymins = []
    ymaxs = []

    for box in boxes:
        x1 = box["x1"] / w
        x2 = box["x2"] / w
        y1 = box["y2"] / h
        y2 = box["y1"] / h

        if x2 <= x1 or y2 <= y1:
            continue

        xmins.append(x1)
        xmaxs.append(x2)
        ymins.append(y1)
        ymaxs.append(y2)

    class_texts = ["box".encode("ascii")] * len(xmins)
    class_ids = [1] * len(xmins)

    return (
        filename,
        id_,
        w,
        h,
        data,
        xmins,
        xmaxs,
        ymins,
        ymaxs,
        class_texts,
        class_ids,
    )


def gen_records(examples, output):
    writer = tf.io.TFRecordWriter(output)

    for example in tqdm.tqdm(examples):
        tf_example = create_tf_example(example)
        writer.write(tf_example.SerializeToString())

    writer.close()


def main(_):
    meta_filename = os.path.join(FLAGS.data, "meta.json")

    with open(meta_filename, "r") as f:
        meta = json.load(f)

    filenames = glob.glob(os.path.join(FLAGS.data, "*.png"))

    examples = []

    for filename in tqdm.tqdm(filenames):
        examples.append(filename_example(filename, meta))

    examples = sorted(examples, key=lambda x: x[1])

    train_count = int(FLAGS.train_split * len(examples))

    train_examples = examples[:train_count]
    test_examples = examples[train_count:]

    gen_records(train_examples, os.path.join(FLAGS.output, "train.tfrecords"))
    gen_records(test_examples, os.path.join(FLAGS.output, "test.tfrecords"))

    LMAP = """
item {
  id: 1
  name: 'box'
}
"""

    with open(os.path.join(FLAGS.output, "labelmap.txt"), "w") as f:
        f.write(LMAP)


if __name__ == "__main__":
    app.run(main)
