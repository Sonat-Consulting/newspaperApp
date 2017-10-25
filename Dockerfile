FROM python:3.6.3

COPY . .

RUN pip install -r ./requirements.txt ; curl https://raw.githubusercontent.com/codelucas/newspaper/master/download_corpora.py | python3

HEALTHCHECK CMD curl --fail http://localhost:5000/health || exit 1

CMD ["gunicorn", "--log-level=debug", "--timeout=260", "--bind", "0.0.0.0:5000", "app:app"]
