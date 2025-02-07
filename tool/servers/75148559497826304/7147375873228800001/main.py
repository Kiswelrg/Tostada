import inspect
import json
from UtilGlobal.internet.test_proxy import check_port, get_url_via_proxy
from UtilGlobal.message.dump2msg import dump2msg

def f_availableIpPort(method_detail, auser, channel_cid, **kwargs):
    def geturl(pp):
        return f"http://{pp['ip']}:{pp['port']}"
    r = [{
        'type': 'text',
        'content': '🟢 means internet access, 🟡 means service is up but no internet or is too slow, ⚫ means service is down.',
        'display': 'block',
        'font-size': '',
    }]
    for ipport in method_detail['data']['Available_Proxies']:
        ipport['status'] = '⚫'
        if check_port(ipport['ip'], ipport['port']):
            ipport['status'] = '🟡'
        if get_url_via_proxy('https://baidu.com', geturl(ipport)):
            ipport['status'] = '🟢'
        r.append({
            'type': 'text',
            'content': ipport,
            'display': 'block'
        })
    return json.dumps(
        dump2msg(
            r,
            auser,
            '/static/@me/1F955.svg',
            channel_cid,
            is_edited=True,
        ),
        ensure_ascii=False
    )


def f_301928492109():
    return inspect.currentframe().f_code.co_name + '_function return'

def f_test_func(test_arg1,test_arg2,test_arg3):
    return f_301928492109()

