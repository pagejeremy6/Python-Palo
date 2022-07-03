
import requests
import re
import csv

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
    'xpath' : "/config/predefined/application-container",
    'key' : api_key
}

# API request
response = requests.get(base_path, params=query_params, verify=False)
# Response into a string
apps_container_palo = response.text

# find block of each existing container apps, put in a list
match_block = re.findall(r"\s+<entry ([\s\S]+?)\n\s\s\s\s<\/entry", apps_container_palo)


# Init empty list
app_from_container = []

# header for csv
header_csv = ['container', 'apps']


with open ('./palo_containers.csv', 'w', newline='', encoding='UTF8') as g:
    writer = csv.writer(g)
    #write header to csv
    writer.writerow(header_csv)
    # iterate list, each block is an application container 
    for element in match_block:
        # extract the name of the app container
        app_container_name = re.match(r"id=\"\d+\" name=\"([a-z0-9\.\-]+)\"", element).group(1)
        # Split each string(block) into lines and iterate
        element = element.splitlines()
        for line in element:
            # regex for base apps in container
            if "<member" in line and "ottawa" in line:
                sub_app_name_base = re.search(r"pre_ottawa_name=\"[a-z0-9\-\.]+\">([a-z0-9\-\.]+)", line).group(1)
                # add to list
                app_from_container.append(sub_app_name_base)
            # other apps in container    
            if "<member" in line and not "ottawa" in line:
                sub_app_name = re.search(r"<member>([a-z0-9\.\-]+)", line).group(1)
                #add to list
                app_from_container.append(sub_app_name)
        # Transform list to a string
        str_app_from_container = " ".join(app_from_container)
        # Build a list
        my_list = [app_container_name, str_app_from_container]
        # write list to csv
        writer.writerow(my_list)
        # re init list
        app_from_container = []
        my_list = []