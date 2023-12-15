from flask import Flask, request, jsonify
import domain
import dataclasses
import os
import dotenv
import utility

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
            "videoId": video.video_id,
            "tsuriScore": min(int(video.like_count * 1000 / video.view_count), 100),
            "tsuriReport": utility.convert_key(dataclasses.asdict(video), utility.snake2camel)
        } if isinstance(video, domain.Video) else {
            "status": f"ERROR: {video.error_message}",
            "videoId": video.video_id,
            "tsuriScore": -1,
        } for video in videos]

    video_ids = parse_video_ids(request.args["videoId"])
    return jsonify({
        "items": create_items(video_ids)
    })


app.run(host="0.0.0.0", port=40000, debug=True)
