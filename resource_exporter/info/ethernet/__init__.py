from resource_exporter.info.ethernet.ethernet_info_linux import EthernetInfoLinux
from resource_exporter.info.ethernet.ethernet_info_mac import EthernetInfoMac
from resource_exporter.info.ethernet.ethernet_info_win import EthernetInfoWin
from resource_exporter.info.system.os_type import OSType
from resource_exporter.interface.shell import Shell


def create_ethernet_info():
    os_type = Shell.get_os()
    if os_type == OSType.MAC:
        return EthernetInfoMac()
    if os_type == OSType.WINDOWS:
        return EthernetInfoWin()
    if os_type == OSType.LINUX:
        return EthernetInfoLinux()
    return None
