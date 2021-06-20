from flask import Flask,redirect,url_for,render_template,request,send_file,session
from pytube import YouTube
import time
import urllib.request
import re,ast
import datetime

app=Flask(__name__)
app.config['SECRET_KEY'] = 'kedar'
@app.route('/')
def home():
    html = urllib.request.urlopen("https://www.youtube.com/feed/explore")
    videos = re.findall(r"watch\?v=(\S{11})",html.read().decode())
    for i in range(9):
        videos[i] = "https://www.youtube.com/watch?v="+str(videos[i])
    trend_list = videos[:9]
    for i in range(len(trend_list)):
        session[str(i)] = trend_list[i]
        trend_list[i]=YouTube(session[str(i)])
    return render_template('index.html',list=trend_list,)

@app.route('/static/',methods=['GET', 'POST'])
def downloads():
    if request.method == 'POST':
        if request.form.get("url"):
            url=request.form.get("url")
            session['link'] = url
            url = YouTube(session['link'])  
        else:
            ind = request.form.get("url1")
            session['link']=session[str(ind)]
            url = YouTube(session['link'])  
        return render_template('download.html',  url=url)
        
#filetitle = url.title, filepath = filepath,
@app.route('/download/',methods=['GET', 'POST'])
def download_video():
    if request.method== 'POST':
        url = YouTube(session['link'])
        itag = request.form.get('itag')
        filepath = request.form.get('filepath')
        video = url.streams.get_by_itag(itag)
        filepath = video.download()
        return send_file(filepath, as_attachment=True)
    return render_template('index.html',value='home')
            
if __name__ == '__main__':
    app.run(port=5000,debug=True)