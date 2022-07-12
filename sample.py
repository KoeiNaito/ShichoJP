import subprocess
import os

url_decoded = "https://m3u.if101.tv/xm3u8/3a3104ef0007c39f9ca0a40f574e6ccb024272a02bdac314c5c2f72710fc4fe89921f11e97d0da21.m3u8"
url_int = 1

dir = os.getcwd().replace("\\", "/")
ffmpeg_path = dir + "/ShichoJP_downloader/ffmpeg/bin/ffmpeg.exe"
output_path = dir + "/ShichoJP_downloader/outputs/output_" + str(url_int) + ".mp4"
ffmpeg_command = ffmpeg_path + ' -i ' + url_decoded + ' -c copy -bsf:a aac_adtstoasc ' + output_path
subprocess.call(ffmpeg_command, shell=True)

    # dir = os.getcwd().replace("\\", "/")
    # output_path = dir + "/ShichoJP_downloader/outputs/output_" + str(i+1) + ".mp4"
    # ffmpeg_command = "ffmpeg" + ' -i ' + url_decoded + ' -c copy -bsf:a aac_adtstoasc ' + output_path
    # subprocess.call(ffmpeg_command, shell=True)


import subprocess
from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    url_decoded = "https://m3u.if101.tv/xm3u8/3a3104ef0007c39f9ca0a40f574e6ccb024272a02bdac314c5c2f72710fc4fe89921f11e97d0da21.m3u8"
    url_int = 1
    output_path = "output_" + str(url_int) + ".mp4"
    ffmpeg_command = "ffmpeg" + ' -i ' + url_decoded + ' -c copy -bsf:a aac_adtstoasc ' + output_path
    subprocess.call(ffmpeg_command, shell=True)

    return "Finish"