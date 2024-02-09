from resource_exporter.info.cpu.cpu_info import CPUInfo
from resource_exporter.interface.shell import Shell


class CPUInfoLinux(CPUInfo):

    def __init__(self):
        CPUInfo.__init__(self)

    def get(self):
        result = dict()
        shell = Shell()
        raw = shell.exec("cat /proc/cpuinfo | grep 'name' | uniq")
        raw = raw.split(':')[1].replace('\n', '')
        result['name'] = raw
        result['detail'] = self._get_cpu_benchmark_net_data(result['name'])
        return result
