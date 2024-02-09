import json

from resource_exporter.info.cpu import create_cpu_info


def test_get_cpu():
    obj = create_cpu_info()
    print(json.dumps(obj.get(), indent=2))
