from converters.converter import Converter
from converters.fix_value_filter import FixValueFilter
from converters.value_go_trough import ValueGoTrough


class Translator():
    converters: (Converter, Converter, Converter)

    def __init__(self, converters: (Converter, Converter, Converter)):
        self.converters = converters
        pass

    def translatable(self, values: [int]) -> bool:
        return self.converters[0].isValid(values[0]) and self.converters[1].isValid(values[1]) and self.converters[2].isValid(values[2])

    def translate(self, values: [int]) -> [int]:
        return [self.converters[0].convert(values[0]), self.converters[1].convert(values[1]), self.converters[2].convert(values[2])]

class FaderTranslator(Translator):
    def __init__(self, address: (int, int), destAddress: (int, int)):
        super().__init__((FixValueFilter(address[0], destAddress[0]), FixValueFilter(address[1], destAddress[1]), ValueGoTrough()))