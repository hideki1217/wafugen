from flask import Flask, request, jsonify, make_response
import domain
import computer_vision
import os
import dotenv
import utility
import sys

dotenv.load_dotenv()
youtube = domain.Youtube(os.environ["GOOGLE_API_KEY"])
vision = computer_vision.Vision(
    os.environ["AZURE_VISION_KEY"], os.environ["AZURE_VISION_ENDPOINT"])

app = Flask(__name__)
app.json.ensure_ascii = False


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
            "tsuriReport":
                utility.asdict_camel(video) | {"image_tag": [
                    caption for caption in vision.read(video.thumbnail_standard.url)],
                "transcript": youtube.video_transcript(video.video_id)}
        } if isinstance(video, domain.Video) else {
            "status": f"ERROR: {video.error_message}",
            "videoId": video.video_id,
            "tsuriScore": -1,
        } for video in videos]

    video_ids = parse_video_ids(request.args["videoId"])
    response = jsonify({
        "items": create_items(video_ids)
    })
    response.status_code = 200
    response.headers["Cache-Control"] = "max-age=604800"
    return response


app.run(host="0.0.0.0", port=int(sys.argv[1]), debug=True)
