class BaseParser:
    def __init__(self):
        self.html_source = ''

    def parse(self):
        raise NotImplementedError("Should have implemented this")
