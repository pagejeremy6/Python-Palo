
## Convert ASA objects to Palo SET commands

### Format of a set command for an object on a palo
### set vsys vsys1 address $obj_name ip-netmask x.x.x/yy

import re

# Read file as a string
with open("config_ASA.txt") as f:
    output = f.read()

# String split into a list, each line element of the list
asa_config = output.splitlines()

# Regex to match 2 uses cases subnet and host, groupdict does not work with findall, so no really uses to name var in regex. Will give back a list
match_subnet = (re.findall(r"object network (\S+)\n\s+subnet (\S+) (\S+)", output))
match_host = (re.findall(r"object network (\S+)\n\s+host (\S+)", output))


# Create a file to write in
with open ("set_cmd.txt", "w") as g: 
    for lines in match_subnet:
        var_obj_name, ip_addr, mask = lines
        # function to convert mask to cidr
        cidr = str(sum(bin(int(x)).count('1') for x in mask.split('.')))
        # Create SET commands strings
        set_cmd = f'set vsys vsys1 address {var_obj_name} ip-netmask {ip_addr}/{cidr}\n'
        g.write(set_cmd)
    
    for lines in match_host:
        var_obj_name, ip_addr = lines
        set_cmd = f'set vsys vsys1 address {var_obj_name} ip-netmask {ip_addr}/32\n'
        g.write(set_cmd)
    g.close()
