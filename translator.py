from converters.converter import Converter
from converters.encoder_value_converter import EncoderValueConverter
from converters.fix_value_filter import FixValueFilter
from converters.value_go_trough import ValueGoTrough


class Translator():
    converters: (Converter, Converter, Converter)

    def __init__(self, converters: (Converter, Converter, Converter)):
        self.converters = converters
        pass

    def translatable(self, values: [int]) -> bool:
        return self.converters[0].isValid(values[0]) and self.converters[1].isValid(values[1]) and self.converters[
            2].isValid(values[2])

    def translate(self, values: [int]) -> [int]:
        return [self.converters[0].convert(values[0]), self.converters[1].convert(values[1]),
                self.converters[2].convert(values[2])]

    def get_instant_feedback(self, values: [int]) -> [int]:
        feedback: [int] = [self.converters[0].getPossibleFeedback(values[0]),
                           self.converters[1].getPossibleFeedback(values[1]),
                           self.converters[2].getPossibleFeedback(values[2])]
        if len([value for value in feedback if value is None]) > 0:
            return None
        return [self.converters[0].getPossibleFeedback(values[0]), self.converters[1].getPossibleFeedback(values[1]),
                self.converters[2].getPossibleFeedback(values[2])]


class ProgrammerEncoderTranslator(Translator):
    negative_dest_address: (int, int)
    positive_dest_address: (int, int)
    address: (int, int)
    repeat_message = 0

    def __init__(self, address: (int, int), destAddressPos: (int, int), destAddressNeg: (int, int)):
        self.address = address
        self.positive_dest_address = destAddressPos
        self.negative_dest_address = destAddressNeg
        super().__init__([])

    def translate(self, values: [int]) -> [int]:
        self.repeat_message = abs(values[2] - 63)
        print(self.repeat_message)
        if values[2] > 63:
            return (self.positive_dest_address[0], self.positive_dest_address[1], 60)
        else:
            return (self.negative_dest_address[0], self.negative_dest_address[1],60)

    def get_instant_feedback(self, values: [int]) -> [int]:
        return [self.address[0], self.address[1], 63]

    def translatable(self, values: [int]) -> bool:
        return values[0] == self.address[0] and values[1] == self.address[1]


class FaderTranslator(Translator):
    def __init__(self, address: (int, int), destAddress: (int, int)):
        super().__init__(
            (FixValueFilter(address[0], destAddress[0]), FixValueFilter(address[1], destAddress[1]), ValueGoTrough()))
