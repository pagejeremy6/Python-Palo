
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
    'xpath' : "/config/predefined/application/entry[@name='quic']",
    'key' : api_key
}


response = requests.get(base_path, params=query_params, verify=False)
print(response.text)