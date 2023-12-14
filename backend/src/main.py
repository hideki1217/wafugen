from flask import Flask, request

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/v1/report")
def create_report():
    def parse_video_ids(s: str):
        return s[1:-1].split(",")

    def create(video_id):
        return {
            "video_id": video_id,
            "tsuri_score": 50,
            "tsuri_report": {
                "example": "*"
            }
        }

    video_ids = parse_video_ids(request.args["video_id"])

    return {
        "items": [create(video_id) for video_id in video_ids]
    }


app.run(host="0.0.0.0", port=40000, debug=True)
