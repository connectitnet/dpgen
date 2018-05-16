import requests
import xmltodict

OUTBOUND = 1
INBOUND = 2

def get_local_prefixes(npa, nxx, dir=OUTBOUND):
    params = {'npa': npa, 'nxx': nxx, 'dir': dir}
    r = requests.get(
        url="http://localcallingguide.com/xmllocalprefix.php?",
        params= params
    )
    return xmltodict.parse(r.content)['root']['lca-data']['prefix']


def get_npa_data(npa):
    params = {'npa': npa}
    r = requests.get(
        url="http://localcallingguide.com/xmllistnpa.php?",
        params= params
    )
    return xmltodict.parse(r.content)['root']['npadata']