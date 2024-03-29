from resource_exporter.info.cpu.cpu_info_linux import CPUInfoLinux
from resource_exporter.info.cpu.cpu_info_mac import CPUInfoMac
from resource_exporter.info.cpu.cpu_info_win import CPUInfoWin
from resource_exporter.info.system.os_type import OSType
from resource_exporter.interface.shell import Shell


def create_cpu_info():
    os_type = Shell.get_os()
    if os_type == OSType.MAC:
        return CPUInfoMac()
    if os_type == OSType.WINDOWS:
        return CPUInfoWin()
    if os_type == OSType.LINUX:
        return CPUInfoLinux()
    return None
