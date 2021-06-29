from converters.converter import Converter


class ValueGoTrough(Converter):
    def convert(self, value: int) -> int:
        return value

    def isValid(self, value: int) -> bool:
        return True
