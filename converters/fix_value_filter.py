from converters.converter import Converter


class FixValueFilter(Converter):
    inValue: int
    outValue: int

    def __init__(self, inValue: int, outValue: int):
        self.inValue = inValue
        self.outValue = outValue

    def convert(self, value: int) -> int:
        return self.outValue

    def isValid(self, value: int) -> bool:
        return value == self.inValue
