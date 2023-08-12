import torch
import torchvision.transforms as transforms
from PIL import Image
from flask import Flask, jsonify, request, render_template, send_file, Response, url_for
from io import BytesIO
import io, cv2
import json
import numpy as np
import os,time
import glob
import base64
from yolo import YOLO
import config

app = Flask(__name__)
from predict import detect
from yolo import YOLO

app.config.from_object(config)
global i
i=0
yolo = YOLO()
books = [
    {"id": 1, "name": "三国演义"},
    {"id": 2, "name": "水浒传"},
    {"id": 3, "name": "红楼梦"},
    {"id": 4, "name": "西游记"},
]
flag ={}
flag["flag"] = 1
resSets = {}

@app.route("/predict", methods=['get', 'post'])  #
def predict():
    image = base64.b64decode(request.form.get("image"))
    bytes_stream = BytesIO(image)
    image = Image.open(bytes_stream)
    r_image = yolo.detect_image(image, crop=True, count=False)
    num = flag["flag"]
    last_num = num-1
    num = str(num)
    last_num = str(last_num)
    print("num" ,num)
    if num!='1':
        os.remove("./static/" + last_num + ".jpg")
    r_image.save("./static/"+num+".jpg")
    resSets["resurl"] = "http://10.3.4.163:5000" +  "/static/"+num+".jpg"
    flag["flag"] = flag["flag"]+1
    print(resSets["resurl"])

    return jsonify(resSets)

@app.route("/video", methods=['get', 'post'])  #
def video():
    num = flag["flag"]
    last_num = num - 1
    num = str(num)
    last_num = str(last_num)
    request_video_save_path = "demo.mp4"
    video_save_path = "./static/video.mp4"
    video_fps = 25.0

    #接收前端文件
    file_obj = request.files.get('file')
    if file_obj is None:
        print("没有发送文件")
    file_obj.save(request_video_save_path)
    return '1'

@app.route('/pic')
def pic():  # put application's code here
    num1 = flag["flag"]
    num1 = str(num1)
    flag_url_img = "./static/"+num1+".jpg"
    return render_template('index1.html', flag_url_img)

@app.route('/index')

def index():
    return render_template('index2.html')

def gen():
    video_path = 'demo.mp4'
    video_path = 0 # 0是本地摄像头，1是外接摄像头。不加引号！！！！！！！！！！！
    vid = cv2.VideoCapture(video_path)
    while True:
        return_value, frame = vid.read()
        frame = cv2.flip(frame, 1)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # 转变成Image
        frame = Image.fromarray(np.uint8(frame))
        # 进行检测
        frame = np.array(yolo.detect_image(frame))
        # RGBtoBGR满足opencv显示格式
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        image = cv2.imencode('.jpg', frame)[1].tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def hello_world():  # put application's code here
    return 'hello world !!'


if __name__ == '__main__':
    app.run(host="10.3.4.163", port=5000)  # 校园网 10.61.202.250  网线10.3.4.163
