from __future__ import division

import random

class User (object):
    """Defines a user profile on a network node."""
    def __init__(self, name, password):
        super(User, self).__init__()
        
        self.name       = name
        self.password   = make_password(**password)

def make_password(brute_force=1, dictionary=1, rainbow=1):
    return {
        "id":           random.random(),
        "brute_force":  brute_force,
        "dictionary":   dictionary,
        "rainbow":      rainbow,
    }

def crack_ratio(password_strength, crack_strength):
    # If it's 0 then we make it just a tiny bit more and it'll have a silly crack time
    crack_strength = max(0.00000001, crack_strength)
    
    ratio = password_strength / crack_strength
    
    return ratio
        
