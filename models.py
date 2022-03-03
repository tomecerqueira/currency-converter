class Pair:
    def __init__(self, code, name):
        self.code = code
        self.name = name

class ConvertedPair:
    def __init__(self, base_currency, to_currency, rate):
        self.base_currency = base_currency
        self.to_currency = to_currency
        self.rate = rate