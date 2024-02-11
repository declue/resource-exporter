import json

from resource_exporter.info.storage.storage_info import StorageInfo
from resource_exporter.interface.shell import Shell


class StorageInfoLinux(StorageInfo):

    def __init__(self):
        StorageInfo.__init__(self)

    def get(self):
        shell = Shell()
        raw = json.loads(shell.exec(
            'lsblk -d -o NAME,FSTYPE,LABEL,MODEL,SERIAL,SIZE,STATE,OWNER,MODE,ROTA,SCHED,TYPE,VENDOR,ZONED --json'))
        disks = []
        for disk in raw['blockdevices']:
            if 'loop' not in disk['name']:
                item = {'name': disk['model'].strip()}

                i = 0
                for i in range(len(disk['size'])):
                    s = disk['size'][i]
                    if not str(s).isdigit() and s != '.':
                        break
                item['size'] = ''.join(disk['size'][:i]) + " " + ''.join(disk['size'][i:]) + "B"

                item['SN'] = disk['serial']
                if disk['rota'] == "0":
                    item['type'] = 'SSD'
                else:
                    item['type'] = 'HDD'
                disks.append(item)
        return disks
