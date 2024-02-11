import json

from resource_exporter.info.mainboard import create_mainboard_info


def test_get_mainboard_info():
    obj = create_mainboard_info()
    print(json.dumps(obj.get(), indent=2))
