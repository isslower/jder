
#更新到青龙面板

import requests
import json
import re
import time

class Update():

    def __init__(self,ck=None,phone=None):
        #青龙面板地址、账号密码
        self.host = "http://192.168.31.104:5800/"
        self.name = ""
        self.password = ""
        self.ck = ck
        self.token = self.get_token()
        self.phone = phone


    def get_token(self):
        t = int(round(time.time() * 1000))
        url = self.host + "api/user/login?t="+str(t)
        payload = json.dumps({
            "username": self.name,
            "password": self.password
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload).json()
        print("获取token:",response)
        return response["data"]["token"]

    # 比对ck进行更新，如果未启用，进行启用
    def match_ck(self):
        pt_pin = str(re.findall(r"pt_pin=(.+?);", self.ck)[0])
        print("pt_pin:",pt_pin)
        cklist = self.get_all_ck()
        for i in cklist:
            if pt_pin in str(i["value"]):
                id = i["_id"]
                remark = i["remarks"]
                print("开始更新",remark,"的ck")
                self.update_ck(remark,id)
                if i["status"] == 1:
                    print("启用成功")
                    self.start_ck(id)
                return
        self.add_ck()
        return

    # 获取所有的变量
    def get_all_ck(self):
        t = int(round(time.time() * 1000))
        url = self.host + "api/envs?searchValue=&t="+str(t)
        payload = ""
        headers = {
            'Authorization': 'Bearer '+self.token
        }
        response = requests.request("GET", url, headers=headers, data=payload).json()
        # print(response["data"])
        return response["data"]

    # 更新变量
    def update_ck(self,remark=None,id=None):
        t = int(round(time.time() * 1000))
        url = self.host+"api/envs?t="+str(t)
        payload = json.dumps({
            "name": "JD_COOKIE",
            "value": self.ck,
            "remarks": remark,
            "_id": id
        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer '+self.token
        }
        # print(payload)
        response = requests.request("PUT", url, headers=headers, data=payload)
        return


    def add_ck(self):
        t = int(round(time.time() * 1000))
        url = self.host+"api/envs?t="+str(t)
        payload = json.dumps([
            {
                "value": self.ck,
                "name": "JD_COOKIE",
                "remarks": self.phone
            }
                ])
        headers = {
            'Authorization': 'Bearer '+self.token,
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        return


    def start_ck(self,id):
        t = int(round(time.time() * 1000))
        url = self.host+"api/envs/enable?t="+str(t)
        print(id)
        list=[]
        list.append(id)
        payload = json.dumps(
            list
        )
        headers = {
            'Authorization': 'Bearer '+self.token,
            'Content-Type': 'application/json'
        }
        print("启用ck：",payload)
        response = requests.request("PUT", url, headers=headers, data=payload)
        return





if __name__ == '__main__':

    ck = 'pt_key=33JiC5lOADBAJIqAX8UDhNHkh_qypfyAyQkqWu5ADdZgHkudbNtdlSkBEOIMxO73oT_npf__Hvc;pt_pin=jd_67r828540e7yd;'
    phone = '13486329823'
    id = "y27oepazezEkR85x"
    Update(ck,phone).match_ck()


