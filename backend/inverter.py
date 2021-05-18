from absl import app
from absl import flags

from marks.engine import EncodingDerenderEngine
from text.engine import TextDerenderEngine
import cv2

from PIL import Image, ImageDraw

flags.DEFINE_string("image", "examples/covid.png", "Input image path")
FLAGS = flags.FLAGS


class Inverter(object):
    def __init__(self):
        self.text_engine = TextDerenderEngine(
            keypath="text/GoogleVisionToken.json", fontfile="text/Arial.ttf"
        )
        self.mark_engine = EncodingDerenderEngine(box_model_path="marks/box_model2")

    def derender(self, img):
        h, w, _ = img.shape

        text_meta = self.text_engine.derender(img)
        mark_meta = self.mark_engine.derender(img)

        return {
            "width": w,
            "height": h,
            "layers": {"text": text_meta, "mark": mark_meta},
        }

    def render(self, meta):
        img = Image.new("RGBA", (meta["width"], meta["height"]))

        text_layer = self.text_engine.render(meta["layers"]["text"])
        mark_layer = self.mark_engine.render(meta["layers"]["mark"])

        draw = ImageDraw.Draw(img)
        draw.rectangle((0, 0, meta["width"], meta["height"]), fill=(255, 255, 255))

        img.paste(mark_layer, (0, 0), mark_layer)
        img.paste(text_layer, (0, 0), text_layer)

        return img


def main(argv):
    img = cv2.imread(FLAGS.image)[:, :, ::-1]

    i = Inverter()
    meta = i.derender(img)
    img = i.render(meta)
    img.save("test.png")


if __name__ == "__main__":
    app.run(main)
