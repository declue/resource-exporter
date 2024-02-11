from resource_exporter.info.memory.memory_info import MemoryInfo
from resource_exporter.interface.shell import Shell
from resource_exporter.util.file_util import convert_file_size


class MemoryInfoLinux(MemoryInfo):

    def __init__(self):
        MemoryInfo.__init__(self)

    @staticmethod
    def _get_size(memory_detail):
        size = 0
        for item in memory_detail:
            if item['size'] == 'No Module Installed':
                item['size'] = ''
                continue
            size += float(item['size'].replace('GB', ''))
        size = size * 1024 * 1024 * 1024
        return convert_file_size(size, 1024)

    def get(self):
        result = {}
        shell = Shell()
        raw = shell.exec('sudo dmidecode -t memory')
        lines = raw.split('\n')
        chip_list = []

        begin = False
        chip = None
        for line in lines:
            if line == 'Memory Device':
                begin = True
                chip = {}
                continue
            if line == '':
                begin = False
                if chip is not None:
                    chip_list.append(chip)
                    chip = None
                continue

            if begin is True and chip is not None:
                items = line.split(':')
                key = items[0].strip()
                value = items[1].strip()

                if key == 'Size':
                    chip['size'] = value.strip()
                    if "MB" in chip.get('size', ""):
                        val = chip['size'].replace('MB', '').strip()
                        val = int(val) / 1024
                        chip['size'] = f"{int(val)} GB"

                if key == 'Bank Locator':
                    chip['slot'] = value.strip()
                if key == 'Part Number':
                    chip['PN'] = value
                if key == 'Serial Number':
                    chip['SN'] = value
                if key == 'Speed':
                    chip['speed'] = value
        result['memory_detail'] = chip_list

        result['size'] = self._get_size(result['memory_detail'])
        val = result.get('size', "")
        if val != '0':
            result['size'] = f"{int(float(val.split(' ')[0]))} {val.split(' ')[1]}"
        return result
