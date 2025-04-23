import re

def expand_interface_name(interface):
    mapping = {
        "Gi": "GigabitEthernet",
        "Gig": "GigabitEthernet",
        "Fa": "FastEthernet",
        "Te": "TenGigabitEthernet",
        "Lo": "Loopback",
        "Se": "Serial",
        "Eth": "Ethernet",
        "Po": "Port-channel"
    }

    # Suporte a interfaces com 2 ou 3 níveis (ex: Gi0/1 ou Gi1/0/1)
    match = re.match(r"([A-Za-z]+)\s*(\d+(?:/\d+){1,2})", interface)
    if match:
        prefix, numbers = match.groups()
        full_prefix = mapping.get(prefix, prefix)
        return f"{full_prefix}{numbers}"

    return interface.strip()
