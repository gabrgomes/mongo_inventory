from app import application, api
from app.users.views import users_ns

api.add_namespace(users_ns, '/api/v1/users')

from app.auth.views import auth_ns
api.add_namespace(auth_ns, '/api/v1/auth')

from app.inventory.views import inventory_ns
api.add_namespace(inventory_ns, '/api/v1/inventory')

'''
from app.task_rooms.views import taskrooms_ns
api.add_namespace(taskrooms_ns, '/api/v1/task_rooms')

from app.tasks.views import tasks_ns
api.add_namespace(tasks_ns, '/api/v1/tasks')
'''
if __name__ == '__main__':
    application.run(host='0.0.0.0')
