from flask import Flask, render_template, request, redirect
from mappings.setup_mappings import setup as setup_midi
import rtmidi

from midi_controller import MidiController

app = Flask(__name__)

midi = MidiController()
midi.start_loop()
setup_midi(midi)


@app.route('/')
def setup():
    return getSetupPage()


@app.route('/select')
def select():
    in_apc_port = request.args.get('in_apc_port', default=None)
    out_apc_port = request.args.get('out_apc_port', default=None)
    in_ma_port = request.args.get('in_ma_port', default=None)
    out_ma_port = request.args.get('out_ma_port', default=None)
    if in_apc_port != None:
        midi.selectInApcPort(in_apc_port)
    if out_apc_port != None:
        midi.selectOutApcPort(out_apc_port)
    if in_ma_port != None:
        midi.selectInMaPort(in_ma_port)
    if out_ma_port != None:
        midi.selectOutMaPort(out_ma_port)
    return redirect('/')


def getSetupPage():
    return render_template('setup.html', model=midi.get_setup_model())


if __name__ == '__main__':
    print("Starting on localhost:5000...")
    app.run()
