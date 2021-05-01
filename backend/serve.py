from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import random

app = Flask(__name__)
CORS(app)

@app.route('/')
def main():

    response = {
        "message": "Server is working!"
    }
    return jsonify(response)

@app.route('/derender', methods = ['GET', 'POST'])
def derender():
    try:
        data = json.loads(request.data)
        image_url = data['image']
        print(image_url)
        # run functions

        # return stats
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
        print(e)
        return jsonify({"error": e}), 400

@app.route('/changes', methods = ['GET', 'POST'])
def changes():
    try:
        data = json.loads(request.data)
        edits = data['changes']
        print(edits)

        # do edits and return an image?
        
        response = {
            "message": "Your image"
        }
        return jsonify(response)
    except Exception as e:
        print(e)
        return jsonify({"error": e}), 400

if __name__ == "__main__":
    app.run(debug=True)