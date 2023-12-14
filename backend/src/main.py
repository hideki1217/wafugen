from flask import Flask, request
import domain
import dataclasses
import os
import dotenv

dotenv.load_dotenv()
youtube = domain.Youtube(os.environ["GOOGLE_API_KEY"])

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/v1/report")
def create_report():
    def parse_video_ids(s: str):
        return s.split(",")

    def create_items(video_ids):
        videos = youtube.video_summary(video_ids)

        return [{
            "status": "ok",
            "video_id": video.video_id,
            "tsuri_score": min(int(video.like_count * 1000 / video.view_count), 100),
            "tsuri_report": dataclasses.asdict(video)
        } if isinstance(video, domain.Video) else {
            "status": f"ERROR: {video.error_message}",
            "video_id": video.video_id,
            "tsuri_score": -1,
        } for video in videos]

    video_ids = parse_video_ids(request.args["video_id"])
    return {
        "items": create_items(video_ids)
    }


app.run(host="0.0.0.0", port=40000, debug=True)
