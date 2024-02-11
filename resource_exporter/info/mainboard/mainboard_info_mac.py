from resource_exporter.info.mainboard.mainboard_info import MainBoardInfo
from resource_exporter.interface.shell import Shell


class MainBoardInfoMac(MainBoardInfo):

    def __init__(self):
        MainBoardInfo.__init__(self)

    def get(self):
        shell = Shell()
        raw = shell.exec("ioreg -l | grep IOPlatformSerialNumber")
        sn = raw.split("=")[1].replace("\"", "").strip()

        return {"name": "Mac Board",
                "Manufacturer": "Apple",
                "SN": sn}
