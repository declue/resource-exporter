from resource_exporter.interface.shell import Shell


class WMICShell(Shell):

    def __init__(self):
        Shell.__init__(self)

    def exec(self, command, encoding_type=None):
        output = Shell.exec(command + "/format:value", encoding_type)
        return self._parse(output)

    @classmethod
    def _parse(cls, output: str):
        ret = {}
        for line in output.split("\n"):
            if len(line) == 0:
                continue
            items = line.split("=")
            if len(items) != 2:
                continue
            if items[0] not in ret:
                ret[items[0]] = [items[1].replace("\r", "")]
            else:
                old = ret[items[0]]
                if isinstance(old, str):
                    ret[items[0]] = [old]
                ret[items[0]].append(items[1].replace("\r", ""))
        return ret
