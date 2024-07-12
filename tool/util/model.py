import random
import string
from .. import models
# from functools import partial

def randomId(N, opt):
    head = random.choices( ((opt & 0b001) != 0) * string.ascii_lowercase + 
                       ((opt & 0b010) != 0) * string.ascii_uppercase + 
                       ((opt & 0b100) != 0) * string.digits, k=1)[0]
    body = ''.join(random.choices( (opt&0b001 )*string.ascii_lowercase + (opt&0b010 )*string.ascii_uppercase + string.digits, k=N-1))
    return head + body


def getXCode(name,base,r):
    f = {
        'Server': (models.Server),
        'Channel': (models.Channel),
    }[name]
    
    bot = pow(10, r - 4)
    head = pow(10, r - 3)
    a = random.randint(bot, head-1) + base*head

    while f.objects.filter(urlCode = a).exists():
        a = random.randint(bot, head-1) + base*head
    return int(a)


def getServerCode():
    # return getXCode('Server',355,7)
    while True:
        random_value = random.randint(1e18, 2**63 - 1)
        if not models.Server.objects.filter(urlCode=random_value).exists():
            return random_value

def getChannelOfChatCode():
    # return getXCode('Channel',201,10)
    while True:
        random_value = random.randint(1e18, 2**63 - 1)
        if not models.ChannelOfChat.objects.filter(urlCode=random_value).exists():
            return random_value
        
def getChannelOfVoiceCode():
    # return getXCode('Channel',201,10)
    while True:
        random_value = random.randint(1e18, 2**63 - 1)
        if not models.ChannelOfVoice.objects.filter(urlCode=random_value).exists():
            return random_value
        
def getCategoryCode():
    while True:
        random_value = random.randint(1e18, 2**63 - 1)
        if not models.CategoryInServer.objects.filter(urlCode=random_value).exists():
            return random_value