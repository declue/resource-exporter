import xmltodict

from resource_exporter.info.ethernet.ethernet_info import EthernetInfo
from resource_exporter.interface.shell import Shell


class EthernetInfoLinux(EthernetInfo):

    def __init__(self):
        EthernetInfo.__init__(self)

    def get(self):
        shell = Shell()
        raw = shell.exec('lshw -class network -xml')
        json_data = xmltodict.parse(raw)
        eth_list = []
        if isinstance(json_data['list']['node'], list):
            for i in range(len(json_data['list']['node'])):
                eth = self._get_node_info(json_data['list']['node'][i])
                if eth is not None:
                    eth_list.append(eth)
        else:
            eth = self._get_node_info(json_data['list']['node'])
            if eth is not None:
                eth_list.append(eth)
        return eth_list

    @classmethod
    def _get_node_info(cls, node):
        eth = {}
        eth['type'] = node['description'] if 'description' in node else ""
        if eth['type'] == 'Ethernet interface':
            eth['type'] = 'ethernet'
        elif eth['type'] == 'Wireless interface':
            eth['type'] = 'wifi'
        eth['name'] = node['product'] if 'product' in node else ""
        eth['interface'] = node['logicalname'] if 'logicalname' in node else ""
        eth['manufacturer'] = node['vendor'] if 'vendor' in node else ""
        eth['address'] = node['serial'] if 'serial' in node else ""

        invalid = False
        for item in node['configuration']['setting']:
            if item['@id'] == 'speed':
                eth['speed'] = item['@value']
            if item['@id'] == 'driver' and item['@value'] == 'bridge':
                invalid = True
        if invalid is True:
            return None

        for item in node['capabilities']['capability']:
            if item['@id'] == 'physical':
                eth['phy'] = item['#text']
        return eth
