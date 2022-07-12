from bs4 import BeautifulSoup as bs
from urllib import request, parse
import json
import subprocess
import os

base_url = "https://shichojp.net/index.php/vod/play/id/143187/"
story_num = 12

for i in range(story_num):
    url = base_url + "sid/7/nid/" + str(i+1) + ".html"
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
    print(results)
    dict_data = json.loads(results)
    url_encoded = dict_data["url"]
    url_decoded = parse.unquote(url_encoded)

    print(url_decoded)

    dir = os.getcwd().replace("\\", "/")
    ffmpeg_path = dir + "/ShichoJP_downloader/ffmpeg/bin/ffmpeg.exe"
    output_path = dir + "/ShichoJP_downloader/outputs/output.mp4"
    ffmpeg_command = ffmpeg_path + ' -i ' + url_decoded + ' -c copy -bsf:a aac_adtstoasc ' + output_path
    subprocess.call(ffmpeg_command, shell=True)