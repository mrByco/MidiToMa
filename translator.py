from converters.converter import Converter


class Translator():
    converters: (Converter, Converter, Converter)

    def __init__(self, converters: (Converter, Converter, Converter)):
        self.converters = converters
        pass

    def translate(values: (int, int, int)) -> (int, int, int):
        pass