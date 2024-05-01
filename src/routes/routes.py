
class Routes:
    def __init__(self, api):
        self.api = api; 
        pass
    def add_resource(self, resource_name, resource_url):
       self.api.add_resource(resource_name, resource_url)