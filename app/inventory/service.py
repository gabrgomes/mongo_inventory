from flask import abort
from bson import ObjectId
from app.inventory.models import inventory_request, inventory_record
from app.utils.db_utils import Base
from app.utils.helper import custom_marshal, update_timestamp
from app.common.constants import COLLECTIONS
base_obj = Base()

class InventoryService(object):
    """
    Room Related Services
    """
    def create_inventory(self, payload):
        """
        Function to create inventory in mongo
        :param payload:
        :return:
        """
        count, records = base_obj.get(COLLECTIONS['INVENTORIES'], { "$and": [ {"inventory_name": payload['inventory_name']}, {"sigla": payload['sigla']} ]})
        if count > 0:
            abort(400, "Inventory Already Exists")
        payload = custom_marshal(payload, inventory_record, 'create')
        _id = base_obj.insert(COLLECTIONS['INVENTORIES'], payload)
        print(_id, type(_id))
 
    def get_inventories(self, sigla, state):
        """
        Get Inventories for a particular system
        :param sigla:
        :return:
        """
        if state == 'active':
            query = {"sigla": sigla, "meta.is_deleted": False, "meta.is_archived": False}
        elif state == 'archived':
            query = {"sigla": sigla, "meta.is_archived": True}
        elif state == 'deleted':
            query = {"sigla": sigla, "meta.is_deleted": True}
        count, records = base_obj.get(COLLECTIONS['INVENTORIES'], query)
        return records

    def get_inventory(self, id):
        """
        Get Inventory with id
        :param id:
        :return:
        """
        count, records = base_obj.get(COLLECTIONS['INVENTORIES'], {"_id": ObjectId(id)})
        if count != 1:
            abort(400, "Inventory not found")
        return records

    def delete_inventory(self, id):
        """
        Delete inventory
        :return:
        """
        count, records = base_obj.get(COLLECTIONS['INVENTORIES'], {"_id": ObjectId(id)})
        if count != 1:
            abort(400, "inventory Already Deleted")
        payload = update_timestamp()
        payload["meta.is_archived"], payload["meta.is_deleted"] = False, True
        base_obj.update(COLLECTIONS['INVENTORIES'], {"_id": ObjectId(id)}, 
                        {"$set": payload})

    def archive_inventory(self, id):
        """
        Archive inventory
        :return:
        """
        payload = update_timestamp()
        payload["meta.is_archived"], payload["meta.is_deleted"] = True, False
        base_obj.update(COLLECTIONS['INVENTORIES'], {"_id": ObjectId(id)},
                        {"$set": payload})

    def change_status(self, id):
        """
        Change Status to Active
        :return:
        """
        payload = update_timestamp()
        payload["meta.is_archived"], payload["meta.is_deleted"] = False, False
        base_obj.update(COLLECTIONS['INVENTORIES'], {"_id": ObjectId(id)},
                        {"$set": payload})