from flask import Flask, request

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/v1/report")
def create_report():
    def parse_youtube_ids(s: str):
        assert s[0] == "[" and s[-1] == "]"
        return s[1:-1].split(",")

    youtube_ids = parse_youtube_ids(request.args["youtube_ids"])

    return [{
        "youtube_id": youtube_id,
        "tsuri_score": 50,
        "tsuri_report": {
            "example": 10
        }
    } for youtube_id in youtube_ids]


app.run(host="0.0.0.0", port=40000, debug=True)
