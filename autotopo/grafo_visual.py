import json
import networkx as nx
import matplotlib.pyplot as plt

with open("topologia_completa.json", "r", encoding="utf-8") as f:
    dados = json.load(f)

G = nx.Graph()

for conexao in dados["conexoes"]:
    a = f'{conexao["dispositivo_a"]}\n{conexao["interface_a"]}'
    b = f'{conexao["dispositivo_b"]}\n{conexao["interface_b"]}'
    G.add_edge(a, b)

nx.draw(G, with_labels=True, node_color='lightblue', edge_color='gray', node_size=2500, font_size=8)
plt.savefig("Topologia.png")
print("✅ Grafo salvo como 'Topologia.png'")