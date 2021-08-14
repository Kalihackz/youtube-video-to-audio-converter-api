from flask import Flask,send_file,request
import os , io
from pytube import YouTube
from multiprocessing import Process

app = Flask(__name__)

@app.route('/')
def index():
    return 'Video to Audio Converter API<br>API link : https://audio.kalihackz.repl.co/api/v1/download?link=[youtube_link]]'

@app.route('/api/v1/download')
def download_file():
    video_link = request.args.get("link")
    try:
        video = YouTube(video_link)
        audio = video.streams.filter(only_audio=True, file_extension='mp4').first()
        audio.download(os.getcwd())
        file = ((audio.download())[19:])

        return_data = io.BytesIO()
        with open(file, 'rb') as fo:
            return_data.write(fo.read())

        return_data.seek(0)
        task = Process(target=rm(file))
        task.start()

        return send_file(return_data,as_attachment=True,download_name=(file+'.mp3'),mimetype='audio/mp3')

    except Exception as e:
         return {"error":""+str(e)}

def rm(path):
    os.remove(path)
        
app.run(port=3000,host='0.0.0.0',debug=True)
