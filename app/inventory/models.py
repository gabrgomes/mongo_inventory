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

inventory_record = api.inherit('inventory_record', inventory_request, {
#    'hosts': fields.Nested(hosts),
#    'groups': fields.Nested(groups),
#    'all': fields.Nested(all),
    'hosts': fields.List(fields.String),
    'groups': fields.List(fields.String),
    'all': fields.List(fields.String),
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