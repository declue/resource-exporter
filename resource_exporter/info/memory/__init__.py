from resource_exporter.info.memory.memory_info_linux import MemoryInfoLinux
from resource_exporter.info.memory.memory_info_mac import MemoryInfoMac
from resource_exporter.info.memory.memory_info_win import MemoryInfoWin
from resource_exporter.info.system.os_type import OSType
from resource_exporter.interface.shell import Shell


def create_memory_info():
    os_type = Shell.get_os()
    if os_type == OSType.MAC:
        return MemoryInfoMac()
    if os_type == OSType.WINDOWS:
        return MemoryInfoWin()
    if os_type == OSType.LINUX:
        return MemoryInfoLinux()
    return None
