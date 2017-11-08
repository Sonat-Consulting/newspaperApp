
from flask import Flask, jsonify, request
import logging
import sys
import os
from flask_cors import CORS
from flask_cors import cross_origin

from extractor import extract_articles

app = Flask(__name__)
CORS(app)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healty", "ARTICLE_AMOUNT": os.environ["ARTICLE_AMOUNT"]}), 200


@cross_origin()
@app.route("/", methods=["GET"])
def get_articles():
    original_url = request.args.get("url")
    request_amount = request.args.get("amount")

    amount = 0
    if request_amount:
        amount = int(request_amount)
    elif request.args.get("size"):
        amount = int(request.args.get("size"))
    elif "ARTICLE_AMOUNT" in os.environ:
        amount = int(os.environ["ARTICLE_AMOUNT"])
    logger.info("Using size, %s", amount)
    data = extract_articles(original_url, amount)

    return jsonify(data)


