

### Require at least Python 3.6, for f-strings

# Module to make request to a web page
import requests
# Module for regex
import re
# Module for date
from datetime import date
# Module to hide password
from getpass import getpass


print()
print("This script require an XML API admin account on the Palo firewall or on the Panorama")
print()

user_admin = input("What is the admin username: ")
admin_pass = getpass()
fw_url = input("What is the ip/fqdn of the palo/pano: ")



if "." in fw_url:
    fw_url_mod = fw_url.replace(".", "-")

today = date.today()
file_name = f"api_key_{fw_url_mod}_{today}"


query_params = {
    'type' : 'keygen',
    'user' : user_admin,
    'password' : admin_pass
}

base_path = f"https://{fw_url}/api/"

# GET method. verify=False otherwise SSL error cert not trusted
response = requests.get(base_path, params=query_params, verify=False)
status_code = response.status_code
# string
content = response.text



if status_code == 200:
    print("Status code: 200. Working")
    # regex to find key
    api_key = re.search(r"key.([a-zA-Z0-9\=]*)", content).group(1)
    #print(api_key)
    
    with open(file_name, "w") as f:
        f.write(api_key)
        f.close()

elif status_code == 403:
    print(response.content)

else:
    print(f"Status code: {response.status_code}\nNot Working")

