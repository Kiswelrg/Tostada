import yaml
import subprocess
from UtilGlobal.message.dump2msg import dump2msg
from tool.util.toolAPI import TOOL_LINK_EXPIRY_HOURS

def embedVmess2Clash(vmess_dict, clash_dict):
    # 调用函数加载配置文件
    config_data = clash_dict
    vmess_data = vmess_dict
    
    # Modify configuration data
    custom_rules = [
        'DOMAIN-SUFFIX,claude.ai,FUN',
        'DOMAIN-SUFFIX,openai.com,FUN',
        'DOMAIN-SUFFIX,bing.com,FUN',
        'DOMAIN-SUFFIX,bingapis.com,FUN',
        'DOMAIN-SUFFIX,anthropic.com,FUN',
        'DOMAIN-SUFFIX,chatgpt.com,FUN',
        'DOMAIN-SUFFIX,dify.ai,FUN',
        'DOMAIN-SUFFIX,restapi.amap.com,DIRECT',
        'IP-CIDR,192.168.0.0/16,DIRECT',
        'IP-CIDR,172.28.89.205/16,DIRECT',
        'DOMAIN-SUFFIX,pcpartpicker.com,DIRECT',
        'DOMAIN-SUFFIX,anaconda.com,FUN',
    ]
    
    config_data['proxies'].insert(0, vmess_data['proxies'][0])
    
    config_data['proxy-groups'].append({
        'name': 'FUN',
        'type': 'select',
        'proxies': [vmess_data['proxies'][0]['name'], 'DIRECT']
    })
    
    config_data['rules'] = custom_rules + config_data['rules']('/home/wxy/Downloads/AgentNEO.yml')['rules']
    return config_data

def embedVmess2ClashString(vmess_str, clash_str):
    # 调用函数加载配置文件
    config_data = yaml.safe_load(clash_str)
    vmess_data = yaml.safe_load(vmess_str)

    return embedVmess2Clash(vmess_data, config_data)

def embedVmess2ClashFile(vmess_path, clash_path):
    # Read YAML configuration file
    def load_yaml_config(file_path):
        with open(file_path, 'r') as file:
            config = yaml.safe_load(file)
        return config
    
    # Save YAML configuration to file
    def save_yaml_config(file_path, config_data):
        with open(file_path, 'w') as file:
            yaml.dump(config_data, file, default_flow_style=False)
    
    # 调用函数加载配置文件
    config_data = load_yaml_config(clash_path)
    vmess_data = load_yaml_config(vmess_path)

    return embedVmess2Clash(vmess_data, config_data)

def vmess2clash(subconverter_executable):
    # Run an executable without parameters
    # subprocess.run(["/home/wxy/tool/subconverter/subconverter"])

    # Run an executable with parameters
    r = subprocess.run([subconverter_executable, "-g"], capture_output=True, text=True)
    'SUCCESS' in r.stderr.rsplit('\n', 4)[-4]



