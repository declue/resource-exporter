from resource_exporter.info.storage.storage_info import StorageInfo
from resource_exporter.interface.shell import Shell


class StorageInfoMac(StorageInfo):

    def __init__(self):
        StorageInfo.__init__(self)

    def get(self):
        disk_list = []
        for i in range(0, 100):
            disk_id = f"disk{i}"
            disk_info = self._get_disk_info(disk_id)
            if disk_info is None:
                break
            if disk_info == "":
                continue
            disk_list.append(disk_info)
        return disk_list

    def _get_disk_info(self, disk_id):
        shell = Shell()
        raw = shell.exec(f"diskutil info {disk_id}")
        if len(raw) == 0:
            return None
        disk_info = {}
        for line in raw.split("\n"):
            items = line.split(":")
            if len(items) != 2:
                continue
            key = items[0].strip()
            value = items[1].strip()

            if key == "Device / Media Name":
                disk_info['name'] = value
            elif key == 'Solid State':
                disk_info['type'] = "SSD" if value == "Yes" else "HDD"
            elif key == 'Virtual':
                if value == "Yes":
                    return ""
            elif key == "Disk Size":
                disk_info['size'] = value.split("(")[0].strip()
        return disk_info
