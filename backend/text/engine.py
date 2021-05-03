from absl import app
from absl import flags

from .ocr_lib import OCRLib

from PIL import Image, ImageDraw, ImageFont

FLAGS = flags.FLAGS


class TextDerenderEngine(object):
    def __init__(self, keypath="GoogleVisionToken.json", fontfile="Arial.ttf"):
        self.ocrlib = OCRLib(keypath=keypath)
        self.fontfile = fontfile

    def derender(self, img):
        h, w, _ = img.shape

        (_, texts, txt_to_bb) = self.ocrlib.detect_text_image(img)

        final_boxes = []

        for text in texts:
            (x0, y0), _, (x1, y1), _ = txt_to_bb[text]

            xmin = x0
            ymin = y0
            xmax = x1
            ymax = y1

            final_boxes.append(
                {
                    "type": "text",
                    "text": text,
                    "box": (xmin, ymin, xmax, ymax),
                    "color": (0, 0, 0),
                }
            )

        return {
            "layer": "text",
            "entities": final_boxes,
            "width": w,
            "height": h,
        }

    def find_font(self, text, box):
        x0, y0, x1, y1 = box

        fontsize = 1  # starting font size

        font = ImageFont.truetype(self.fontfile, fontsize)
        while font.getsize(text)[0] < x1 - x0:
            # iterate until the text size is just larger than the criteria
            fontsize += 1
            font = ImageFont.truetype(self.fontfile, fontsize)

        return font

    def render(self, meta):
        img = Image.new("RGBA", (meta["width"], meta["height"]))

        draw = ImageDraw.Draw(img)
        for entity in meta["entities"]:
            if entity["type"] != "text":
                continue

            x0, y0, x1, y1 = entity["box"]
            fnt = self.find_font(entity["text"], entity["box"])
            draw.text((x0, y0), entity["text"], font=fnt, fill=tuple(entity["color"]))

        return img


def main(argv):
    pass


if __name__ == "__main__":
    app.run(main)
