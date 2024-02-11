from resource_exporter.info.storage.storage_info import StorageInfo
from resource_exporter.interface.shell import Shell
from resource_exporter.interface.wmic_shell import WMICShell
from resource_exporter.util.file_util import convert_file_size


class StorageInfoWin(StorageInfo):

    def __init__(self):
        StorageInfo.__init__(self)

    def get(self):
        shell = WMICShell()
        raw = shell.exec("wmic diskdrive get")
        disks = []
        disk_count = len(raw['Caption'])
        for i in range(disk_count):
            disk = {
                'name': raw['Caption'][i],
                'disk_type': raw['MediaType'][i],
                'SN': raw['SerialNumber'][i],
                'size': convert_file_size(int(raw['Size'][i]), 1000)}
            disks.append(disk)

        for disk in disks:
            disk['type'] = self._get_media_type(disk['name'])
        return disks

    def _get_media_type(self, name):
        shell = Shell()
        command = "powershell -command \"&{Get-PhysicalDisk | Where-Object -Property MediaType -eq 'SSD'}\""
        raw = shell.exec(command)
        for line in raw.split("\n"):
            if name in line:
                return "SSD"
        return "HDD"
