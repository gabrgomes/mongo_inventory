from flask_restplus import fields, reqparse
from app import api
from app.common.models import meta


group_request = api.model('group_request', {
    'group_name': fields.String(required=True),
    'group_vars': fields.Raw(default={})
})


group_record = api.inherit('group_record', group_request, {
#    'meta': fields.Nested(meta)
})
