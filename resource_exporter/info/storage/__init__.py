from resource_exporter.info.storage.storage_info_linux import StorageInfoLinux
from resource_exporter.info.storage.storage_info_mac import StorageInfoMac
from resource_exporter.info.storage.storage_info_win import StorageInfoWin
from resource_exporter.info.system.os_type import OSType
from resource_exporter.interface.shell import Shell


def create_storage_info():
    os_type = Shell.get_os()
    if os_type == OSType.MAC:
        return StorageInfoMac()
    if os_type == OSType.WINDOWS:
        return StorageInfoWin()
    if os_type == OSType.LINUX:
        return StorageInfoLinux()
    return None
