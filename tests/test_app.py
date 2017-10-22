import flask

app = flask.Flask(__name__)

# TODO: Expand this


def test_params():

    with app.test_request_context("/?url=http://vg.no"):
        assert flask.request.path == "/"
        assert flask.request.args["url"] == "http://vg.no"
