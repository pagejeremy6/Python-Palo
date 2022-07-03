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
    'xpath' : "/config/predefined/application",
    'key' : api_key
}

app_name_list = []

# API call, output to string
response = requests.get(base_path, params=query_params, verify=False)
all_apps = response.text

# List of block for each apps
match_block = re.findall(r"\s+<entry ([\s\S]+?)\n\s\s\s\s<\/entry", all_apps)

my_list = []

header = ['id',
          'name',
          'category',
          'subcategory',
          'technology',
          'risk',
          'member'
          ]

# init CSV
with open('palo_apps.csv', 'w', newline='', encoding='UTF8') as g:
    writer = csv.writer(g)
    # Write header to csv
    writer.writerow(header) 
    # Loop block of apps   
    for element in match_block:
        # each line a string
        element = element.splitlines()
        for line in element:
            # Get name and ID
            if "name=" in line and "id=" in line:
                app_id = (re.search(r"id=.(\d+)", line).group(1))
                app_name = (re.search(r"name=.([a-z0-9\-]+)", line).group(1))
            # Get category
            elif "<category>" in line:
                app_category = (re.search(r"<category>([a-z0-9\-]+)", line).group(1))
                #print(app_category)
            # Get subcategory
            elif "<subcategory>" in line:
                app_subcategory = (re.search(r"<subcategory>([a-z0-9\-]+)", line).group(1))
                #print(app_subcategory)
            # Get Technology
            elif "<technology>" in line:
                app_technology = (re.search(r"<technology>([a-z0-9\-]+)", line).group(1))
                #print(app_technology) 
            # Get risk
            elif "<risk>" in line:
                app_risk = (re.search(r"<risk>([1-5])", line).group(1))
                #print(app_risk)
            # Get default port
            elif "<member>" in line and ("tcp" in line or "udp" in line):
                app_port = (re.search(r"<member>([a-z0-9\-\/\,]+)", line).group(1))
                #print(app_port)
            # elif dependant applications
        my_list = [app_id, app_name, app_category, app_subcategory, app_technology, app_risk, app_port]
        writer.writerow(my_list)
        my_list = []
