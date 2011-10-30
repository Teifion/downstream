from game.classes import user

class Service (object):
    """A service has no in-game benefit but might be a security hole"""
    
    name = "ServiceNoName"
    
    def __init__(self, app_type="cracker", **service_data):
        super(Service, self).__init__()
        
        self.service_data   = service_data
        self.version        = version
        self.service_data   = service_data
        
        self.generate_password()
    
    def vulnerabilities(self):
        raise Exception("Not implemented")
    
    def generate_password(self, **kwargs):
        self.password = user.make_password(
            brute_force = 1 + self.version,
            dictionary  = 1 + self.version,
            rainbow     = 1 + self.version,
        )

