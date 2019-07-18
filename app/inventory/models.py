from flask_restplus import fields
from app import api

inventory_request = api.model('inventory_request', {
    'inventory_name': fields.String(required=True, description="Inventory name"),
    'sigla': fields.String(required=True, description="Sigla")
})

from app.common.models import meta
meta_inventory = api.inherit('meta_inventory', meta, {
    "is_archived": fields.Boolean(default=False)
})


from app.hosts.models import host_request
from app.groups.models import group_request, group_edit
inventory_record = api.inherit('inventory_record', inventory_request, {
    'hosts': fields.Nested(host_request),
    'groups': fields.Nested(group_request),
    'all': fields.Nested(group_edit),
#    'hosts': fields.List(fields.Raw),
#    'groups': fields.List(fields.Raw),
#    'all': fields.List(fields.Raw),
    'meta': fields.Nested(meta_inventory)
})

from flask_restplus import  reqparse
state_parser = reqparse.RequestParser()
state_parser.add_argument('State', type=str, location='args')

inventory_response = api.inherit('inventory_response', inventory_record, {
    '_id': fields.String()
})


'''
user_request = api.inherit('user base', user_base, {
    'confirm_password': fields.String(description="Confirm password")
})
'''