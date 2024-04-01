import random,string
from . import models

def getUserCode():
    while True:
        random_value = random.randint(1e18, 2**63 - 1)
        if not models.AUser.objects.filter(urlCode=random_value).exists():
            return random_value