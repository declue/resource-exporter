from resource_exporter.info.memory.memory_info import MemoryInfo
from resource_exporter.interface.wmic_shell import WMICShell
from resource_exporter.util.file_util import convert_file_size


class MemoryInfoWin(MemoryInfo):

    def __init__(self):
        MemoryInfo.__init__(self)

    def get(self):
        shell = WMICShell()
        raw = shell.exec("wmic memorychip get")
        chip_list = []
        chip_count = len(raw['Capacity'])

        total_size = 0
        for i in range(chip_count):
            chip = {'size': convert_file_size(int(raw['Capacity'][i]), 1024)}
            val = convert_file_size(int(raw['Capacity'][i]), 1024)
            chip['size'] = f"{int(float(val.split(' ')[0]))} {val.split(' ')[1]}"

            total_size = int(raw['Capacity'][i]) + total_size
            chip['slot'] = raw['BankLabel'][i].replace("BANK ", "")
            chip['speed'] = raw['ConfiguredClockSpeed'][i]
            chip['PN'] = raw['PartNumber'][i].strip()
            chip['SN'] = raw['SerialNumber'][i]
            chip_list.append(chip)

        total_size = convert_file_size(int(total_size), 1024)
        total_size = f"{int(float(total_size.split(' ')[0]))} {total_size.split(' ')[1]}"

        return {
            "size": total_size,
            "memory_detail": chip_list
        }
