import abc
import os
import subprocess
import platform
from resource_exporter.info.system.os_type import OSType


class Shell(metaclass=abc.ABCMeta):

    def __init__(self):
        self.os_type = self.get_os()

    @classmethod
    def get_os(cls):
        raw: str = platform.system()
        if raw.lower() == "darwin":
            return OSType.Mac
        elif raw.lower() == "linux" or raw.lower() == "linux2":
            return OSType.Linux
        elif raw.lower() == "win32" or raw.lower() == "win64" or raw.lower() == "windows":
            return OSType.Windows
        else:
            return OSType.Unknown

    def exec(self, command, encoding_type=None):
        if encoding_type is None:
            encoding_type = self.encoding_type()

        with subprocess.Popen(command, shell=True, stdout=subprocess.PIPE) as p:
            stdout, stderr = p.communicate()
        return stdout.decode(encoding_type)

    def encoding_type(self):
        if self.os_type == OSType.Windows:
            return "euc-kr"
        else:
            return "utf8"
