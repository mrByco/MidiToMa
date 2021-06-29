class Setup():
    available_in_ports: [str]
    available_out_ports: [str]

    selected_apc_out: str
    selected_apc_in: str
    selected_ma_out: str
    selected_ma_in: str

    def __init__(self, available_in_ports: [str], available_out_ports: [str], selected_apc_out: str,
                 selected_apc_in: str, selected_ma_out: str, selected_ma_in: str):
        self.available_in_ports = available_in_ports
        self.available_out_ports = available_out_ports

        self.selected_apc_out = selected_apc_out
        self.selected_apc_in = selected_apc_in
        self.selected_ma_out = selected_ma_out
        self.selected_ma_in = selected_ma_in

        self.usedPorts = [selected_ma_in, selected_ma_out, selected_apc_in, selected_apc_out]
