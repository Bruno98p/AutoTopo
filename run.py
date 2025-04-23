import os
import json
import sys
import subprocess
from autotopo.main import gerar_topologia
from autotopo.grafo import montar_topologia

def executar_pipeline(pasta="configs"):
    print(f"📥 Lendo arquivos da pasta '{pasta}'...")

    # Gera a estrutura da topologia a partir dos arquivos
    topologia = gerar_topologia(pasta)
    print("✅ Topologia de dispositivos processada.")

    # Monta as conexões entre dispositivos
    conexoes = montar_topologia(topologia["dispositivos"])
    print("✅ Conexões entre dispositivos processadas.")

    # Adiciona conexões à topologia
    topologia["conexoes"] = conexoes.get("conexoes", [])

    # Caminho para salvar o JSON de saída
    os.makedirs("Produtos", exist_ok=True)
    json_path = os.path.join("Produtos", "topologia_completa.json")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(topologia, f, indent=4)

    print(f"✅ Topologia completa salva em '{json_path}'")

    # Gera o grafo visual
    subprocess.run([sys.executable, "autotopo/grafo_visual.py"], check=True)
    print("✅ Imagem gerada com sucesso!")

# Só executa se rodar diretamente este arquivo
if __name__ == "__main__":
    executar_pipeline()
