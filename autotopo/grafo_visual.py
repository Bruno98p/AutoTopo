import matplotlib.pyplot as plt
import networkx as nx
import os
import json

try:
    # Carrega a topologia salva
    json_path = "Produtos/topologia_completa.json"
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"Arquivo não encontrado: {json_path}")

    with open(json_path, "r", encoding="utf-8") as f:
        topo = json.load(f)

    G = nx.Graph()

    # Adiciona nós
    cores = []
    formas = {}
    for nome, dados in topo["dispositivos"].items():
        tipo = dados.get("tipo", "host").lower()
        G.add_node(nome, tipo=tipo)

        if tipo == "roteador":
            cores.append("red")
            formas[nome] = "s"
        elif tipo == "switch":
            cores.append("skyblue")
            formas[nome] = "o"
        else:
            cores.append("lightgreen")
            formas[nome] = "d"

    # Adiciona conexões
    for conexao in topo["conexoes"]:
        origem = conexao["dispositivo_a"]
        destino = conexao["dispositivo_b"]
        intf_origem = conexao["interface_a"]
        intf_destino = conexao["interface_b"]

        if origem not in G.nodes or destino not in G.nodes:
            print(f"⚠️ Conexão ignorada: {origem} ⇄ {destino} (dispositivo ausente)")
            continue

        label = f"{intf_origem} ⇄ {intf_destino}"
        G.add_edge(origem, destino, label=label)

    if len(G.edges) == 0:
        print("⚠️ Atenção: Nenhuma conexão foi detectada na topologia.")

    # Layout
    pos = nx.spring_layout(G, seed=42)

    # Tamanho da figura
    num_dispositivos = len(topo["dispositivos"])
    largura = max(10, num_dispositivos * 3)
    altura = max(6, num_dispositivos * 2)

    plt.figure(figsize=(largura, altura))

    # Nós por forma
    for shape in set(formas.values()):
        nos_com_forma = [n for n in G.nodes() if formas[n] == shape]
        nx.draw_networkx_nodes(
            G,
            pos,
            nodelist=nos_com_forma,
            node_shape=shape,
            node_color=[cores[list(G.nodes()).index(n)] for n in nos_com_forma],
            node_size=1500
        )

    # Labels e arestas
    nx.draw_networkx_labels(G, pos, font_size=10, font_family="monospace")
    nx.draw_networkx_edges(G, pos)

    # ✅ Correção: define edge_labels corretamente
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

    # Interfaces/IPs
    for conexao in topo["conexoes"]:
        origem = conexao["dispositivo_a"]
        destino = conexao["dispositivo_b"]

        if origem not in pos or destino not in pos:
            continue

        intf_origem = conexao["interface_a"]
        intf_destino = conexao["interface_b"]
        ip_origem = conexao["ip_a"]
        ip_destino = conexao["ip_b"]

        x_o, y_o = pos[origem]
        x_d, y_d = pos[destino]

        plt.text(x_o - 0.05, y_o + 0.08, f"{intf_origem}\n{ip_origem}", fontsize=8, ha='right',
                 bbox=dict(facecolor='white', alpha=0.7, boxstyle='round,pad=0.3'))
        plt.text(x_d + 0.05, y_d + 0.08, f"{intf_destino}\n{ip_destino}", fontsize=8, ha='left',
                 bbox=dict(facecolor='white', alpha=0.7, boxstyle='round,pad=0.3'))

    plt.axis("off")
    plt.title("Topologia de Rede - AutoTopo", fontsize=14, pad=20)
    saida = "Produtos/topologia.png"
    plt.savefig(saida, dpi=150)
    print(f"✅ Topologia gerada com sucesso em: {saida}")

except Exception as e:
    print(f"❌ Erro ao gerar topologia: {e}")
