from flask import abort
from bson import ObjectId
from app.groups.models import group_request
from app.utils.db_utils import Base
from app.utils.helper import custom_marshal, update_timestamp, update_meta
from app.common.constants import COLLECTIONS
base_obj = Base()

class GroupsService(object):
    """
    Groups Service
    """
    def create_group(self, inventory_id, payload):
        """
        Create a group in inventory
        :param payload:
        :return:
        """
        #payload = custom_marshal(payload, group_record, 'create')
        #payload['_id'] = ObjectId()
        count, records = base_obj.get(COLLECTIONS['INVENTORIES'], {"groups.group_name": payload['group_name']})
        if count > 0:
            abort(400, "Group name Already Exists")
        result = base_obj.update(COLLECTIONS['INVENTORIES'], {'_id': ObjectId(inventory_id)},
                                 {"$push": {'groups': payload}})
        result_meta = base_obj.update(COLLECTIONS['INVENTORIES'], {'_id': ObjectId(inventory_id)},
                                 {"$set": update_meta() })

    def update_group(self, inventory_id, group_name, payload):
        """
        Update the group id with payload
        :param inventory_id:
        :param group_name:
        :param payload:
        :return:
        """
#        payload = custom_marshal(payload, group_request, 'update', prefix="groups.$")
        result = base_obj.update(COLLECTIONS['INVENTORIES'], {'_id': ObjectId(inventory_id), "groups.group_name": group_name},
                                 {"$set": {'groups.$': payload}})
        result_meta = base_obj.update(COLLECTIONS['INVENTORIES'], {'_id': ObjectId(inventory_id)},
                                 {"$set": update_meta() })

    def delete_group(self, inventory_id, group_name):
        """
        Delete the group with group_name
        :param inventory_id:
        :param group_name:
        :param payload:
        :return:
        """
        result = base_obj.update(COLLECTIONS['INVENTORIES'], {'_id': ObjectId(inventory_id)}, 
                                 {"$pull": { "groups": {"group_name": group_name}}})
        result = base_obj.update(COLLECTIONS['INVENTORIES'], {'_id': ObjectId(inventory_id)}, 
                                 {"$pull": { "hosts.$[].host_groups": group_name }})
        result_meta = base_obj.update(COLLECTIONS['INVENTORIES'], {'_id': ObjectId(inventory_id)},
                                 {"$set": update_meta() })
 
'''
    def update_group(self, inventory_id, group_id, payload):
        """
        Update the group id with payload
        :param inventory_id:
        :param group_id:
        :param payload:
        :return:
        """
        payload = custom_marshal(payload, group_request, 'update', prefix="groups.$")
        result = base_obj.update(COLLECTIONS['INVENTORIES'], {'_id': ObjectId(inventory_id), "groups._id": ObjectId(group_id)},
                                 {"$set": payload})
'''