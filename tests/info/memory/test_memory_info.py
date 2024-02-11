import json

from resource_exporter.info.memory import create_memory_info


def test_get_memory_info():
    obj = create_memory_info()
    print(json.dumps(obj.get(), indent=2))
