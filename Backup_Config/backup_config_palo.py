
import requests
from datetime import date

# Import API key
with open("../api_key_palo") as f:
    api_key = f.read()
    f.close()

# Import base Path
with open("../base_path") as f:
    base_path = f.read()
    f.close()

# Parameter to export configuration
query_params = {
    'type' : 'export',
    'category' : 'configuration',
    'key' : api_key
}


response = requests.get(base_path, params=query_params, verify=False)

today = date.today()
file_name = f"running_config_{today}.xml"

with open(file_name, "wb") as g:
    g.write(response.content)
    g.close()