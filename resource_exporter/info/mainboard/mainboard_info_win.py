from resource_exporter.info.mainboard.mainboard_info import MainBoardInfo
from resource_exporter.interface.wmic_shell import WMICShell


class MainBoardInfoWin(MainBoardInfo):

    def __init__(self):
        MainBoardInfo.__init__(self)

    def get(self):
        shell = WMICShell()
        raw_data = shell.exec("wmic baseboard get")
        return {
            "name": raw_data['Product'],
            "SN": raw_data['SerialNumber'],
            "Manufacturer": raw_data['Manufacturer']
        }
