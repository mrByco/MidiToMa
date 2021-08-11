from converters.fix_value_filter import FixValueFilter
from converters.value_go_trough import ValueGoTrough
from midi_controller import MidiController
from translator import Translator, FaderTranslator, ProgrammerEncoderTranslator


def setup(midi: MidiController):
    setup_main_exec_faders(midi)
    setup_side_enc_faders(midi)
    setup_programmer_encoders(midi)
    setup_main_exec_buttons(midi)
    setup_5x9_buttons(midi)
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

def setup_side_enc_faders(midi: MidiController):
    translators: [Translator] = [
        FaderTranslator((176, 16), (130, 1)),
        FaderTranslator((176, 17), (130, 2)),
        FaderTranslator((176, 18), (130, 3)),
        FaderTranslator((176, 19), (130, 4)),
        FaderTranslator((176, 20), (130, 5)),
        FaderTranslator((176, 21), (130, 6)),
        FaderTranslator((176, 22), (130, 7)),
        FaderTranslator((176, 23), (130, 8)),
    ]
    midi.apc_ma_translators.extend(translators)

def setup_programmer_encoders(midi: MidiController):
    translators: [Translator] = [
        ProgrammerEncoderTranslator((176, 48), (145, 8), (146, 8)),
        ProgrammerEncoderTranslator((176, 49), (131, 2), (132, 2)),
        ProgrammerEncoderTranslator((176, 50), (131, 3), (132, 3)),
        ProgrammerEncoderTranslator((176, 51), (131, 4), (132, 4)),
        ProgrammerEncoderTranslator((176, 52), (131, 5), (132, 5)),
        ProgrammerEncoderTranslator((176, 53), (131, 6), (132, 6)),
        ProgrammerEncoderTranslator((176, 54), (131, 7), (132, 7)),
        ProgrammerEncoderTranslator((176, 55), (131, 8), (132, 8)),
    ]
    midi.apc_ma_translators.extend(translators)


def setup_main_exec_buttons(midi: MidiController):
    translators: [Translator] = [
        Translator((ValueGoTrough(), FixValueFilter(50, 50), FixValueFilter(127, 127))),
        Translator((ValueGoTrough(), FixValueFilter(49, 49), FixValueFilter(127, 127))),
        Translator((ValueGoTrough(), FixValueFilter(48, 48), FixValueFilter(127, 127))),
    ]
    midi.apc_ma_translators.extend(translators)


def setup_5x9_buttons(midi: MidiController):
    translators: [Translator] = [
        Translator((ValueGoTrough(), FixValueFilter(51, 51), FixValueFilter(127, 127))),
        Translator((ValueGoTrough(), FixValueFilter(52, 52), FixValueFilter(127, 127))),

        Translator((ValueGoTrough(), FixValueFilter(53, 53), FixValueFilter(127, 127))),
        Translator((ValueGoTrough(), FixValueFilter(54, 54), FixValueFilter(127, 127))),
        Translator((ValueGoTrough(), FixValueFilter(55, 55), FixValueFilter(127, 127))),
        Translator((ValueGoTrough(), FixValueFilter(56, 56), FixValueFilter(127, 127))),
        Translator((ValueGoTrough(), FixValueFilter(57, 57), FixValueFilter(127, 127))),
        Translator((ValueGoTrough(), FixValueFilter(58, 58), FixValueFilter(127, 127))),

        Translator((ValueGoTrough(), FixValueFilter(80, 80), FixValueFilter(127, 127))),
        Translator((ValueGoTrough(), FixValueFilter(81, 81), FixValueFilter(127, 127))),
        Translator((ValueGoTrough(), FixValueFilter(82, 82), FixValueFilter(127, 127))),
        Translator((ValueGoTrough(), FixValueFilter(83, 83), FixValueFilter(127, 127))),
        Translator((ValueGoTrough(), FixValueFilter(84, 84), FixValueFilter(127, 127))),
        Translator((ValueGoTrough(), FixValueFilter(85, 85), FixValueFilter(127, 127))),
        Translator((ValueGoTrough(), FixValueFilter(86, 86), FixValueFilter(127, 127))),
    ]
    midi.apc_ma_translators.extend(translators)


