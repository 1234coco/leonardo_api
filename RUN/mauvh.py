import requests
import json
from PIL import Image
from urllib.request import urlretrieve
from selenium import webdriver
import threading
import os
import time
import shutil
from deep_translator.google import GoogleTranslator
# Define headers
def get_user_token(cookie=None):
    header = {
        'authority':'app.leonardo.ai',
        'Accept-Language':'vi,en-US;q=0.9,en;q=0.8',
        'Cookie':cookie,
    }
    # Gửi yêu cầu HTTP
    response = requests.get("https://app.leonardo.ai/api/auth/session", headers=header)
    print(response.text)
    return response.text
def Authentication(token = None):
    headers = {
        "authority": "api.leonardo.ai",
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5",
        "authorization": f"Bearer {token}",
        "origin": "https://app.leonardo.ai",
        "referer": "https://app.leonardo.ai/",
    }
    return headers
def GenarationImage(Authen = None,Input="fire"):
    inp = translat(Input)
    payload = {
        "operationName": "CreateSDGenerationJob",
        "variables": {
            "arg1": {
                "prompt": inp,
                "negative_prompt": "",
                "nsfw": True,
                "num_images": 4,
                "width": 640,
                "height": 832,
                "num_inference_steps": 10,
                "guidance_scale": 7,
                "sd_version": "v1_5",
                "modelId": "ac614f96-1082-45bf-be9d-757f2d31c174",
                "presetStyle": "LEONARDO",
                "scheduler": "LEONARDO",
                "public": False,
                "tiling": False,
                "leonardoMagic": False,
                "poseToImage": False,
                "poseToImageType": "POSE",
                "weighting": 0.75,
                "highContrast": False,
                "elements": [],
                "controlnets": [],
                "photoReal": False
            }
        },
        "query": "mutation CreateSDGenerationJob($arg1: SDGenerationInput!) {\n sdGenerationJob(arg1: $arg1) {\n generationId\n __typename\n }\n}"
    }
    response = requests.post("https://api.leonardo.ai/v1/graphql", headers=Authen, json=payload)

    return response
def URL(user_id=None, response=None, prompt="fire"):
    inp = translat(prompt)
    prompt = inp
    lists = json.loads(response.text)
    url_normal = "https://cdn.leonardo.ai/users/"
    ids = lists["data"]["sdGenerationJob"]["generationId"]
    list_url = []
    Character = [r"`",r"~",r"!",r"@",r"#",r"$",r"%",r"^",r"&",r"*",r"(",r")",r"-",r"_",r"+",r"=",r"{",r"}",r"[",r"]",r";",r":",r"'",r'"',r",",r"<",r".",r">",r"/",r"?"]
    for Ch in Character:
        prompt = prompt.replace(Ch,"")
    list_url.append(url_normal + user_id + "/" + "generations/" + ids + "/" + f"Default_{prompt.replace(r' ', r'_')}_0.jpg")
    list_url.append(url_normal + user_id + "/" + "generations/" + ids + "/" + f"Default_{prompt.replace(r' ', r'_')}_1.jpg")
    list_url.append(url_normal + user_id + "/" + "generations/" + ids + "/" + f"Default_{prompt.replace(r' ', r'_')}_2.jpg")
    list_url.append(url_normal + user_id + "/" + "generations/" + ids + "/" + f"Default_{prompt.replace(r' ', r'_')}_3.jpg")
    be = url_normal + user_id + "/" + "generations/" + ids + "/"
    print(list_url)
    return list_url , be
def get_user_id(token = None,userSub=None):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        # Add other headers if needed
    }

    body = {
        "operationName": "GetUserDetails",
        "variables": {
            "userSub": userSub
        },
        "query": """
            query GetUserDetails($userSub: String) {
                users(where: {user_details: {cognitoId: {_eq: $userSub}}}) {
                    id
                    username
                    blocked
                }
            }
        """
    }

    respon = requests.post("https://api.leonardo.ai/v1/graphql",headers=headers,json=body)
    re = json.loads(respon.text)
    print(respon.text)
    idss = re["data"]["users"][0]["id"]
    print(idss)
    return idss
def show_image(Images=None, lists=None, cook=None):
    def openimage(url=None, lists=None):
        name_file = url.replace(lists, "")
        path = os.getcwd() + "\\RUN"
        print(url)
        os.system(f"{path}\\curl.exe -o {path}\\Temp\\{name_file} -l {url}")
        time.sleep(2)
        return f"{path}\\Temp\\{name_file}"

    def runs(n =None):
        pa = openimage(n, lists=lists)
        img = Image.open(pa)
        img.show()

    thread_list = []
    for _ in Images:
        t = threading.Thread(target=runs,args={_})
        thread_list.append(t)
        t.start()

    for t in thread_list:
        t.join()
def translat(name):
    string = GoogleTranslator(source="auto",target="en").translate(name)
    return string
def save_image(name=str(),url=list(),dst=str()):
    for i in range(4):
        file = "RUN\\Temp\\"+url[i].replace(name,"")
        print(file)
        shutil.copy2(file,dst=dst)
    
    
    
#def show_image(Images = None,lists = None,cook = None):
#    def openimage(url = None,lists=None):
#        name_file = url.replace(lists,"")
#        path = os.getcwd() + "\\RUN"
#        print(url)
#        os.system(f"{path}\\curl.exe -o {path}\\Temp\\{name_file} -l {url}")
#        time.sleep(2)
#        return f"{path}\\Temp\\{name_file}"
#    for n in Images:
#        def runs():
#            name_file = os.getcwd() + "\\RUN\\Temp\\" +n.replace(lists,"")
#            pa = openimage(n,lists=lists)
#            img = Image.open(name_file) 
#            img.show()
#        g = threading.Thread(target=runs)
#        g.run()
#        g.join()
    



    



# Send request



