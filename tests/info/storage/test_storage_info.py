import json

from resource_exporter.info.storage import create_storage_info


def test_get_disk_info():
    obj = create_storage_info()
    print(json.dumps(obj.get(), indent=2))
