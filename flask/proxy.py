from flask import Flask
from flask import Response
from flask import stream_with_context

import requests

app = Flask(__name__)

@app.route('/.json', methods=["POST"])
def home():
    req = requests.get("http://23.96.26.252:5000/.json", stream = True)
    return Response(stream_with_context(req.iter_content()), content_type = req.headers['content-type'])

if __name__ == '__main__':
	app.run(debug=True, host="0.0.0.0")