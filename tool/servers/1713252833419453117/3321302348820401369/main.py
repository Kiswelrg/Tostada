import yaml


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

if __name__ == '__main__':
    embedVmess2ClashFile('/home/wxy/tool/test_subconverter_output.yaml', "/home/wxy/Downloads/AgentNEO.yml")