import requests
import xmltodict
from itertools import groupby, count

OUTBOUND = 1
INBOUND = 2

MAX_PREFIX_LIST_LEN = 5


def get_local_prefixes(npa, nxx, dir=OUTBOUND):
    params = {'npa': npa, 'nxx': nxx, 'dir': dir}
    r = requests.get(
        url="http://localcallingguide.com/xmllocalprefix.php?",
        params=params
    )
    return xmltodict.parse(r.content)['root']['lca-data']['prefix']


def get_npa_data(npa):
    params = {'npa': npa}
    r = requests.get(
        url="http://localcallingguide.com/xmllistnpa.php?",
        params=params
    )
    return xmltodict.parse(r.content)['root']['npadata']


def get_ranges_from_iterable(iterable):
    def as_range(iterable):
        l = list(iterable)
        if len(l) > 1:
            return '{0}-{1}'.format(l[0], l[-1])
        else:
            return '{0}'.format(l[0])

    return [as_range(g) for _, g in groupby(iterable, key=lambda n, c=count(): n - next(c))]


def render_prefix_dict_as_str(prefix_dict):
    output = ""
    for npa, nxxs in prefix_dict.items():
        chunks = [nxxs[x:x + MAX_PREFIX_LIST_LEN] for x in range(0, len(nxxs), MAX_PREFIX_LIST_LEN)]
        output = output + "\n" + '\n'.join([str(npa)+'['+','.join(nxxs)+']xxxx' for nxxs in chunks])

    return output