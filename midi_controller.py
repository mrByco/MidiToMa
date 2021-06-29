import threading
import time
from typing import Dict

import rtmidi
from flask import json
from rtmidi import MidiIn, MidiOut

from model.setup import Setup
from translator import Translator
import asyncio

VIRTUAL_PORT_NAME = "MA Connector [plug it ;)] "
APC_INIT_CODE = [0xf0, 0x7e, 0x00, 0x06, 0x01, 0xf7, 0xf0, 0x47, 0x00, 0x73, 0x60, 0x00, 0x04, 0x41, 0x01, 0x01, 0x01, 0xf7,
                 0xB0, 0x18, 0x02, 0xB0, 0x19, 0x02, 0xB0, 0x1A, 0x02, 0xB0, 0x1B, 0x02, 0xB0, 0x1C, 0x02, 0xB0, 0x1D, 0x02,
                 0xB0, 0x1E, 0x02, 0xB0, 0x1F, 0x02, 0xB0, 0x38, 0x00, 0xB0, 0x39, 0x00, 0xB0, 0x3A, 0x00, 0xB0, 0x3B, 0x00,
                 0xB0, 0x3C, 0x00, 0xB0, 0x3D, 0x00, 0xB0, 0x3E, 0x00, 0xB0, 0x3F, 0x00]


class MidiController():
    apc_out = rtmidi.MidiOut()
    apc_in = rtmidi.MidiIn()
    ma_in = rtmidi.MidiIn()
    ma_out = rtmidi.MidiOut()

    availableIn: [str]
    availableOut: [str]

    selectedApcIn: str = None
    selectedApcOut: str = None
    selectedMaIn: str = None
    selectedMaOut: str = None

    apc_ma_translators: [Translator] = []

    def __init__(self):
        self.refresh_available_ports()
        self.loadState()


    def translate_loop_task(self):
        while True:
            message = self.apc_in.get_message()
            if (message):
                self.on_apc_message(message[0])
                print(f'midi{message[0]}')
            message = self.ma_in.get_message()
            if (message):
                print(f'mas{message}')

    def start_loop(self):
        b = threading.Thread(name='background', target=self.translate_loop_task)
        b.start()

    def refresh_available_ports(self):
        self.availableIn = self.apc_in.get_ports()
        self.availableOut = self.apc_out.get_ports()

    def get_setup_model(self) -> Setup:
        self.refresh_available_ports()
        selected_apc_in = self.selectedApcIn
        selected_apc_out = self.selectedApcOut
        return Setup(available_in_ports=self.availableIn, available_out_ports=self.availableOut,
                     selected_apc_in=selected_apc_in, selected_apc_out=selected_apc_out,
                     selected_ma_in=self.selectedMaIn, selected_ma_out=self.selectedMaOut)

    def selectInApcPort(self, in_port):
        self.selectMidiPort(self.apc_in, in_port)
        self.selectedApcIn = in_port
        self.savedState()

    def selectOutApcPort(self, out_port):
        self.selectMidiPort(self.apc_out, out_port)
        self.selectedApcOut = out_port
        self.apc_out.send_message(APC_INIT_CODE)
        self.savedState()

    def selectInMaPort(self, in_ma_port):
        self.selectMidiPort(self.ma_in, in_ma_port)
        self.selectedMaIn = in_ma_port
        self.savedState()

    def selectOutMaPort(self, out_ma_port: str):
        self.selectMidiPort(self.ma_out, out_ma_port)
        self.selectedMaOut = out_ma_port
        self.savedState()

    def selectMidiPort(self, midi, port: str):
        midi.close_port()
        ports: [str] = midi.get_ports()
        if port == None or port == "" or not port in ports:
            return
        index = ports.index(port)
        midi.open_port(index)


    def on_apc_message(self, message: [int]):
        for translator in self.apc_ma_translators:
            if translator.translatable(message):
                result = translator.translate(message)
                print(f'apc{message} > ma{result}')
                self.ma_out.send_message(result)

    def on_ma_message(self, message: (int, int, int)):
        print(message)

    def loadState(self):
        try:
            file = open('state.json', 'r')
            stateString = file.readline()
        except FileNotFoundError:
            file = open('state.json', mode='w+')
            file.writelines(['{}'])
            stateString = '{}'
        obj: Dict = json.loads(stateString)
        file.close()
        self.selectInApcPort(obj.get('selectedApcIn', ''))
        self.selectOutApcPort(obj.get('selectedApcOut', ''))
        self.selectInMaPort(obj.get('selectedMaIn', ''))
        self.selectOutMaPort(obj.get('selectedMaOut', ''))

    def savedState(self):
        obj = {
            'selectedApcIn': self.selectedApcIn,
            'selectedApcOut': self.selectedApcOut,
            'selectedMaIn': self.selectedMaIn,
            'selectedMaOut': self.selectedMaOut
        }
        stateString = json.dumps(obj)
        file = open('state.json', mode='w')
        file.writelines(stateString)
        file.close()

