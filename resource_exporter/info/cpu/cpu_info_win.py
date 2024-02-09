from resource_exporter.interface.wmic_shell import WMICShell
from resource_exporter.info.cpu.cpu_info import CPUInfo


class CPUInfoWin(CPUInfo):

    def __init__(self):
        CPUInfo.__init__(self)

    def get(self):
        shell = WMICShell()
        name = shell.exec("wmic cpu get name")['Name'][0]
        detail = self._get_cpu_benchmark_net_data(name)
        return {"name": name,
                "detail": detail}
