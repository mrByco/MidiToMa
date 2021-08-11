class Converter:
    feedback_same: bool

    def __init__(self, feedback_same: bool = False):
        self.feedback_same = feedback_same

    def isValid(self, value: int) -> bool:
        pass

    def convert(self, value: int) -> int:
        pass

    def getPossibleFeedback(self, value: int) -> int:
        if self.feedback_same:
            return value
        else:
            return None
