import re
import requests

# Import API key
with open("../../api_key_palo") as f:
    api_key = f.read()
    f.close()

# Import base Path
with open("../../base_path") as f:
    base_path = f.read()
    f.close()

# Parameter to export configuration
query_params = {
    'type' : 'config',
    'action' : 'get',
    'xpath' : "/config/predefined/application",
    'key' : api_key
}



response = requests.get(base_path, params=query_params, verify=False)
all_apps = response.text

match_block = re.findall(r"\s+<entry ([\s\S]+?)\n\s\s\s\s<\/entry", all_apps)

new_list = []

for element in match_block:
    if "<risk>1" in element or "<risk>2" in element:
        #new_list.append(element)
        if "<member>[Web App]</member>" in element:
            #new_list.append(element)
            if "<technology>browser-based</technology>" in element:
                #new_list.append(element)
                if ("<subcategory>proxy</subcategory>" not in element and 
                    "<subcategory>remote-access</subcategory>" not in element):
                    new_list.append(element)

app_risk = []

for element in new_list:
    element = element.splitlines()
    for line in element:
        if "name=" in line and "id=" in line:
            app_name = (re.search(r"name=.([a-z0-9\-\.]+)", line).group(1))
            app_risk.append(app_name)

print(app_risk)