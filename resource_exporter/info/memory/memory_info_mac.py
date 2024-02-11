from resource_exporter.info.memory.memory_info import MemoryInfo
from resource_exporter.interface.shell import Shell


class MemoryInfoMac(MemoryInfo):

    def __init__(self):
        MemoryInfo.__init__(self)

    def get(self):
        shell = Shell()
        memory_detail_raw = {
            "PN": self._parse_items(shell.exec('system_profiler SPMemoryDataType | grep Part')),
            "SN": self._parse_items(shell.exec('system_profiler SPMemoryDataType | grep Serial')),
            "size": self._parse_items(shell.exec('system_profiler SPMemoryDataType | grep Size')),
            "slot": self._parse_items(shell.exec('system_profiler SPMemoryDataType | grep BANK')),
            "speed": self._parse_items(shell.exec('system_profiler SPMemoryDataType | grep Speed')),
            "type": self._parse_items(shell.exec('system_profiler SPMemoryDataType | grep Type')),
            "status": self._parse_items(shell.exec('system_profiler SPMemoryDataType | grep Status')),
            "manufacturer": self._parse_items(shell.exec('system_profiler SPMemoryDataType | grep Manufacturer'))
        }

        new_slot_list = []
        for item in memory_detail_raw.get('slot', []):
            if '/' in item:
                elem = item.split('/')[0]
                new_slot_list.append(elem.split(' ')[1])
        memory_detail_raw['slot'] = new_slot_list

        total_size = 0
        for item in memory_detail_raw['size']:
            new_size = [int(s) for s in item.split() if s.isdigit()]
            if len(new_size) > 0:
                total_size += int(new_size[0])

        memory_detail = []

        def get_memory_detail_item(raw, key, index):
            try:
                return raw[key][index]
            except IndexError:
                return ""

        for i in range(len(memory_detail_raw['size'])):
            chip = {
                'PN': get_memory_detail_item(memory_detail_raw, 'PN', i),
                'SN': get_memory_detail_item(memory_detail_raw, 'SN', i),
                'size': get_memory_detail_item(memory_detail_raw, 'size', i),
                'slot': get_memory_detail_item(memory_detail_raw, 'slot', i),
                'speed': get_memory_detail_item(memory_detail_raw, 'speed', i),
                'type': get_memory_detail_item(memory_detail_raw, 'type', i),
                'status': get_memory_detail_item(memory_detail_raw, 'status', i),
                'manufacturer': get_memory_detail_item(memory_detail_raw, 'manufacturer', i)
            }
            memory_detail.append(chip)

        if total_size == 0:
            lines = shell.exec('system_profiler SPMemoryDataType | grep Memory:').split("\n")
            for line in lines:
                line = line.replace("Memory:", "").strip()
                if len(line) > 0:
                    total_size = line
                    break
            total_size_string = f"{total_size}"
            memory_detail = {
                "PN": "",
                "SN": "",
                "size": total_size_string,
                "slot": "",
                "speed": "",
                "type": self._parse_items(shell.exec('system_profiler SPMemoryDataType | grep Type'))[0],
                "status": "",
                "manufacturer": self._parse_items(shell.exec('system_profiler SPMemoryDataType | grep Manufacturer'))[0]
            }
        else:
            total_size_string = f"{total_size} GB"

        return {
            "size": total_size_string,
            "memory_detail": memory_detail
        }

    @classmethod
    def _parse_line(cls, line: str):
        raw = line.lstrip().split(": ")
        if len(raw) == 2:
            return raw[1]
        return raw[0]

    @classmethod
    def _parse_items(cls, item):
        ret_list = []
        for line in item.split('\n'):
            if line == '':
                continue
            ret_list.append(cls._parse_line(line))
        return ret_list
