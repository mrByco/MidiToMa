from converters.converter import Converter


class ValueGoTrough(Converter):
    def __init__(self, feedback_same: bool = False):
        super().__init__(feedback_same=feedback_same)

    def convert(self, value: int) -> int:
        return value

    def isValid(self, value: int) -> bool:
        return True
