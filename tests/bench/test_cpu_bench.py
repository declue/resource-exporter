from resource_exporter.bench.cpu_bench import CPUBench


def test_single():
    print(CPUBench().test_single_thread())


def test_full():
    # print(CPUBench().test_full_threads())
    pass
