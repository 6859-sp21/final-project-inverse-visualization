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
        stats = []
        for i in range(10):
            stats.append({
                'text': 'tip ' + str(i),
                'x': random.randint(0,400),
                'y': random.randint(0,200)})
        response = {
            "message": "Your stats",
            "stats": stats,
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": e}), 400


if __name__ == "__main__":
    app.run(debug=True)