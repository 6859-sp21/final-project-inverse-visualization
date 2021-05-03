import numpy as np
import cv2
import os
from google.cloud import vision
import pickle
import hashlib

_CACHE_NAME = "ocr_cache.p"


def hash_contents(s):
    h = hashlib.sha1()
    h.update(s)
    return h.hexdigest()


def check_cached(h):
    if not os.path.exists(_CACHE_NAME):
        return

    with open(_CACHE_NAME, "rb") as f:
        cache = pickle.load(f)
    return cache.get(h, None)


def write_cache(h, r):
    cache = {}

    if os.path.exists(_CACHE_NAME):
        with open(_CACHE_NAME, "rb") as f:
            cache = pickle.load(f)

    cache[h] = r

    with open(_CACHE_NAME, "wb") as f:
        pickle.dump(cache, f)


class OCRLib(object):
    def __init__(self, keypath="GoogleVisionToken.json"):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = keypath

    # Detect the text in a remote image
    # Return a tuple (bounding_boxes, text_in_bounding_box)
    # where text_in_bounding_box[i] is the text inside bounding_boxes[i]
    # Citation: https://cloud.google.com/vision/docs/ocr#detect_text_in_a_remote_image
    def detect_text_uri(self, uri):
        from google.cloud import vision

        client = vision.ImageAnnotatorClient()
        image = vision.Image()
        image.source.image_uri = uri

        response = client.text_detection(image=image)
        return self.detect_text(response)

    # Detect the text in a local image
    # Citation: https://cloud.google.com/vision/docs/ocr#detect_text_in_a_local_image
    def detect_text_path(self, path):
        from google.cloud import vision
        import io

        client = vision.ImageAnnotatorClient()

        with io.open(path, "rb") as image_file:
            content = image_file.read()

        image = vision.Image(content=content)

        response = client.text_detection(image=image)
        return self.detect_text(response)

    def detect_text_image(self, image):
        from google.cloud import vision

        contents = cv2.imencode(".png", image)[1].tostring()
        h = hash_contents(contents)

        cr = check_cached(h)
        if cr:
            return cr

        image = vision.Image(content=contents)
        client = vision.ImageAnnotatorClient()
        response = client.text_detection(image=image)
        res = self.detect_text(response)
        write_cache(h, res)
        return res

    # Return a tuple: (bounding_boxes, text_in_bounding_box, txt_to_bb)
    # where text_in_bounding_box[i] is the text inside bounding_boxes[i].
    # and txt_to_bb maps text to its corresponding bounding box
    # A bounding box is an array [(x0,y0), (x1,y1), (x2,y2), (x3,y3)]
    # and the order of the coordinates is as follows:
    # array[0] = top left of the box
    # array[1] = top right
    # array[2]= bottom right
    # array[3]= bottom left
    def detect_text(self, response):
        texts = response.text_annotations

        bounding_boxes = []
        text_in_bounding_box = []
        txt_to_bb = dict()
        for text in texts:
            # print('\n"{}"'.format(text.description))

            # vertices = (['({},{})'.format(vertex.x, vertex.y)
            # for vertex in text.bounding_poly.vertices])
            vertices = [(vertex.x, vertex.y) for vertex in text.bounding_poly.vertices]
            bounding_boxes.append(vertices)
            text_in_bounding_box.append(text.description)
            txt_to_bb[text.description] = vertices
            # print(vertices)
            # print('bounds: {}'.format(','.join(vertices)))
        if response.error.message:
            raise Exception(
                "{}\nFor more info on error messages, check: "
                "https://cloud.google.com/apis/design/errors".format(
                    response.error.message
                )
            )

        # The first bounding box encompasses ALL text
        # and the first text entry is ALL of the text
        # we don't need those
        bounding_boxes = bounding_boxes[1:]
        text_in_bounding_box = text_in_bounding_box[1:]
        return (bounding_boxes, text_in_bounding_box, txt_to_bb)

    # Citation: https://stackoverflow.com/questions/52846474/how-to-resize-text-for-cv2-puttext-according-to-the-image-size-in-opencv-python
    def get_optimal_font_scale(self, text, width, font, thickness):
        for scale in reversed(range(0, 60, 1)):
            textSize = cv2.getTextSize(
                text, fontFace=font, fontScale=scale / 10, thickness=thickness
            )
            new_width = textSize[0][0]
            if new_width <= width:
                return scale / 10
        return 1

    def write_text_in_bounding_box(self, img, bb, text):
        (height, width, n_channels) = img.shape

        # Create blank black image with identical dimensions to our image
        transparent_img = np.zeros((height, width, n_channels), dtype=np.uint8)

        # Make the background white
        transparent_img.fill(255)

        # Indices of coordinates in bounding box array
        top_left = 0
        bottom_right = 2

        white = (255, 255, 255)
        black = (0, 0, 0)

        font = cv2.FONT_HERSHEY_SIMPLEX
        tl_X = bb[top_left][0]
        tl_Y = bb[top_left][1]
        br_X = bb[bottom_right][0]
        br_Y = bb[bottom_right][1]
        width = abs(tl_X - br_X)
        height = abs(tl_Y - br_Y)
        text_loc = (tl_X, int(tl_Y + 0.5 * height))
        thickness = 1
        scale = self.get_optimal_font_scale(text, width, font, thickness)

        cv2.putText(
            transparent_img, text, text_loc, font, scale, black, thickness, cv2.LINE_AA
        )
        return transparent_img
