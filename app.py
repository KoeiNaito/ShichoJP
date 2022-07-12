import flask
from flask import Flask, render_template, send_file
from bs4 import BeautifulSoup as bs
from urllib import request, parse
import json
import subprocess

app = Flask(__name__, static_folder="static")

story_num_list = []
file_name_list = []

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/results", methods=["POST"])
def resutls():
    base_url = flask.request.form["url"]
    base_url = str(base_url).replace(".html", "").replace("detail", "play")
    story_num = flask.request.form["story"]
    story_num_list.append(story_num)
    server_num = flask.request.form["sever_num"]
    file_name = flask.request.form["file_name"]
    file_name_list.append(file_name)

    i = int(story_num)
    url = base_url + "/sid/" + str(server_num) + "/nid/" + story_num + ".html"
    data = None
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"}
    req = request.Request(url, data, headers)
    response = request.urlopen(req)
    html = response.read()
    soup = bs(html, "html.parser")

    scripts = soup.find_all("script")

    target = "var player_aaaa="
    idx = str(scripts[10]).find(target)
    r = str(scripts[10])[idx+len(target):]
    results = r.replace("</script>", "")
    dict_data = json.loads(results)
    url_encoded = dict_data["url"]
    url_decoded = parse.unquote(url_encoded)

    print(url_decoded)
    
    #This is for local. 
    # dir = os.getcwd().replace("\\", "/")
    # ffmpeg_path = dir + "/ShichoJP_downloader/ffmpeg/bin/ffmpeg.exe"
    # output_path = dir + "/ShichoJP_downloader/outputs/output_" + str(i+1) + ".mp4"
    # ffmpeg_command = ffmpeg_path + ' -i ' + url_decoded + ' -c copy -bsf:a aac_adtstoasc ' + output_path
    # subprocess.call(ffmpeg_command, shell=True)

    output_path = "/home/tiramisu/mysite/" + str(file_name) +"_output_" + str(i) + ".mp4"
    ffmpeg_command = "ffmpeg" + ' -i ' + url_decoded + ' -c copy -bsf:a aac_adtstoasc ' + output_path
    subprocess.call(ffmpeg_command, shell=True)

    return send_file(output_path, as_attachment=True, attachment_filename=str(str(file_name)+"_output_"+str(i)+".mp4"))


@app.route("/usage")
def usage():
    return render_template("usage.html")

@app.route("/donate")
def donate():
    return render_template("donate.html")

@app.route("/status", methods=["POST"])
def status():
    story_num = flask.request.form["story"]
    file_name = flask.request.form["file_name"]

    removal_command = "rm " + "/home/tiramisu/mysite/" + str(file_name) + "_output_" + str(story_num) + ".mp4"
    subprocess.call(removal_command, shell=True)
    return render_template("results.html")

if __name__ == "__main__":
    app.run(debug=True)
