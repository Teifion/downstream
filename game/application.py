from engine.render import controls

class Application (controls.Panel):
    def __init__(self, position, size, priority=0):
        super(Application, self).__init__(position, size, priority)
    
    def logic_cycle(self):
        pass

