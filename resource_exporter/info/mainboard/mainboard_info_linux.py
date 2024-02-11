from resource_exporter.info.mainboard.mainboard_info import MainBoardInfo
from resource_exporter.interface.shell import Shell


class MainBoardInfoLinux(MainBoardInfo):

    def __init__(self):
        MainBoardInfo.__init__(self)

    def get(self):
        shell = Shell()
        return {"name": shell.exec("sudo dmidecode -s baseboard-product-name").replace('\n', ''),
                "Manufacturer": shell.exec("sudo dmidecode -s baseboard-serial-number").replace('\n', ''),
                "SN": shell.exec("sudo dmidecode -s baseboard-manufacturer").replace('\n', '')}
