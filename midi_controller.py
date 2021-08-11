import math
import threading
import time
from typing import Dict

import rtmidi
import serial
from flask import json
from rtmidi import MidiIn, MidiOut

from model.setup import Setup
from translator import Translator, ProgrammerEncoderTranslator
import asyncio

VIRTUAL_PORT_NAME = "MA Connector [plug it ;)] "
APC_INIT_CODE = [0xf0, 0x7e, 0x00, 0x06, 0x01, 0xf7, 0xf0, 0x47, 0x00, 0x73, 0x60, 0x00, 0x04, 0x41, 0x01, 0x01, 0x01,
                 0xf7,
                 0xB0, 0x18, 0x02, 0xB0, 0x19, 0x02, 0xB0, 0x1A, 0x02, 0xB0, 0x1B, 0x02, 0xB0, 0x1C, 0x02, 0xB0, 0x1D,
                 0x02,
                 0xB0, 0x1E, 0x02, 0xB0, 0x1F, 0x02, 0xB0, 0x38, 0x00, 0xB0, 0x39, 0x00, 0xB0, 0x3A, 0x00, 0xB0, 0x3B,
                 0x00,
                 0xB0, 0x3C, 0x00, 0xB0, 0x3D, 0x00, 0xB0, 0x3E, 0x00, 0xB0, 0x3F, 0x00]

try:
    button_serial = serial.Serial("COM7", 57600)
except:
    button_serial = None


class MidiController:
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
    ma_apc_translators: [Translator] = []

    def __init__(self):
        self.refresh_available_ports()
        self.load_state()

    def translate_loop_task(self):
        if button_serial is not None:
            button_serial.flushInput()
        while True:
            t1 = time.time()
            message = self.apc_in.get_message()
            if message:
                self.on_apc_message(message[0])
                print(f'apc{message[0]}')
            message = self.ma_in.get_message()
            if message:
                self.apc_out.send_message(message[0])
                print(f'ma{message[0]}')

            if button_serial is not None and button_serial.in_waiting:
                print(button_serial.in_waiting)
                inp = button_serial.readline()
                msg = inp.decode()

                print(msg)
                num_str = ""
                for char in msg:
                    try:
                        int(char)
                        num_str += char
                    except:
                        if num_str != "":
                            self.on_x_keys_message(int(num_str), True if char == "t" else False)
                            num_str = ""

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
                if type(translator) is ProgrammerEncoderTranslator:
                    for i in range(translator.repeat_message):
                        print('repeat')
                        self.ma_out.send_message(result)
                else:
                    self.ma_out.send_message(result)
                feedback = translator.get_instant_feedback(message)
                if feedback != None:
                    self.apc_out.send_message(feedback)

    def on_x_keys_message(self, key_number: int, state: bool):
        if key_number == 1:
            return
        if state:
            message = [0x90 + ((key_number % 5)), 121 + math.floor(key_number / 5), 127 if state else 0]
        else:
            message = [0x80 + ((key_number % 5)), 121 + math.floor(key_number / 5), 127 if state else 0]
        print(message)
        self.ma_out.send_message(message)

    def load_state(self):
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
