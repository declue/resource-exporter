import platform

from resource_exporter.info.system.os_type import OSType
from resource_exporter.interface.shell import Shell


def test_get_os_type():
    shell = Shell()
    os_type = shell.get_os()
    if platform.platform().startswith("Windows"):
        assert os_type == OSType.WINDOWS
    elif platform.platform().startswith("Linux"):
        assert os_type == OSType.LINUX
    elif platform.platform().startswith("Darwin") or platform.platform().startswith("macOS"):
        assert os_type == OSType.MAC
    else:
        assert os_type == OSType.UNKNOWN


def test_exec():
    shell = Shell()
    result = shell.exec("ls")
    assert result is not None
