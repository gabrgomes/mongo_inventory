from flask_restplus import fields, reqparse
from app import api
from app.common.models import meta


host_request = api.model('host_request', {
    'host_name': fields.String(required=True),
    'host_vars': fields.Raw(),
    'host_groups': fields.List(fields.String),
})

host_record = api.inherit('host_record', host_request, {
#    'meta': fields.Nested(meta)
})