from game.classes import application, job, user

base_time = 1000

crack_times = {
    "brute_force":  1,
    "dictionary":   0.5,
    "rainbow":      0.1,
}

class Cracker (application.Application):
    def __init__(self, **app_data):
        super(Cracker, self).__init__(app_type="cracker", **app_data)
    
    def _cracking_power(self, version):
        return {
            "brute_force":  version + 1,
            "dictionary":   version + 1,
            "rainbow":      version + 1,
        }
    
    def _max_progress(self, version, target_password, cracking_power):
        crack_time = 99999999
        for k, v in target_password.items():
            if k == "id": continue
            
            ratio = user.crack_ratio(v, cracking_power.get(k, 0))
            c_time = ratio * base_time * crack_times[k]
            
            # If it's zero then it's uncrackable via that method
            if c_time > 0:
                crack_time = min(crack_time, c_time)
        
        return crack_time
    
    def launch(self, network, owner, version, target_password):
        j = job.Job(
            owner           = owner,
            version         = version,
            short_name      = self.data['short_name'],
            full_name       = self.data['full_name'],
            
            max_progress    = self._max_progress(version, target_password, self._cracking_power(version))
        )
        
        def _cycle(self, cpu_points=1):
            pass
        
        def _complete():
            network.players[owner].passwords.add(target_password['id'])
        
        j._cycle    = _cycle
        j._complete = _complete
        
        return j

