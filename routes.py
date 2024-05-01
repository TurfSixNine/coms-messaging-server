from Resources.message import Message
from Resources.group import Group
from Resources.insights import Insights
from Resources.user import User
from Resources.auth import Auth
class Routes:
    def __init__(self, api):
        self.api = api; 
        self.add_resource(Auth, "/auth/<string:route>")
        self.add_resource(Message, "/messages")
        self.add_resource(Group, "/group", "/group/<string:id>")
        self.add_resource(Insights, "/insights",'/insights/<string:type>')
        self.add_resource(User, "/users",'/users/<string:id>')
        
    def add_resource(self, resource_name, resource_url, extra_url="/"):
       self.api.add_resource(resource_name, resource_url, extra_url)