from flask import Flask, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

@app.route('/')
def main():

    response = {
        "message": "Server is working!"
    }
    return jsonify(response)

@app.route('/derender')
def derender():
    try:
        response = {
            "message": "Your stats",
            "stats": (random.randint(0,100),random.randint(0,100)),
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": e}), 400


if __name__ == "__main__":
    app.run(debug=True)