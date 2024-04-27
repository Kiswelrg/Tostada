import inspect
import json
from UtilGlobal.internet.test_proxy import check_port, get_url_via_proxy


def f_availableIpPort(method_detail):
    def geturl(pp):
        return f"http://{pp['ip']}:{pp['port']}"
    r = []
    for ipport in method_detail['data']['Available_Proxies']:
        ipport['status'] = 0
        if check_port(ipport['ip'], ipport['port']):
            ipport['status'] = 1
        if get_url_via_proxy('https://4.ipw.cn', geturl(ipport)):
            ipport['status'] = 2
        r.append(ipport)
    return json.dumps(r, ensure_ascii=False)


def f_301928492109():
    return inspect.currentframe().f_code.co_name + '_function return'