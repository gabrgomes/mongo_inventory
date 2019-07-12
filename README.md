# mongo_inventory

Ansible inventory backed by mongodb

Estrutura: 
ansible_plugin/ - ansible inventory plugins examples
app/auth/ 
app/common/ 
app/inventory 
app/users
app/utils/
inventory_files - inventory examples
scripts - script examples

ToDo:
- api/v1/auth - OK
- api/v1/users - OK
- api/v1/inventory
	- create inventory - OK
	- get inventories
	- edit inventory
	- delete inventory
- api/v1/hosts
	- include host
	- edit host
	- delete host
- api/v1/groups
	- include group
	- edit group
	- delete group

- ini_to_json.py
- json_to_ini.py

- ansible inventory plugin
