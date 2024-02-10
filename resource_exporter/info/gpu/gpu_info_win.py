from resource_exporter.info.gpu.gpu_info import GPUInfo
from resource_exporter.interface.shell import Shell
from resource_exporter.interface.wmic_shell import WMICShell
from resource_exporter.util.file_util import convert_file_size


class GPUInfoWin(GPUInfo):

    def __init__(self):
        GPUInfo.__init__(self)

    def get(self):
        wmic_shell = WMICShell()
        shell = Shell()
        raw = wmic_shell.exec("wmic path win32_VideoController get")
        gpu_list = list()
        gpu_count = len(raw['Caption'])
        for i in range(gpu_count):
            gpu = dict()
            gpu['name'] = raw['Name'][i]
            gpu['manufacturer'] = raw['AdapterCompatibility'][i]
            gpu['memory'] = convert_file_size(raw['AdapterRAM'][i], 1024)
            if gpu['memory'] == '4.0 GB' and 'Intel' not in gpu['name']:
                command = "powershell -command (Get-ItemProperty -Path '{}' -Name {}  -ErrorAction SilentlyContinue)" \
                    .format(
                    "HKLM:\SYSTEM\ControlSet001\Control\Class\{4d36e968-e325-11ce-bfc1-08002be10318}\\0*",
                    "HardwareInformation.qwMemorySize"
                )
                for line in shell.exec(command).split('\n'):
                    if 'HardwareInformation.qwMemorySize' in line:
                        gpu['memory'] = convert_file_size(
                            int(line.replace('HardwareInformation.qwMemorySize :', '').strip()),
                            1024)
            gpu['driver'] = raw['DriverVersion'][i]
            gpu['status'] = raw['Status'][i]
            gpu_list.append(gpu)

        return gpu_list
