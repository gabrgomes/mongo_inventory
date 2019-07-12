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
 