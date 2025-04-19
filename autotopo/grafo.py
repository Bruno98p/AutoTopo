def montar_dispositivo(hostname, ip_brief, int_desc, cdp):
  dispositivo = {
      "hostname": hostname,
      "interfaces": {}
  }

  for intf in ip_brief:
      nome = intf["interface"]

      descricao_info = next((i for i in int_desc if i["interface"] == nome), {})
      cdp_info = next((c for c in cdp if c["local_interface"] == nome), {})

      dispositivo["interfaces"][nome] = {
          "ip": intf.get("ip", ""),
          "status": intf.get("status", ""),
          "protocolo": intf.get("protocolo", ""),
          "descricao": descricao_info.get("descricao", ""),
          "conectado_a": {
              "dispositivo": cdp_info.get("remote_device"),
              "interface": cdp_info.get("remote_interface")
          } if cdp_info else None
      }
  return dispositivo


def identificar_tipo(hostname):
  if hostname.lower().startswith("sw"):
      return "switch"
  elif hostname.lower().startswith("r"):
      return "roteador"
  else:
      return "desconhecido"








def montar_topologia(dispositivos):
  conexoes = []

  for hostname, dados in dispositivos.items():
      interfaces = dados.get("interfaces", {})

      for nome_intf, intf_data in interfaces.items():
          vizinho = intf_data.get("conectado_a")
          if vizinho and vizinho["dispositivo"]:
              if hostname < vizinho["dispositivo"]:
                  conexoes.append({
                      "dispositivo_a": hostname,
                      "interface_a": nome_intf,
                      "ip_a": intf_data.get("ip"),
                      "descricao_a": intf_data.get("descricao"),
                      "dispositivo_b": vizinho["dispositivo"],
                      "interface_b": vizinho["interface"],
                      "ip_b": dispositivos.get(vizinho["dispositivo"], {}).get("interfaces", {}).get(vizinho["interface"], {}).get("ip"),
                      "descricao_b": dispositivos.get(vizinho["dispositivo"], {}).get("interfaces", {}).get(vizinho["interface"], {}).get("descricao")
                  })

  return {"conexoes": conexoes}
