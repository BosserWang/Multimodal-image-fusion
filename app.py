from flask import Flask, render_template, send_from_directory, request
from flask_cors import CORS
import json
import time
import os
from test import main
from RGB2YCrCb import RGB_main
from Blend_images import Blend_main

app = Flask(__name__)
CORS(app)


class MyHttpResponse:
    def __init__(self, code=200, data=None, msg=''):
        if data is None:
            data = {}
        self.code = code
        self.data = data
        self.msg = msg

    def to_json_resp(self):
        return obj_to_json(
            {
                'code': self.code,
                'data': self.data,
                'msg': self.msg
            }
        )


@app.route('/')
def index():  # put application's code here
    return render_template('index.html')



@app.route('/detection')
def detection():
    return render_template('detection.html')

@app.route('/fusion')
def fusion():
    return render_template('fusion.html')

@app.route('/process')
def process():
    return render_template('process.html')

@app.route('/result')
def result():
    return render_template('result.html')


@app.route('/login', methods=['POST'])
def login():
    params = request.get_json()
    print(params)
    resp = MyHttpResponse()
    if params['username'] == 'admin':
        if params['password'] == '123456':
            resp.data = '1'
        else:
            resp.data = '0'
    else:
        resp.data = '-1'
    return resp.to_json_resp()


@app.route("/getInfraredPic", methods=['POST'])
def getInfraredPic():
    resp = MyHttpResponse()
    if 'file' not in request.files:
        resp.data = '-1'
        return resp.to_json_resp()
    file = request.files['file']
    if file.filename == '':
        resp.data = '0'
        return resp.to_json_resp()
    if file:
        del_files('./images/Infrared')
        filename = file.filename
        file.save('./images/Infrared/' + filename)
        resp.data = ""
        resp.msg = ""
        return resp.to_json_resp()


@app.route("/getVisiblePic", methods=['POST'])
def getVisiblePic():
    resp = MyHttpResponse()
    if 'file' not in request.files:
        resp.data = '-1'
        return resp.to_json_resp()
    file = request.files['file']
    if file.filename == '':
        resp.data = '0'
        return resp.to_json_resp()
    if file:
        del_files('./images/Visible')
        filename = file.filename
        file.save('./images/Visible/' + filename)
        resp.data = ""
        resp.msg = ""
        return resp.to_json_resp()
@app.route("/getResult", methods=['POST'])
def getResult():
    del_files('./result/detection')
    del_files('./result/fusion')
    resp = MyHttpResponse()
    start_time = time.time()
    resp.data = main()
    RGB_main(resp.data)
    Blend_main(resp.data)
    end_time = time.time()
    resp.msg = end_time - start_time
    return resp.to_json_resp()

def del_files(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')


@app.route("/showHomeImage/<path:filename>")
def show_home_image(filename):
    return send_from_directory('home_images', filename)

@app.route("/showResDetectionImage/<path:filename>")
def show_detection_image(filename):
    return send_from_directory('result/detection', filename)

@app.route("/showResFusionImage/<path:filename>")
def show_fusion_image(filename):
    return send_from_directory('result/fusion', filename)
@app.route("/showProcessImage/<path:filename>")
def show_process_image(filename):
    return send_from_directory('process', filename)

def obj_to_json(obj):
    return json.dumps(obj)


if __name__ == '__main__':
    app.run()
