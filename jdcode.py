import os
import requests
from flask_cors import CORS
from flask import Flask, request, render_template
import json
import subprocess
from update import Update
import configparser

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app, supports_credentials=True)
conf = configparser.ConfigParser()
conf.read("./config.ini", encoding='UTF-8')


@app.route('/getCode', methods=['POST'])
def get_code():
    data = json.loads(request.get_data())
    phone = data["phone"]
    print(data)
    cmd = './getcode.sh {}'.format(phone)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.wait()
    # out = p.stdout.read()
    out = p.stdout.readlines()
    print(out)
    if 'success' in str(out[-1]):
        return {'code':'200',"message":"获取成功"}
    else:
        return {'code':'400',"message":"获取失败"}


@app.route('/sendCode', methods=['POST'])
def input_code():
    data = json.loads(request.get_data())
    print(data)
    phone = data["phone"]
    code = data ["code"]
    cmd = './inputcode.sh {} {}'.format(phone,code)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = p.stdout.readlines()
    print(out)
    if 'pt_key' in str(out[-1]):
        qlckfile = '{}qlck'.format(phone)
        with open(qlckfile, 'r') as f:
            qlck = f.read()
            send_dding(phone,qlck)
            Update(qlck,phone).match_ck()
        os.remove(qlckfile)
        return {'code':'200',"message":"获取成功","qlck":qlck}
    else:
        return {'code':'400',"message":"获取失败"}


def send_dding(phone,text):
    #钉钉的机器人token，校验关键字为ck
    token = conf["dding"].get("token")
    url = "https://oapi.dingtalk.com/robot/send?access_token=" + token
    payload = json.dumps({
        "text": {
            "content": phone+"ck:"+text
        },
        "msgtype":"text"
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)


if __name__ == '__main__':

    app.run(debug=True, host='0.0.0.0', port=6000)


