import base64
import hashlib
import json
from cryptography.fernet import Fernet
from django.utils import timezone
from .ImportTool import importFunction
from ..models import ToolInChannelOfChat
from UtilGlobal.message.dump2msg import dump2msg

TOOL_LINK_EXPIRY_HOURS = 12

def generate_temp_link(method_detail, u, channel_cid, TOOL_SECRET_KEY):
    # Create a timestamp 24 hours from now
    expiry = timezone.now() + timezone.timedelta(hours=TOOL_LINK_EXPIRY_HOURS)
    
    # Create payload with all necessary data
    payload = {
        'method_detail': method_detail,
        'u': u,
        'expiry': hex(round(expiry.timestamp()))[2:]
    }
    
    # Convert to JSON and encode
    payload_str = json.dumps(payload)
    payload_bytes = payload_str.encode('utf-8')
    
    # Generate a deterministic key based on user and channel
    key_base = f"{u}:{method_detail['cid']}:{TOOL_SECRET_KEY}"
    key = base64.urlsafe_b64encode(hashlib.sha256(key_base.encode()).digest())
    
    # Encrypt the payload
    f = Fernet(key)
    encrypted_payload = f.encrypt(payload_bytes)
    
    # Create safe URL-friendly token
    token = base64.urlsafe_b64encode(encrypted_payload).decode('utf-8')
    
    # Generate the URL
    temp_link = f"/api/i/toolapi/{u}/{method_detail['cid']}/{token}/"
    return temp_link



def verify_and_process_temp_link(user_cid, tool_cid, token, TOOL_SECRET_KEY, **kwargs):
    from account.models import AUser
    try:
        # Decode the token
        encrypted_payload = base64.urlsafe_b64decode(token.encode('utf-8'))
        
        # Extract user and channel from the decrypted payload to regenerate key
        # (You'll need to implement this part based on your token structure)
        
        # Decrypt payload
        key_base = f"{user_cid}:{tool_cid}:{TOOL_SECRET_KEY}"
        key = base64.urlsafe_b64encode(hashlib.sha256(key_base.encode()).digest())
        f = Fernet(key)
        
        decrypted_payload = f.decrypt(encrypted_payload)
        payload = json.loads(decrypted_payload.decode('utf-8'))
        
        # Check expiry
        if int(payload['expiry'], 16) < timezone.now().timestamp():
            return "Link has expired"
        elif payload['u'] != user_cid:
            return "Permission denied"
        elif payload['method_detail']['cid'] != tool_cid:
            return "Invalid link"
        
        tool = ToolInChannelOfChat.objects.get(pk=tool_cid)
        channel = tool.channel
        func = importFunction(f'tool.servers.{channel.server.urlCode}.{channel.urlCode}.main', f'f_{tool.function_name}')
        # Run the original function with the stored parameters
        return func(
            {'display_name': tool.display_name,'function_name': tool.function_name, 'data': tool.data, 'cid': tool.urlCode, 'inputs': payload['method_detail']['inputs']},
            AUser.objects.get(pk=payload['u']),
            channel.urlCode,
            plaintext=True,
            generate_link_func=kwargs['generate_link_func'],
            TOOL_SECRET_KEY=TOOL_SECRET_KEY
        )
        
    except Exception as e:
        print(e)
        return f"Invalid or expired link"
