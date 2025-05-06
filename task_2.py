import math
import re
import timeit
from tabulate import tabulate
import mmh3


class HyperLogLog:
    def __init__(self, p=5):
        self.p = p
        self.m = 1 << p
        self.registers = [0] * self.m
        self.alpha = self._get_alpha()
        self.small_range_correction = 5 * self.m / 2

    def _get_alpha(self):
        if self.p <= 16:
            return 0.673
        elif self.p == 32:
            return 0.697
        else:
            return 0.7213 / (1 + 1.079 / self.m)

    def add(self, item):
        x = mmh3.hash(str(item), signed=False)
        j = x & (self.m - 1)
        w = x >> self.p
        self.registers[j] = max(self.registers[j], self._rho(w))

    def _rho(self, w):
        return len(bin(w)) - 2 if w > 0 else 32

    def count(self):
        Z = sum(2.0 ** -r for r in self.registers)
        E = self.alpha * self.m * self.m / Z

        if E <= self.small_range_correction:
            V = self.registers.count(0)
            if V > 0:
                return self.m * math.log(self.m / V)

        return E


class UniquesCounter:
    def __init__(self):
        self._uniques = set()

    def add(self, item):
        self._uniques.add(item)

    def count(self):
        return len(self._uniques)


def estimate_cardinality(counter):
    with open('lms-stage-access.log') as fh:
        pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')

        for line in fh.readlines():
            match = re.findall(pattern, line)
            if match is not None:
                for x in match:  # iter and add
                    counter.add(x)

    return counter.count()


hll = HyperLogLog(p=16)
uc = UniquesCounter()

hll_start = timeit.default_timer()
hll_estimation = estimate_cardinality(hll)
hll_time = timeit.default_timer() - hll_start

uc_start = timeit.default_timer()
uc_estimation = estimate_cardinality(uc)
uc_time = timeit.default_timer() - uc_start

results = {
    'Точний підрахунок': {
        'Унікальні елементи': uc_estimation,
        'Час виконання (сек.)': uc_time
    },
    'HyperLogLog': {
        'Унікальні елементи': hll_estimation,
        'Час виконання (сек.)': hll_time
    }
}

table = tabulate(
    {
        '': ['Унікальні елементи', 'Час виконання (сек.)'],
        'Точний підрахунок': [uc_estimation, uc_time],
        'HyperLogLog': [hll_estimation, hll_time]
    },
    headers="keys", tablefmt="simple_grid"
)

print(table)
