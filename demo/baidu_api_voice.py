import base64
import urllib
import requests
import json

API_KEY = "lYEShay5YT17nwTj4T5CU9ye"
SECRET_KEY = "XSygUiSVW8xTIkXqVkoKqFMDoYYkRetQ"

def post():
        
    url = "https://vop.baidu.com/pro_api"
    
    # speech 可以通过 get_file_content_as_base64("C:\fakepath\temp.wav",False) 方法获取
    speech,len = get_file_content_as_base64("/home/YFENG/Desktop/Raspi-car/temp.wav",False)
    print(speech)
    print(len)
    payload = json.dumps({
        "format": "wav",
        "rate": 16000,
        "channel": 1,
        "cuid": "N0AfnEwIjBnyuPaswZ2g5UTwYQPyhj8U",
        "dev_pid": 80001,
        "speech": speech,
        "len": len,
        "token": get_access_token()
    }, ensure_ascii=False)
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload.encode("utf-8"))
    
    print(response.text)
    return response.text
    

def get_file_content_as_base64(path, urlencoded=False):
    """
    获取文件base64编码
    :param path: 文件路径
    :param urlencoded: 是否对结果进行urlencoded 
    :return: base64编码信息
    """
    with open(path, "rb") as f:
        data = f.read()
        length = len(data)
        content = base64.b64encode(data).decode("utf8")
        if urlencoded:
            content = urllib.parse.quote_plus(content)
    return content,length

def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))

if __name__ == '__main__':
    post()
