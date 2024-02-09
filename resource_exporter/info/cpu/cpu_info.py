import abc

from resource_exporter.info.cpu.cpu_benchmark_net_fetcher import CpuBenchmarkNetFetcher


class CPUInfo(metaclass=abc.ABCMeta):

    def __init__(self):
        pass

    @abc.abstractmethod
    def get(self):
        pass

    @classmethod
    def _get_cpu_benchmark_net_data(cls, cpu_name):
        return CpuBenchmarkNetFetcher().fetch_cpu_info(cpu_name)
