from flask_restplus import Namespace, Resource, marshal
from flask_jwt_extended import jwt_required
from app import api
from app.groups.models import group_request
from app.groups.service import GroupsService
from app.common.models import auth_parser

groups_ns = Namespace('groups', description="Groups operations")
groups_service = GroupsService()

@groups_ns.expect(auth_parser)
@groups_ns.route('/<string:id>')
class Groups(Resource):
    """
    Groups Operations - Pass inventory id as input
    """
    @jwt_required
    @groups_ns.expect(group_request)
    def post(self, id):
        """
        Add a Group to the Inventory
        :return:
        """
        payload = marshal(api.payload, group_request)
        groups_service.create_group(id, payload)
        return {'status': "Group created successfully"}

@groups_ns.expect(auth_parser)
@groups_ns.route('/<string:inventory_id>/<string:group_name>')
class Groups(Resource):
    """
    Group Operations PUT - Pass inventory id and Group name as input
    """
    @jwt_required
    @groups_ns.expect(group_request)
    def put(self, inventory_id, group_name):
        """
        Edit a Group
        :param id:
        :return:
        """
        payload = marshal(api.payload, group_request)
        #group_name =  payload['group_name']
        groups_service.update_group(inventory_id, group_name, payload)
        return {'status': "Group updated successfully"}

@groups_ns.expect(auth_parser)
@groups_ns.route('/delete/<string:inventory_id>/<string:group_name>')
class Groups(Resource):
    """
    Groups Operations Delete - Pass task inventory_id and group_name as input
    """
    @jwt_required
    def delete(self, inventory_id, group_name):
        """
        Delete a Group
        :param id:
        :return:
        """
        groups_service.delete_group(inventory_id, group_name)
        return {'status': "Group deleted successfully"}
