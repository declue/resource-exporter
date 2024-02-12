import time
from multiprocessing import Pool, cpu_count


class CPUBench:

    def __init__(self):
        self.default_max_prime = 10000000

    def is_prime(self, n):
        if n <= 1:
            return False
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False
        return True

    def find_primes(self, start_end):
        start, end = start_end
        count = 0
        for number in range(start, end):
            if self.is_prime(number):
                count += 1
        return count

    def measure_cpu_performance(self, num_processes, task_size):
        start_time = time.time()
        tasks = [(i * task_size, (i + 1) * task_size) for i in range(num_processes)]
        with Pool(processes=num_processes) as pool:
            results = pool.map(self.find_primes, tasks)
        total_primes = sum(results)
        end_time = time.time()
        duration = end_time - start_time
        eps = total_primes / duration
        return duration, eps, total_primes

    def test_single_thread(self):
        num_processes = 1
        task_size = self.default_max_prime // num_processes
        return num_processes, self.measure_cpu_performance(num_processes, task_size)

    def test_full_threads(self):
        num_processes = cpu_count()
        task_size = self.default_max_prime // num_processes
        return num_processes, self.measure_cpu_performance(num_processes, task_size)
