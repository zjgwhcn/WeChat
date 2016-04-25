import urllib.request
import json

# AppID = 'wx5648d7ee9a4be6e2'
# AppSecret = 'd4171e1e4860901c95d56aa9d81038b5'
AppID = 'wx6b11c0a7c39c89bb'
AppSecret = 'f8dce47284bab8aa55e1ffd7798eab39'
url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (
    AppID, AppSecret)

result = urllib.request.urlopen(url).read().decode()
access_token = json.loads(result).get('access_token')
print(access_token)
url = 'https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s' % access_token

data = {
    "button": [
        {
            "name": "监控",
            "sub_button": [
                {
                    "type": "click",
                    "name": "获取温湿度",
                    "key": "V1001_TEMPERATURE"
                },
                {
                    "type": "click",
                    "name": "实况截图",
                    "key": "V1001_SCREENSHOT"
                },
                {
                    "type": "click",
                    "name": "实时监控",
                    "key": "V1001_MONITOR"
                },
                {
                    "type": "click",
                    "name": "开启安全预警",
                    "key": "V1001_AUTOSAFE_ON"
                },
                {
                    "type": "click",
                    "name": "关闭安全预警",
                    "key": "V1001_AUTOSAFE_OFF"
                }                
            ]
        },
        {
            "name": "操作",
            "sub_button": [
                {
                    "type": "click",
                    "name": "摄像头左转45°",
                    "key": "V1001_LEFT"
                },
                {
                    "type": "click",
                    "name": "摄像头右转45°",
                    "key": "V1001_RIGHT"
                },
                {
                    "type": "click",
                    "name": "开启自动旋转",
                    "key": "V1001_AUTOMOVE_ON"
                },
                {
                    "type": "click",
                    "name": "关闭自动旋转",
                    "key": "V1001_AUTOMOVE_OFF"
                }
            ]
        }
    ]
}

req = urllib.request.Request(url)
req.add_header('Context-Type', 'application/json')
req.add_header('encoding', 'utf-8')

response = urllib.request.urlopen(
    req, json.dumps(data, ensure_ascii=False).encode())
print(response.read())
