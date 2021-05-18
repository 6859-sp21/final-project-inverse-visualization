from werkzeug.middleware.proxy_fix import ProxyFix
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import json
import random
import inverter
from PIL import Image
from io import BytesIO, StringIO
import base64
import numpy as np
from config import DEBUG
import requests

import tensorflow as tf

gpus = tf.config.experimental.list_physical_devices("GPU")
if gpus:
    try:
        # Currently, memory growth needs to be the same across GPUs
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        logical_gpus = tf.config.experimental.list_logical_devices("GPU")
        print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
    except RuntimeError as e:
        # Memory growth must be set before GPUs have been initialized
        print(e)

app = Flask(__name__, static_folder="./dist/static", template_folder="./dist")
CORS(app)

inv = inverter.Inverter()

if DEBUG:
    # If we're sitting behind a proxy, all redirects and such are wonky.
    # nginx handles this gracefully, but the webpack dev server doesn't.
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_host=1)


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    """Catch all route to serve the frontend.
    """

    return render_template("index.html")


@app.route("/api/image", methods=["POST"])
def b64image():
    url = request.json.get("url", None)
    r = requests.get(url)
    img = Image.open(BytesIO(r.content))
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = "data:image/png;base64," + base64.b64encode(buffered.getvalue()).decode(
        "utf-8"
    )

    return img_str


@app.route("/api/decompile", methods=["POST"])
def decompile():
    b64 = request.json.get("image", None)
    if b64 is None:
        return "No image"

    b64 = b64.split(",")[-1]
    img = Image.open(BytesIO(base64.b64decode(b64)))
    img = np.uint8(img)
    img = img[:, :, :3]

    meta = inv.derender(img)
    return jsonify(meta)


@app.route("/api/compile", methods=["POST"])
def compile():
    meta = request.json["meta"]
    img = inv.render(meta)

    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = "data:image/png;base64," + base64.b64encode(buffered.getvalue()).decode(
        "utf-8"
    )

    return img_str


@app.route("/derender", methods=["GET", "POST"])
def derender():
    try:
        data = json.loads(request.data)
        image_url = data["image"]
        print(image_url)
        # run functions

        # return stats
        stats = []
        for i in range(10):
            stats.append(
                {
                    "text": "tip " + str(i),
                    "x": random.randint(0, 400),
                    "y": random.randint(0, 200),
                }
            )
        response = {
            "message": "Your stats",
            "stats": stats,
        }
        return jsonify(response)
    except Exception as e:
        print(e)
        return jsonify({"error": e}), 400


@app.route("/changes", methods=["GET", "POST"])
def changes():
    try:
        data = json.loads(request.data)
        edits = data["changes"]
        print(edits)

        # do edits and return an image?

        response = {"message": "Your image"}
        return jsonify(response)
    except Exception as e:
        print(e)
        return jsonify({"error": e}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8112)
