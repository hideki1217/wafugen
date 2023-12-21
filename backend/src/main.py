from flask import Flask, request, jsonify, make_response
import domain
import chat
import computer_vision
import os
import dotenv
import sys
import json

dotenv.load_dotenv()
youtube = domain.Youtube(os.environ["GOOGLE_API_KEY"])
vision = computer_vision.Vision(
    os.environ["AZURE_VISION_KEY"], os.environ["AZURE_VISION_ENDPOINT"])
chatbot = chat.ChatBot(os.environ["OPENAI_API_BASE"], os.environ[
    "OPENAI_API_VERSION"], os.environ["OPENAI_API_KEY"], os.environ["OPENAI_API_ENGINE"])

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

        def ask_to_chatbot(thumbnail_texts: list[str], title: str, transcript: list[domain.TranscriptSegment]):
            thumbnail_text = '\n'.join(thumbnail_texts)
            transcripts = ','.join([seg.text for seg in transcript])
            transcripts = transcripts[:min(10000, len(transcripts))]

            prompt = f"""以下のテキストから期待される動画コンテンツと実際の動画コンテンツとがどの程度剥離しているかを判定してください.
まず、サムネイルに含まれる文字列とタイトルから期待される動画コンテンツを素直で好意的な視点で端的に推定し、要約してください。
次に、動画コンテンツの字幕から実際の動画コンテンツを網羅的視点で水平思考を用いて推定し、要約してください。
最後に、期待される動画コンテンツの内容に対する実際の動画コンテンツの内容の納得感を0から100の整数で定量化し、その根拠を述べてください。

希望する出力形式:
{{
    "期待される動画コンテンツの要約": \"-||-\",
    "実際の動画コンテンツの要約": \"-||-\",
    "納得感": 0から100の整数,
    "根拠": \"-||-\"
}}

サムネイルに含まれる文字列: \"\"\"
{thumbnail_text}
\"\"\"

タイトル: \"\"\"
{title}
\"\"\"

動画コンテンツの字幕の先頭1000文字: \"\"\"
{transcripts}
\"\"\"

出力: \n
"""
            response = chatbot.create(
                [chat.Message('system', prompt).asdict()])
            print(response)
            return response

        def score_item(video: domain.Video):
            try:
                thumbnail_texts = vision.read(video.thumbnail_standard.url)
                transcript = youtube.video_transcript(video.video_id)
                title = video.title

                response = ask_to_chatbot(thumbnail_texts, title, transcript)
                assert len(response) == 1
                assert response[0].role == "assistant"
                content = response[0].content

                return content
            except:
                # HACK: grasp all exception
                return None

        def try_parse_json(s):
            try:
                return json.loads(s)
            except:
                return "error"

        contents = []
        for video in videos:
            if isinstance(video, domain.Video) and (score_info_str := score_item(video)) is not None:
                score_value = 100 - \
                    int(score_info_str[score_info_str.find(
                        "\"納得感\": ") + len("\"納得感\": "):][:2].strip())

                contents.append(
                    {
                        "status": "ok",
                        "videoId": video.video_id,
                        "tsuriScore": score_value,
                        "tsuriReport": {
                            "try_parse_json": try_parse_json(score_info_str),
                            "raw": score_info_str
                        }
                    }
                )
            else:
                contents.append(
                    {
                        "status": f"ERROR: {getattr(video, 'error_message', '')}",
                        "videoId": video.video_id,
                        "tsuriScore": -1,
                    }
                )
        return contents

    video_ids = parse_video_ids(request.args["videoId"])
    response = jsonify({
        "items": create_items(video_ids),
    })
    response.status_code = 200
    response.headers["Cache-Control"] = "max-age=604800"
    return response


app.run(host="0.0.0.0", port=int(sys.argv[1]), debug=True)
