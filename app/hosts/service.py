from flask import abort
from bson import ObjectId
from app.hosts.models import host_request, host_record
from app.utils.db_utils import Base
from app.utils.helper import custom_marshal, update_timestamp
from app.common.constants import COLLECTIONS
base_obj = Base()

class HostsService(object):
    """
    Hosts Service
    """
    def create_host(self, id, payload):
        """
        Create a host in inventory
        :param payload:
        :return:
        """
        #payload = custom_marshal(payload, host_record, 'update')
        #payload['_id'] = ObjectId()
        count, records = base_obj.get(COLLECTIONS['INVENTORIES'], {"hosts.host_name": payload['host_name']})
        if count > 0:
            abort(400, "Host name Already Exists")
        result = base_obj.update(COLLECTIONS['INVENTORIES'], {'_id': ObjectId(id)},
                                 {"$push": {'hosts': payload}})

    def update_host(self, inventory_id, host_name, payload):
        """
        Update the host id with payload
        :param inventory_id:
        :param host_name:
        :param payload:
        :return:
        """
        payload = custom_marshal(payload, host_request, 'update', prefix="hosts.$")
        #payload = custom_marshal(payload, host_request, 'update')
        result = base_obj.update(COLLECTIONS['INVENTORIES'], {'_id': ObjectId(inventory_id), "hosts.host_name": host_name},
                                 {"$set": payload})

    def delete_host(self, inventory_id, host_name):
        """
        Delete the host with host_name
        :param inventory_id:
        :param host_name:
        :param payload:
        :return:
        """
        payload = update_timestamp(prefix="hosts.$")
 #       payload["tasks.$.meta.is_archived"], payload["tasks.$.meta.is_deleted"] = False, True
        result = base_obj.update(COLLECTIONS['INVENTORIES'], {'_id': ObjectId(inventory_id)}, 
                                 {"$pull": { "hosts": {"host_name": host_name}}})
        result = base_obj.update(COLLECTIONS['INVENTORIES'], {'_id': ObjectId(inventory_id)},
                                 {"$set": payload})
        print(result)

'''
    def update_host(self, inventory_id, host_id, payload):
        """
        Update the host id with payload
        :param inventory_id:
        :param host_id:
        :param payload:
        :return:
        """
        payload = custom_marshal(payload, host_request, 'update', prefix="hosts.$")
        result = base_obj.update(COLLECTIONS['INVENTORIES'], {'_id': ObjectId(inventory_id), "hosts._id": ObjectId(host_id)},
                                 {"$set": payload})
'''