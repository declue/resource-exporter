from resource_exporter.info.gpu.gpu_info_linux import GPUInfoLinux
from resource_exporter.info.gpu.gpu_info_mac import GPUInfoMac
from resource_exporter.info.gpu.gpu_info_win import GPUInfoWin
from resource_exporter.info.system.os_type import OSType
from resource_exporter.interface.shell import Shell


def create_gpu_info():
    os_type = Shell.get_os()
    if os_type == OSType.MAC:
        return GPUInfoMac()
    if os_type == OSType.WINDOWS:
        return GPUInfoWin()
    if os_type == OSType.LINUX:
        return GPUInfoLinux()
    return None
