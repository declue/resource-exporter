import json

from resource_exporter.info.gpu import create_gpu_info


def test_get_gpu_info():
    obj = create_gpu_info()
    print(json.dumps(obj.get(), indent=2))
