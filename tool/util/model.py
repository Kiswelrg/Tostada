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
        'ToolServer': (models.ToolServer),
        'Tool': (models.Tool),
    }[name]
    
    print(f)
    bot = pow(10, r - 4)
    head = pow(10, r - 3) 
    a = random.randint(bot, head-1) + base*head

    while f.objects.filter(urlCode = a).exists():
        a = random.randint(bot, head-1) + base*head
    return int(a)


def getToolServerCode():
    return getXCode('ToolServer',355,7)

def getToolCode():
    return getXCode('Tool',201,10)