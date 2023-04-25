#
#
#
class Statistics(object):
    def __init__(self):
        self._results = {}
        self._cache = {}
        self._domain = {}
        self._ncall = 0
    def __call__(self,domain,A,B,R):
        if not domain in self._domain: self._domain[domain] = 1
        else: self._domain[domain] += 1

        if not domain in self._results: self._results[domain] = []
        self._results[domain] = self._results[domain] + [(A,B,R)]

        if not (domain,A,B,) in self._cache: self._cache[(domain,A,B,)] = 1
        else: self._cache[(domain,A,B,)] += 1
        self._ncall += 1
    def display(self):
        print('# definition applications',self._ncall)
        for key,value in self._domain.items(): print(key,value)

STAT = Statistics()
