import yaml

# Load the existing YAML file
with open("neo.yml", "r", encoding="utf-8") as file:
    data = yaml.safe_load(file)

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

# Get the first proxy group name
first_proxy_group_name = data["proxy-groups"][0]["name"]

# Modify custom rules to match the first proxy group name if necessary
modified_rules = []
for rule in custom_rules:
    parts = rule.rsplit(",", 1)  # Split by the last comma
    if len(parts) == 2 and parts[1] == "PROXY":
        modified_rules.append(f"{parts[0]},{first_proxy_group_name}")
    else:
        modified_rules.append(rule)

# Insert the new rules at the start of the existing rules
data["rules"] = modified_rules + data["rules"]

# Save the modified YAML back
with open("config_modified.yaml", "w", encoding="utf-8") as file:
    yaml.safe_dump(data, file, allow_unicode=True, default_flow_style=False)

print("Config modified and saved as config_modified.yaml")
