from resource_exporter.info.mainboard.mainboard_info_linux import MainBoardInfoLinux
from resource_exporter.info.mainboard.mainboard_info_mac import MainBoardInfoMac
from resource_exporter.info.mainboard.mainboard_info_win import MainBoardInfoWin
from resource_exporter.info.system.os_type import OSType
from resource_exporter.interface.shell import Shell


def create_mainboard_info():
    os_type = Shell.get_os()
    if os_type == OSType.MAC:
        return MainBoardInfoMac()
    if os_type == OSType.WINDOWS:
        return MainBoardInfoWin()
    if os_type == OSType.LINUX:
        return MainBoardInfoLinux()
    return None
