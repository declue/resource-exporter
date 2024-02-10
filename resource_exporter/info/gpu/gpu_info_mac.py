import json

from resource_exporter.info.gpu.gpu_info import GPUInfo
from resource_exporter.interface.shell import Shell


class GPUInfoMac(GPUInfo):

    def __init__(self):
        GPUInfo.__init__(self)

    def get(self):
        shell = Shell()
        raw = json.loads(shell.exec("system_profiler SPDisplaysDataType -json"))

        gpu_list = []
        gpu_count = len(raw['SPDisplaysDataType'])
        for i in range(gpu_count):
            gpu = {}
            gpu_data = raw['SPDisplaysDataType'][i]
            gpu['name'] = gpu_data.get('sppci_model', "")
            if 'spdisplays_vram' not in gpu_data:
                continue
            gpu['memory'] = gpu_data.get('spdisplays_vram', "")
            gpu['manufacturer'] = gpu_data.get('spdisplays_vendor', "")
            gpu['driver'] = gpu_data.get('spdisplays_rom-revision', "")
            gpu['status'] = "OK"
            gpu_list.append(gpu)
        return gpu_list
