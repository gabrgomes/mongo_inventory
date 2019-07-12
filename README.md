# mongo_inventory

## Ansible inventory backed by mongodb

This is a project to develop an ansible dynamic inventory plugin backed by MongoDB. The inventory can be managed using REST calls, implemented using FlaskRestPlus. The inventory plugin must receive an inventory name, get the respective inventory via API and parse it to create the in-memory inventory. Hosts and groups can be manipulated individually via API, or the hole inventory can be edited in .ini format. 

## Quick Start
```
pip3 install -r requirements.txt
docker-compose up -d
python3 wsgi.py
```
Access http://localhost:5000

## Directory structure:
```
ansible_plugin/ - ansible inventory plugins examples
app/auth/ 
app/common/ 
app/inventory 
app/users
app/utils/
inventory_files - inventory examples
scripts - script examples
```
## MongoDB document structure
See app/inventory/inventory.json

## To Do:
- api/v1/auth - OK
- api/v1/users - OK
- api/v1/inventory
	- create inventory - OK
	- get inventories
	- edit inventory
	- delete inventory
- api/v1/hosts
	- include host
	- get host
	- edit host
	- delete host
- api/v1/groups
	- include group
	- edit group
	- delete group

- ini_to_json.py
- json_to_ini.py

- ansible inventory plugin
