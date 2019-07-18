from flask_restplus import Namespace, Resource, marshal
from flask_jwt_extended import jwt_required
from app import api
from app.inventory.models import inventory_request, inventory_response, state_parser
from app.inventory.service import InventoryService
from app.common.models import auth_parser
from flask_jwt_extended import get_jwt_identity

inventory_ns = Namespace('inventory', description="Inventory operations")
inventory_service = InventoryService()

@inventory_ns.expect(auth_parser)
@inventory_ns.route('')
class Inventory(Resource):
    """
    Create and Get Inventories
    """
    @jwt_required
    @inventory_ns.expect(inventory_request)
    def post(self):
        """
        Create an Inventory
        :return:
        """
        email = get_jwt_identity()
        payload = marshal(api.payload, inventory_request)
        payload['hosts'] = []
        payload['groups'] = []
        payload['all'] = []
        inventory_service.create_inventory(payload)
        return {'Message': "Inventory created successfully"}


@inventory_ns.expect(auth_parser)
@inventory_ns.route('/<string:sigla>')
class Inventory(Resource):
    """
    Inventories by sigla
    """
    @inventory_ns.expect(state_parser)
    @jwt_required
    def get(self, sigla):
        """
        Get Active, Archived and Deleted Inventories
        :param sigla: 
        :return:
        """
        email = get_jwt_identity()
        args = state_parser.parse_args()
        if self.validate_state(args['State']):
            response = inventory_service.get_inventories(sigla, state=args['State'])
            return {'Message': "Inventories rendered successfully", 'records': marshal(response, inventory_response)}
        else:
            return {"Message": "State is not in (active|archived|deleted)"}
    @staticmethod
    def validate_state(state):
        if state == 'active' or state == 'archived' or state == 'deleted':
            return True
        else:
            return False

@inventory_ns.expect(auth_parser)
@inventory_ns.route('/view/<string:id>')
class Inventory(Resource):
    """
    Get Inventory
    """
    @jwt_required
    def get(self, id):
        """
        Get Inventory
        :param id: 
        :return:
        """
        email = get_jwt_identity()
        response = inventory_service.get_inventory(id)
        #print(response[0])
        #return response[0]
        return marshal(response[0], inventory_response)

@inventory_ns.expect(auth_parser)
@inventory_ns.route('/delete/<string:id>')
class Inventory(Resource):
    @jwt_required
    def delete(self, id):
        """
        Delete an Inventory
        :param id:
        :return:
        """
        payload = api.payload
        inventory_service.delete_inventory(id)
        return {'Message': "Inventory deleted successfully"}


@inventory_ns.expect(auth_parser)
@inventory_ns.route('/archive/<string:id>')
class Inventory(Resource):
    """
    Archive an Inventory
    """
    @jwt_required
    def put(self, id):
        """
        Archive an Inventory
        :param id:
        :return:
        """
        inventory_service.archive_inventory(id)
        return {'Message': "Inventory archived successfully"}

@inventory_ns.expect(auth_parser)
@inventory_ns.route('/undo/<string:id>')
class Inventory(Resource):
    """
    Move Inventory to Active Status
    """
    @jwt_required
    def put(self, id):
        """
        Move Inventory to Active Status
        :param id:
        :return:
        """
        inventory_service.change_status(id)
        return {'Message': "Inventory status changed to Active"}
'''
@taskrooms_ns.expect(auth_parser)
@taskrooms_ns.route('/invite/<string:id>')
class RoomOperations(Resource):
    """
    Invite user to Task room
    """
    @taskrooms_ns.expect(invite_user)
    @jwt_required
    def put(self, id):
        """
        Invite user to Task room
        :param id:
        :return:
        """
        payload = marshal(api.payload, invite_user)
        taskroom_service.invite_user(id, payload['email'])
        return {'Message': "User Added to the Task Room"}

@taskrooms_ns.expect(auth_parser)
@taskrooms_ns.route('/exit/<string:id>')
class RoomOperations(Resource):
    """
    Exit from a Task room
    """
    @jwt_required
    def delete(self, id):
        """
        Exit from a Task room
        :param id:
        :return:
        """
        email = get_jwt_identity()
        taskroom_service.exit_task_room(id, email)
        return {'Message': "Exited from the Task Room"}
'''