from converters.converter import Converter


class EncoderValueConverter(Converter):
    onPositive: int
    onNegative: int

    def __init__(self, onPositive: int, onNegative: int):
        super().__init__(feedback_same=False)
        self.onPositive = onPositive
        self.onNegative = onNegative

    def convert(self, value: int) -> int:
        if value - int(127/2) > 0:
            return self.onPositive
        else:
            return self.onNegative

    def isValid(self, value: int) -> bool:
        return value != int(127/2)

    def getPossibleFeedback(self, value: int) -> int:
        return int(127/2)