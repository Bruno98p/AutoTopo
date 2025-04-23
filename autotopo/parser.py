import re
from .utils import expand_interface_name

def parse_ip_int_brief(raw_output):
    interfaces = []
    lines = raw_output.strip().splitlines()
    for line in lines[1:]:
        parts = re.split(r"\s+", line)
        if len(parts) >= 6:
            interfaces.append({
                "interface": parts[0],
                "ip": parts[1],
                "status": parts[4],
                "protocolo": parts[5]
            })
    return interfaces

def parse_int_description(raw_output):
    descricoes = []
    lines = raw_output.strip().splitlines()
    for line in lines[1:]:
        match = re.match(r"(\S+)\s+(up|down|admin-down)\s+(up|down)\s+(.*)?", line)
        if match:
            interface_abrev = match.group(1)
            descricao = match.group(4).strip() if match.group(4) else ""
            interface = expand_interface_name(interface_abrev)
            descricoes.append({
                "interface": interface,
                "descricao": descricao
            })
    return descricoes

# def parse_cdp_neighbors(raw_output):
#     vizinhos = []
#     lines = raw_output.strip().splitlines()
#     header_found = False
#     for line in lines:
#         if re.search(r"Device ID", line):
#             header_found = True
#             continue
#         if header_found and line.strip():
#             parts = re.split(r"\s{2,}", line.strip())
#             if len(parts) >= 5:
#                 local_interface = expand_interface_name(parts[1])
#                 remote_interface = expand_interface_name(parts[-1])
#                 vizinhos.append({
#                     "remote_device": parts[0],
#                     "local_interface": local_interface,
#                     "remote_interface": remote_interface
#                 })
#     return vizinhos


def parse_cdp_neighbors(raw_output):
    vizinhos = []
    lines = raw_output.strip().splitlines()
    header_found = False

    for line in lines:
        # Detecta início da tabela de vizinhança
        if not header_found and re.search(r"Device ID", line):
            header_found = True
            continue

        # Processa linhas após o cabeçalho
        if header_found:
            line = line.strip()
            if not line or "Total cdp entries" in line:
                continue  # Ignora linhas vazias ou sumário final

            # Divide por 2+ espaços (colunas do CDP)
            parts = re.split(r"\s{2,}", line)
            if len(parts) >= 5:
                try:
                    device_id = parts[0]
                    local_interface = expand_interface_name(parts[1])
                    remote_interface = expand_interface_name(parts[-1])
                    vizinhos.append({
                        "remote_device": device_id,
                        "local_interface": local_interface,
                        "remote_interface": remote_interface
                    })
                except Exception as e:
                    # print(f"[CDP Parser] Erro ao processar linha: {line} -> {e}")
                    continue  # Ignora linha com problema
            else:
                # print(f"[CDP Parser] Linha ignorada por formato incompleto: {line}")
                continue

    return vizinhos

