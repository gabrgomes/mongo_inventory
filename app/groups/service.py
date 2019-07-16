from flask import abort
from bson import ObjectId
from app.groups.models import group_request, group_record
from app.utils.db_utils import Base
from app.utils.helper import custom_marshal, update_timestamp
from app.common.constants import COLLECTIONS
base_obj = Base()

class GroupsService(object):
    """
    Groups Service
    """
    def create_group(self, id, payload):
        """
        Create a group in inventory
        :param payload:
        :return:
        """
        payload = custom_marshal(payload, group_record, 'create')
        #payload['_id'] = ObjectId()
        count, records = base_obj.get(COLLECTIONS['INVENTORIES'], {"groups.group_name": payload['group_name']})
        if count > 0:
            abort(400, "Group name Already Exists")
        result = base_obj.update(COLLECTIONS['INVENTORIES'], {'_id': ObjectId(id)},
                                 {"$push": {'groups': payload}})

    def update_group(self, inventory_id, group_name, payload):
        """
        Update the group id with payload
        :param inventory_id:
        :param group_name:
        :param payload:
        :return:
        """
        payload = custom_marshal(payload, group_request, 'update', prefix="groups.$")
        result = base_obj.update(COLLECTIONS['INVENTORIES'], {'_id': ObjectId(inventory_id), "groups.group_name": group_name},
                                 {"$set": payload})

    def delete_group(self, inventory_id, group_name):
        """
        Delete the group with group_name
        :param inventory_id:
        :param group_name:
        :param payload:
        :return:
        """
        payload = update_timestamp(prefix="groups.$")
 #       payload["tasks.$.meta.is_archived"], payload["tasks.$.meta.is_deleted"] = False, True
        result = base_obj.update(COLLECTIONS['INVENTORIES'], {'_id': ObjectId(inventory_id)}, 
                                 {"$pull": { "groups": {"group_name": group_name}}})
        result = base_obj.update(COLLECTIONS['INVENTORIES'], {'_id': ObjectId(inventory_id)}, 
                                 {"$pull": { "hosts.$[].host_groups": group_name }})
        result = base_obj.update(COLLECTIONS['INVENTORIES'], {'_id': ObjectId(inventory_id)},
                                 {"$set": payload})
        print(result)

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