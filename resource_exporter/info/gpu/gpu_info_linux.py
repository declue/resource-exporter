import re

from resource_exporter.interface.shell import Shell
from resource_exporter.info.gpu.gpu_info import GPUInfo


class GPUInfoLinux(GPUInfo):

    def __init__(self):
        GPUInfo.__init__(self)

    def get(self):
        shell = Shell()
        raw = shell.exec('sudo lshw -C video | grep product')
        raw = raw.replace('product:', '').strip()
        gpu_list = []
        gpu = {}
        if '[' in raw and ']' in raw:
            short_name = re.findall(r"\[(.*?)\]", raw)
            if len(short_name) > 0:
                gpu['short_name'] = short_name[0]
        gpu['name'] = raw
        gpu_list.append(gpu)
        return gpu_list
