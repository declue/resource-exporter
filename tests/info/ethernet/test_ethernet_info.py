import json

from info.ethernet import create_ethernet_info


def test_get_ethernet_info():
    info = create_ethernet_info()
    ethernet_info = info.get()
    print(json.dumps(ethernet_info, indent=1))
