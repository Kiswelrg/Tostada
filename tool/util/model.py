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

def generate_invitation_code(length=8, require_complex=True):
    """
    Generate a random invitation code with specified length.
    The code will consist of uppercase and lowercase letters and numbers.
    
    Args:
        length (int): Length of the invitation code, default is 8
        require_complex (bool): If True, ensures the code contains at least one uppercase letter,
                               one lowercase letter and one number
    
    Returns:
        str: A random invitation code
    """
    # Ensure the code is unique
    while True:
        if require_complex:
            # Ensure we have at least one of each type
            uppercase_letter = random.choice(string.ascii_uppercase)
            lowercase_letter = random.choice(string.ascii_lowercase)
            number = random.choice(string.digits)
            
            # Generate the rest of the characters
            remaining_length = length - 3
            remaining_chars = ''.join(random.choices(
                string.ascii_uppercase + string.ascii_lowercase + string.digits, 
                k=remaining_length
            ))
            
            # Shuffle all the characters together
            all_chars = uppercase_letter + lowercase_letter + number + remaining_chars
            char_list = list(all_chars)
            random.shuffle(char_list)
            code = ''.join(char_list)
        else:
            # Simple generation without complexity requirements
            chars = string.ascii_uppercase + string.digits
            code = ''.join(random.choices(chars, k=length))
        
        # Check if code already exists
        if not models.InvitationCode.objects.filter(code=code).exists():
            return code