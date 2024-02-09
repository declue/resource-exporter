from resource_exporter.info.cpu.cpu_info import CPUInfo
from resource_exporter.interface.shell import Shell


class CPUInfoMac(CPUInfo):

    def __init__(self):
        CPUInfo.__init__(self)

    def get(self):
        shell = Shell()
        result = {}
        raw = shell.exec("sysctl -a | grep machdep.cpu.brand_string:")
        result['name'] = raw.replace("\n", "").replace("machdep.cpu.brand_string: ", "").strip()
        result['detail'] = self._get_cpu_benchmark_net_data(result['name'])
        return result
