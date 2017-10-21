import newspaper
from flask import Flask, jsonify, request
import logging

app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.setLevel(logging.INFO)


handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)
# fix gives access to the gunicorn error log facility
app.logger.handlers.extend(logging.getLogger("gunicorn.error").handlers)


@app.route("/", methods=["GET"])
def get_articles():
    original_url = request.args.get("url")

    url = original_url
    if not original_url.startswith("http://"):
        url = f"http://{original_url}"

    print("Fetching articles from %s", url)

    paper = newspaper.build(str(url), memoize_articles=False)
    print("Amount of articles found: %s", len(paper.articles))
    data = {
            "total": len(paper.articles),
            "content": [

                ],
            "failed": []
            }
    articles = []
    failed = []
    for index, article in enumerate(paper.articles):
        if index < 20:
            article.download()
            article.parse()
            article.nlp()
            try:
                current_article = {
                    "title": article.title,
                    "text": article.text,
                    "top_image": article.top_image,
                    "summary": article.summary,
                    "keywords": article.keywords,
                    "authors": article.authors,
                    "movies": article.movies,
                    "language": article.meta_lang
                }

                if current_article["text"] and len(current_article) > 0:
                    articles.append(current_article)
                else:
                    failed.append(current_article)
            except Exception as e:
                app.logger.erro("Failed to parse article, trying to pass remaining articles")
        else:
            break

    data["content"] = articles
    data["failed"] = failed
    app.logger.info("Retuning data as json")

    return jsonify(data)
