
from flask import Flask, jsonify, request
import logging
import sys
import os
from extractor import extract_articles

app = Flask(__name__)


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


@app.route("/health", methods=["GET"])
def health_check():
    logger.debug(os.environ["LOG_LEVEL"])
    logger.debug(os.environ["ARTICLE_AMOUNT"])
    return jsonify({"status": "healty"}), 200


@app.route("/", methods=["GET"])
def get_articles():
    original_url = request.args.get("url")



    amount = 20
    if "ARTICLE_AMOUNT" in os.environ:
        amount = int(os.environ["ARTICLE_AMOUNT"])
    data = extract_articles(original_url, amount)

    return jsonify(data)


