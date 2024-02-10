from resource_exporter.info.ethernet.ethernet_info import EthernetInfo
from resource_exporter.interface.shell import Shell
from resource_exporter.interface.wmic_shell import WMICShell
from resource_exporter.util.file_util import convert_file_size


class EthernetInfoWin(EthernetInfo):

    def __init__(self):
        EthernetInfo.__init__(self)

    def get(self):
        shell = WMICShell()
        raw = shell.exec("wmic nic get")
        eth_list = []
        eth_count = len(raw['Caption'])

        type_map = self._get_eth_type_info()

        for i in range(eth_count):
            eth = {}
            if raw['PhysicalAdapter'][i] == 'FALSE':
                continue
            type_id = raw['PNPDeviceID'][i].replace("&amp;", "&").lower()
            eth['type'] = type_map[type_id]
            eth['name'] = raw['Name'][i]
            eth['address'] = raw['MACAddress'][i]
            eth['manufacturer'] = raw['Manufacturer'][i]
            eth['status'] = raw['NetConnectionStatus'][i]
            eth['connected'] = raw['NetEnabled'][i]
            eth['speed'] = convert_file_size(int(raw['Speed'][i]), 1000)
            eth_list.append(eth)

        return eth_list

    def _get_eth_type_info(self):
        shell = Shell()
        raw1 = shell.exec(
            "powershell gci 'hklm:SYSTEM\\CurrentControlSet\\Control\\Network\\{4D36E972-E325-11CE-BFC1-08002BE10318}'"
            " -rec ^| gp ^| FT Name  -Au")
        raw2 = shell.exec(
            "powershell gci 'hklm:SYSTEM\\CurrentControlSet\\Control\\Network\\{4D36E972-E325-11CE-BFC1-08002BE10318}'"
            " -rec ^| gp ^| FT PnpInstanceID -Au")

        name_list = raw1.split('\n')[2:]
        id_list = raw2.split('\n')[2:]

        type_map = {}
        for i, _ in enumerate(name_list):
            type_map[id_list[i].replace("\r", "").strip().lower()] = name_list[i].replace("\r", "").strip()
        return type_map
