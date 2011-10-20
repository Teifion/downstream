from game.classes import application

class Cracker (application.Application):
    def __init__(self, **app_data):
        super(Cracker, self).__init__(app_type="cracker", **app_data)

