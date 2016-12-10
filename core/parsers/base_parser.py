import abc


class BaseParser:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self):
        self.html_source = ''

    def parse(self):
        raise NotImplementedError("Should have implemented this")

    @staticmethod
    def _filter_invalid_cells(table_cells):
        import re
        counter_cell_pattern = re.compile(r'<td>[0-9]+</td>')
        return [cell for cell in table_cells
                if str(cell).replace(' ', '').replace('\t', '').replace('\n', '') != '<td>??</td>' and not
                counter_cell_pattern.match(str(cell))]

    @staticmethod
    def strip_euro_sign(money):
        return money[:-2]
