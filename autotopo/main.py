import os
from .parser import parse_ip_int_brief, parse_int_description, parse_cdp_neighbors
from .grafo import montar_dispositivo


def ler_blocos_comando(conteudo):
    blocos = {}
    atual = None
    for linha in conteudo.splitlines():
        if linha.startswith("===") and "===" in linha[4:]:
            atual = linha.replace("=", "").strip().lower()
            blocos[atual] = ""
        elif atual:
            blocos[atual] += linha + "\n"
    return blocos

def processar_config(hostname, conteudo):
    blocos = ler_blocos_comando(conteudo)

    ip_brief = parse_ip_int_brief(blocos.get("show ip int brief", ""))
    int_desc = parse_int_description(blocos.get("show interfaces description", ""))
    cdp = parse_cdp_neighbors(blocos.get("show cdp neighbors", ""))

    return montar_dispositivo(hostname, ip_brief, int_desc, cdp)

def gerar_topologia(pasta_config):
    topologia = {"dispositivos": {}}

    for arquivo in os.listdir(pasta_config):
        if arquivo.endswith(".txt"):
            hostname = os.path.splitext(arquivo)[0]
            with open(os.path.join(pasta_config, arquivo), "r", encoding="utf-8") as f:
                conteudo = f.read()
                dispositivo = processar_config(hostname, conteudo)
                topologia["dispositivos"][hostname] = dispositivo

    return topologia

