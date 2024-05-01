from datetime import datetime
import random

def dump2msg(contents, nickname, avatar, dt = datetime.now(), isEdited = False, isGroupHead = False) -> dict:
    r = {}
    if isinstance(contents, dict):
        contents = [contents]
    if isinstance(contents, list):
        r['contents'] = dumpList(contents)
    r['isEdited'] = {
        'state': isEdited,
        'text': 'edited'
    }
    r['nickname'] = nickname
    r['date_sent'] = dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    r['id'] = random.randint(10, 100)
    r['isGroupHead'] = isGroupHead
    r['avatar_src'] = avatar
    return r
    

def dumpList(contents: list) -> dict:
    content_names = {
        'Text': 'content',
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


def dumpDict(msg: dict) -> str:
    r = ''
    for k, v in msg['content'].items():
        r += f'{k}:{v}, '
    return r[:-2]