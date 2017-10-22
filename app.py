import newspaper
from newspaper.article import ArticleException
from flask import Flask, jsonify, request
import logging
import sys
import os

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

    url = original_url
    if not original_url.startswith("http://"):
        url = f"http://{original_url}"

    logger.info("Fetching articles from %s", url)

    data = extract_articles(url)

    return jsonify(data)


def extract_articles(url):
    """
    Extracts all articles below environment variable ARTICLE_AMOUNT or 20 
    :param url: a valid url, with or without http
    :return: a dictionary containing all elements
    """
    paper = newspaper.build(str(url), memoize_articles=False)
    logger.info("Amount of articles found: %s", len(paper.articles))
    data = {
        "total": len(paper.articles),
        "content": [

        ],
        "failed": []
    }
    articles = []
    failed = []
    for index, article in enumerate(paper.articles):
        if "ARTICLE_AMOUNT" in os.environ and index < int(os.environ["ARTICLE_AMOUNT"]) or index < 20:
            try:
                extract_article(article, articles, failed)
            except (Exception, ArticleException):
                logger.error("Failed to parse article, trying to pass remaining articles")
        else:
            break
    data["content"] = articles
    data["failed"] = failed
    logger.debug("Found {} articles".format(len(articles)))
    logger.debug("Failed parsings {}".format(len(failed)))
    logger.info("Retuning data as json")
    return data


def extract_article(article, articles, failed):
    """
    Extract one article, and append it to the articles list
    :param article: Current article metadata
    :param articles: List to append values to
    :param failed:  List to append failed extractions to
    :return: nothing, appends to articles or failed list
    """
    article.download()
    article.parse()
    article.nlp()
    current_article = {}
    for attribute, value in article.__dict__.items():
        if valid_value(value) and str(attribute) != "html":
            current_article[str(attribute)] = value
    if "text" in current_article and current_article["text"] and len(current_article["text"]) > 0:
        articles.append(current_article)
    else:
        failed.append(current_article)


def valid_value(value):
    """
    Check if a value has a valid type in context of converting it to json 
    :param value: value to check for type
    :return: True or False
    """
    try:
        if value and type(value) in [int, float, str, list, dict]:
            return True
        else:
            return False
    except Exception:
        return False

