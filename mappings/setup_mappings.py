from midi_controller import MidiController
from translator import Translator, FaderTranslator


def setup(midi: MidiController):
    setup_main_exec_faders(midi)
    pass


def setup_main_exec_faders(midi: MidiController):
    translators: [Translator] = [
        FaderTranslator((176, 7), (151, 7)),
        FaderTranslator((177, 7), (152, 7)),
        FaderTranslator((178, 7), (153, 7)),
        FaderTranslator((179, 7), (154, 7)),
        FaderTranslator((180, 7), (155, 7)),
        FaderTranslator((181, 7), (156, 7)),
        FaderTranslator((182, 7), (157, 7)),
        FaderTranslator((183, 7), (158, 7)),
        FaderTranslator((176, 14), (159, 7)),
    ]
    midi.apc_ma_translators.extend(translators)