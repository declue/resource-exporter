import abc
import platform
import subprocess

from resource_exporter.info.system.os_type import OSType


class Shell(metaclass=abc.ABCMeta):

    def __init__(self):
        self.os_type = self.get_os()

    @classmethod
    def get_os(cls):
        raw: str = platform.system()
        if raw.lower() == "darwin":
            return OSType.MAC
        if raw.lower() == "linux" or raw.lower() == "linux2":
            return OSType.LINUX
        if raw.lower() == "win32" or raw.lower() == "win64" or raw.lower() == "windows":
            return OSType.WINDOWS

        return OSType.UNKNOWN

    def exec(self, command, encoding_type=None):
        if encoding_type is None:
            encoding_type = self.encoding_type()

        with subprocess.Popen(command, shell=True, stdout=subprocess.PIPE) as pipe:
            stdout, _stderr = pipe.communicate()
        return stdout.decode(encoding_type)

    def encoding_type(self):
        if self.os_type == OSType.WINDOWS:
            return "euc-kr"
        return "utf8"
