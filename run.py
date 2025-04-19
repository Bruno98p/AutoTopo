import json
from autotopo.main import gerar_topologia
from autotopo.grafo import montar_topologia

if __name__ == "__main__":
    pasta = "configs"
    print(f"📥 Lendo arquivos da pasta '{pasta}'...")

    # Gera os dispositivos
    topologia = gerar_topologia(pasta)
    print("✅ Topologia de dispositivos processada.")

    # Gera as conexões
    conexoes = montar_topologia(topologia["dispositivos"])
    print("✅ Conexões entre dispositivos processadas.")

    # Adiciona as conexões dentro da topologia
    topologia["conexoes"] = conexoes["conexoes"]

    # Salva tudo num único arquivo
    with open("topologia_completa.json", "w", encoding="utf-8") as f:
        json.dump(topologia, f, indent=4)

    print("✅ Topologia completa salva em 'topologia_completa.json'")



import subprocess

# Executa o script diretamente
subprocess.run(["python3", "autotopo/grafo_visual.py"])
