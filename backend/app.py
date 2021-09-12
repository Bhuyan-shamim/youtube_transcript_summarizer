from flask import Flask, request, jsonify
from flask_cors import CORS
import datetime
from transformers import pipeline
from youtube_transcript_api import YouTubeTranscriptApi

# define a variable to hold you app
app = Flask(__name__)
CORS(app)


def StringTime(time):
    time = (int)(time)
    return (str)(time // 60) + ":" + (str)(time % 60)


def get_transcript(video_id):
    print("get_transcript")
    summarizer = pipeline('summarization')
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    try:
        duration = min(120, transcript[-1]['start'] // 5)
        i, end, st = 0, 0, 0
        ps_text = ""
        summary_content = []
        while(i < len(transcript)):
            if(end - st < duration):
                end = transcript[i]['start'] + transcript[i]['duration']
                ps_text += transcript[i]['text']
                ps_text += ". "
            else:
                summary_content.append({"start": StringTime(st), "end": StringTime(
                    end), "text": summarizer(ps_text)[0]['summary_text']})
                st = end
                end = transcript[i]['start'] + transcript[i]['duration']
                ps_text = transcript[i]['text']

            i += 1
        summary_content.append({"start": StringTime(st), "end": StringTime(
            end), "text": summarizer(ps_text)[0]['summary_text']})
        print(summary_content)
        return jsonify(summary_content)
    except Exception as e:
        print(e)
        return jsonify([{"start": StringTime(0), "end": StringTime(0), "text": str(e)}])


# define your resource endpoints
@app.route('/')
def index_page():
    print("Home")
    return "<h1>Hello world</h1>"


@app.route('/api/get_summary', methods=['GET'])
def get_summary():
    video_url = request.args.get('youtube_url', '')
    print(video_url)
    video_id = video_url.split("=")[1]
    print(video_id)
    return get_transcript(video_id)


# server the app when this file is run
if __name__ == '__main__':
    app.run(debug=True)
