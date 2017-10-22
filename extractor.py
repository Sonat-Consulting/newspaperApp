import newspaper
from newspaper.article import ArticleException
import logging

logger = logging.getLogger()


def extract_articles(source_url, amount):
    """
    Extracts all articles below environment variable ARTICLE_AMOUNT or 20 
    :param 
        source_url: an url, with or without http
        amount: an int with amount of articles to download data for
    :return: a dictionary containing all elements
    """
    url = source_url

    if not source_url.startswith("http://") and not source_url.startswith("https://"):
        url = f"http://{source_url}"

    logger.info("Fetching articles from %s", url)

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
        if len(articles) < amount:
            try:
                extract_article(article, articles, failed)
            except (Exception, ArticleException) as e:
                logger.error("Failed to parse article, trying to pass remaining articles because of %s", e)
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

