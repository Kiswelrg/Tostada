import requests
import socket

def check_port(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)  # Set a timeout in seconds
    try:
        result = sock.connect_ex((ip, port))
        if result == 0:
            print(f"Port {port} is open on {ip}")
            return True
        else:
            print(f"Port {port} is NOT open on {ip}")
    except socket.error as err:
        print(f"Error: {err}")
    finally:
        sock.close()
    return False


def get_url_via_proxy(url, proxy):
    try:
        proxies = {"http": proxy, "https": proxy}
        response = requests.get(url, proxies=proxies, timeout=2)
        if response.status_code == 200:
            return True
            print(f"URL: {url}")
            print(response.text)
        else:
            print(f"Failed to get URL {url} via proxy {proxy}")
    except requests.exceptions.RequestException as err:
        # print(f"Error: {err}")
        # print('timed out', proxy)
        pass
    return False

if __name__ == '__main__':
    # Example usage
    # check_port("10.20.50.136", 7890)
    # Example usage
    # get_url_via_proxy("https://4.ipw.cn", "http://10.20.20.21:7890")
    pass