def f_subWithCustomRules(method_detail, u, channel_cid, plaintext=False, **kwargs):
    import yaml,json
    import requests
    from urllib.parse import urlparse
    from django.http import HttpResponse, JsonResponse

    def fetch_yaml(yaml_url):
        if not yaml_url:
            return JsonResponse({"error": "Missing 'url' parameter"}, status=400)

        # Validate the URL format
        parsed_url = urlparse(yaml_url)
        if parsed_url.scheme not in ("http", "https"):
            return JsonResponse({"error": "Invalid URL scheme. Only HTTP and HTTPS are allowed."}, status=400)

        # Avoid SSRF by blocking private/internal IPs
        if parsed_url.hostname in ["localhost", "127.0.0.1", "::1"]:
            return JsonResponse({"error": "Access to local addresses is not allowed."}, status=403)

        try:
            # Fetch the YAML file with a timeout and size limit
            response = requests.get(yaml_url, timeout=5, stream=True)

            # Check response status
            if response.status_code != 200:
                return JsonResponse({"error": "Failed to fetch the YAML file"}, status=response.status_code)

            # Limit file size (e.g., max 1MB)
            content_length = response.headers.get("Content-Length")
            if content_length and int(content_length) > 1024 * 1024:
                return JsonResponse({"error": "YAML file too large (max 1MB allowed)."}, status=400)

            # Read and parse YAML safely
            yaml_data = yaml.safe_load(response.text)

            if not yaml_data or not isinstance(yaml_data, dict):
                return JsonResponse({"error": "Invalid YAML format"}, status=400)
            
            return yaml_data
        except Exception as _:
            return JsonResponse({"error": "Failed to fetch the YAML file"}, status=400)


    # Load the existing YAML file (assuming it's in the project directory)
    # with open("config.yaml", "r", encoding="utf-8") as file:
    #     data = yaml.safe_load(file)
    yaml_url = method_detail['inputs']['url'][0].strip()
    if not yaml_url.startswith(('http://', 'https://')):
        yaml_url = 'http://' + yaml_url
    data = fetch_yaml(yaml_url)

    # Define custom rules
    custom_rules = [
        "DOMAIN-SUFFIX,glitch.me,PROXY",
        "DOMAIN-SUFFIX,glitch.com,PROXY",
        "DOMAIN-SUFFIX,claude.ai,PROXY",
        "DOMAIN-SUFFIX,openai.com,PROXY",
        "DOMAIN-SUFFIX,bing.com,PROXY",
        "DOMAIN-SUFFIX,bingapis.com,PROXY",
        "DOMAIN-SUFFIX,anthropic.com,PROXY",
        "DOMAIN-SUFFIX,chatgpt.com,PROXY",
        "DOMAIN-SUFFIX,dify.ai,PROXY",
        "DOMAIN-SUFFIX,restapi.amap.com,DIRECT",
        "IP-CIDR,192.168.0.0/16,DIRECT",
        "IP-CIDR,172.28.89.205/16,DIRECT",
        "DOMAIN-SUFFIX,pcpartpicker.com,DIRECT",
        "DOMAIN-SUFFIX,anaconda.com,PROXY",
        "DOMAIN-SUFFIX,discord.com,PROXY",
        "DOMAIN-SUFFIX,glitch.com,PROXY",
        "DOMAIN-SUFFIX,glitch.me,PROXY",
        "DOMAIN-SUFFIX,anthropic.com,PROXY",
        "DOMAIN-SUFFIX,claude.ai,PROXY",
        "DOMAIN-SUFFIX,reddit.com,PROXY",
        "DOMAIN-SUFFIX,twitter.com,PROXY",
        "DOMAIN-SUFFIX,usefathom.com,PROXY",
        "DOMAIN-SUFFIX,facebook.net,PROXY",
        "DOMAIN-SUFFIX,g.doubleclick.net,PROXY",
        "DOMAIN-SUFFIX,licdn.com,PROXY",
        "DOMAIN-SUFFIX,ads-twitter.com,PROXY",
        "DOMAIN-SUFFIX,t.co,PROXY",
        "DOMAIN-SUFFIX,facebook.com,PROXY",
        "DOMAIN-SUFFIX,googletagmanager.com,PROXY",
        "DOMAIN-SUFFIX,redditstatic.com,PROXY",
    ]

    try:
        # Get the first proxy group name
        first_proxy_group_name = data["proxy-groups"][0]["name"]

        # Modify custom rules
        modified_rules = []
        for rule in custom_rules:
            parts = rule.rsplit(",", 1)  # Split by the last comma
            if len(parts) == 2 and parts[1] == "PROXY":
                modified_rules.append(f"{parts[0]},{first_proxy_group_name}")
            else:
                modified_rules.append(rule)

        # Insert modified rules at the beginning of the existing rules
        data["rules"] = modified_rules + data["rules"]


        if plaintext:
            # Convert YAML data to a string
            yaml_content = yaml.safe_dump(data, allow_unicode=True, default_flow_style=False)
            res = yaml_content
        else:
            generate_link_func = kwargs['generate_link_func']
            res = [{
                    'type': 'text',
                    'content': f"This is your link to the {method_detail['display_name']} result (expires in {TOOL_LINK_EXPIRY_HOURS} hour(s)): ",
                    'display': 'block'
                }, {
                    'type': 'link',
                    'content': generate_link_func(method_detail, u.urlCode, channel_cid, kwargs['TOOL_SECRET_KEY']),
                    'display': 'inline'
                }
            ]
        

    except Exception as e:
        res = [{
                'type': 'text',
                'content': f"Failed to process the clash config in {method_detail['inputs']['url'][0].strip()}. Make sure your url is correct and the file is valid.",
                'display': 'block'
            }
        ]
    
    if plaintext:
        return res
    return json.dumps(
        dump2msg(
            res,
            u,
            '/static/@me/1F955.svg',
            channel_cid,
            is_edited=True,
        ), 
        ensure_ascii=False
    )
    # Return YAML content as an HTTP response
    return HttpResponse(yaml_content, content_type="text/yaml")


if __name__ == '__main__':
    embedVmess2ClashFile('/home/wxy/tool/test_subconverter_output.yaml', "/home/wxy/Downloads/AgentNEO.yml")