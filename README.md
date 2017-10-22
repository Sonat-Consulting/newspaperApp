# Python Flask app demo of newspaper

Simple python application showing off the newspaper package using python flask, and exposing
a rest api against it.

## To run this with docker-compose

1. docker-compose up -d
2. point your browser to
    1. http://localhost:5555?url=https://bt.no/
    
    
## To run this with docker
1. docker build -t newspaper .
2. docker run --name newspaper -d -p 5000:5000 newspaper
3. point your browser to
    1. http://localhost:5000/?url=http://vg.no
    
## To run test
1. Download nltk models 
    1. curl https://raw.githubusercontent.com/codelucas/newspaper/master/download_corpora.py | python3
2. pip install -r requirements
3. pytest tests/