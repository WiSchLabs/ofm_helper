class BaseParser:
    def __init__(self):
        self.url = ''

    def parse(self):
        raise NotImplementedError("Should have implemented this")
