from resource_exporter.info.ethernet.ethernet_info import EthernetInfo
from resource_exporter.interface.shell import Shell


class EthernetInfoMac(EthernetInfo):

    def __init__(self):
        EthernetInfo.__init__(self)

    def get(self):
        shell = Shell()
        ethernet_list_raw = shell.exec("networksetup -listallhardwareports | grep Device").split('\n')
        address_list = shell.exec("networksetup -listallhardwareports | grep Address").split('\n')
        type_list = shell.exec("networksetup -listallhardwareports | grep Port").split('\n')

        ethernet_list = list()
        idx = 0
        for ethernet in ethernet_list_raw:
            key = ethernet.replace("Device:", "").strip()
            if len(key) == 0:
                continue
            address = address_list[idx].replace("Ethernet Address:", "").strip()
            port_type = type_list[idx].replace("Hardware Port:", "").strip()

            port_type = port_type.replace("-", "")
            port_type = port_type.lower()

            ethernet = {
                "name": key,
                "address": address,
                "type": port_type
            }
            ethernet_list.append(ethernet)
            idx = idx + 1
        return ethernet_list
