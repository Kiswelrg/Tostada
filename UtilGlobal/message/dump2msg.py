from datetime import datetime
import random
from message.models import ChatMessage
from tool.models import ChannelOfChat


def dump2msg(contents, auser, avatar, channel_cid, dt = datetime.now(), is_edited = False) -> dict:
    r = {}
    if not isinstance(contents, list):
        raise Exception('Message Contents must be a list, Generation Failed!')
    for item in contents:
        if 'type' not in item or 'content' not in item:
            raise Exception('Message Contents must have a "type" field, Generation Failed!')
    msg = ChatMessage.objects.create(
        sender=auser,
        is_private=False,
        channel=ChannelOfChat.objects.get(urlCode=channel_cid),
        _type='bot',
        contents=contents,
        # contents = '\n'.join([dumpDict(c['content']) if type(c['content']) == dict else str(c['content']) for c in contents]),
        state='1'
        # contents=dumpList(contents)
    )
    msg.full_clean()
    r['contents'] = msg.contents
    r['is_edited'] = {
        'state': msg.is_edited,
        'text': 'edited'
    }
    r['is_private'] = msg.is_private
    r['sender'] = {
        'username': auser.username,
        'avatar': auser.avatar.url
    }
    r['time_sent'] = dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    r['cid'] = str(msg.urlCode)
    r['attachments'] = []
    r['mentioned_user'] = {}
    r['tool_used'] = {'cid': channel_cid}
    return r
    

def dumpList(contents: list) -> dict:
    content_names = {
        'text': 'content',
        'Link': 'display_name',
    }
    r = []
    for content in contents:
        if isinstance(content['content'], dict):
            r.append({
                'type': content['type'],
                'display': content['display'],
                'font-size': content['font-size'] if 'font-size' in content else '',
                content_names[content['type']]: dumpDict(content)
            })
        elif isinstance(content['content'], str):
            r.append({
                'type': content['type'],
                'content': content['content'],
                'font-size': content['font-size'] if 'font-size' in content else '',
                'display': content['display']
            })
    return r


def dumpDict(msg: dict, upper_key = None) -> str:
    r = ''
    for k, v in (msg if upper_key is None else msg[upper_key]).items():
        r += f'{k}:{v}, '
    return r[:-2]