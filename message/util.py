import random
from . import models

def getDirectMessageCode():
    while True:
        random_value = random.randint(1e18, 2**63 - 1)
        if not models.DirectMessage.objects.filter(urlCode=random_value).exists():
            return random_value
        
def getGroupMessageCode():
    while True:
        random_value = random.randint(1e18, 2**63 - 1)
        if not models.GroupMessage.objects.filter(urlCode=random_value).exists():
            return random_value