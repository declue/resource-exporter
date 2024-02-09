from resource_exporter.info.cpu.cpu_info_linux import CPUInfoLinux
from resource_exporter.info.cpu.cpu_info_mac import CPUInfoMac
from resource_exporter.info.cpu.cpu_info_win import CPUInfoWin
from resource_exporter.info.system.os_type import OSType
from resource_exporter.interface.shell import Shell


def create_cpu_info():
    os_type = Shell.get_os()
    if os_type == OSType.Mac:
        return CPUInfoMac()
    elif os_type == OSType.Windows:
        return CPUInfoWin()
    elif os_type == OSType.Linux:
        return CPUInfoLinux()
