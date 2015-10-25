from flask import Flask
import json, sys, datetime, request, Response

app = Flask(__name__)

@app.route("/.json", methods=["POST"])
def main():
	url = request.form['url']
	referer = request.form['referer']
	date = datetime.datetime.now()

