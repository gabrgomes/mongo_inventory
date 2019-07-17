from flask_restplus import Namespace, Resource, marshal
from flask_jwt_extended import jwt_required
from app import api
from app.hosts.models import host_request, host_edit
from app.hosts.service import HostsService
from app.common.models import auth_parser

hosts_ns = Namespace('hosts', description="Hosts operations")
hosts_service = HostsService()

@hosts_ns.expect(auth_parser)
@hosts_ns.route('/<string:inventory_id>')
class Hosts(Resource):
    """
    Hosts Operations - Pass inventory id as input
    """
    @jwt_required
    @hosts_ns.expect(host_request)
    def post(self, inventory_id):
        """
        Add a Host to the Inventory
        :return:
        """
        payload = marshal(api.payload, host_request)
        hosts_service.create_host(inventory_id, payload)
        return {'status': "Host created successfully"}

@hosts_ns.expect(auth_parser)
@hosts_ns.route('/<string:inventory_id>/<string:host_name>')
class Tasks(Resource):
    """
    Host Operations PUT - Pass inventory id and host name as input
    """
    @jwt_required
    @hosts_ns.expect(host_edit)
    def put(self, inventory_id, host_name):
        """
        Edit a host
        :param id:
        :return:
        """
        payload = marshal(api.payload, host_request)
        payload['host_name'] = host_name
        hosts_service.update_host(inventory_id, host_name, payload)
        return {'status': "Host updated successfully"}

@hosts_ns.expect(auth_parser)
@hosts_ns.route('/delete/<string:inventory_id>/<string:host_name>')
class Tasks(Resource):
    """
    Tasks Operations Delete - Pass task inventory_id and host_name as input
    """
    @jwt_required
    def delete(self, inventory_id, host_name):
        """
        Delete a Host
        :param id:
        :return:
        """
        hosts_service.delete_host(inventory_id, host_name)
        return {'status': "Host deleted successfully"}

'''
@hosts_ns.expect(auth_parser)
@hosts_ns.route('/<string:inventory_id>/<string:host_id>')
class Tasks(Resource):
    """
    Host Operations PUT - Pass inventory id and host id as input
    """
    @jwt_required
    @hosts_ns.expect(host_request)
    def put(self, inventory_id, host_id):
        """
        Edit a host
        :param id:
        :return:
        """
        payload = marshal(api.payload, host_request)
        hosts_service.update_host(inventory_id, host_id, payload)
        return {'status': "Host updated successfully"}
'''