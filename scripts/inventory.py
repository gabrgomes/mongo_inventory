#!/usr/bin/env python
#
# MongoDB-backed dynamic inventory script for Ansible
# http://docs.ansible.com/intro_dynamic_inventory.html

import os

from argparse import ArgumentParser

import pymongo
from bson import json_util

MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_DB = "ansible"

MONGO_USER = "ansible"
MONGO_PASS = "mongogogo"

def list_groups(db, query={}):
    """Returns a dict of all the available groups to be managed

    Group documents in Mongo are in the form:
    {
        name: 'foo',
        hosts: ['bar.example.com', 'baz.example.com'],
        vars: {
            foo: 42,
            bar: 'baz'
        },
        children: ['bar']
    }
    """
    result = {}

    cursor = db.groups.find(query, {
        '_id': False,
        'name': True,
        'hosts': True,
        'vars': True,
        'children': True
     })

    for group in cursor:
        result[group['name']] = {
            'hosts': group.get('hosts', []),
            'vars': group.get('vars', {}),
            'children': group.get('children', [])
        }

    return json_util.dumps(result)

def show_host(db, hostname):
    """Returns a dict containing the variables for a specific host

    Host documents in Mongo are in the form:
    {
        hostname: 'foo.example.com',
        vars: {
            foo: 42,
            bar: 'baz'
        }
    }
    """
    cursor = db.hosts.find_one({'hostname': hostname},
                               {'_id': False, 'vars': True})
    return json_util.dumps(cursor.get('vars', {})) if cursor else '{}'

def main():
    parser = ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--list', dest='list', action='store_true')
    group.add_argument('--host', dest='host', metavar='<hostname>')
    args = parser.parse_args()

    connection = pymongo.Connection(MONGO_HOST, MONGO_PORT)
    db = connection[MONGO_DB]

    if MONGO_USER and MONGO_PASS:
        db.authenticate(MONGO_USER, MONGO_PASS)

    if args.list:
        result = list_groups(db)
    elif args.host:
        result = show_host(db, args.host)

    print(result)

if __name__ == '__main__':
    main()