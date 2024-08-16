import requests
from os import environ

import xml.etree.ElementTree as ET

BASE_URL = environ.get("OPENDATA_BASE_URL", "")

r = requests.get(f"{BASE_URL}/retornarVotacionesXAnno?prmAnno=2022")
tree = ET.parse(r.text)
root = tree.getroot()


namespace = {"ns": "http://opendata.camara.cl/camaradiputados/v1"}
listaVotaciones = []

with open("votaciones_por_anno.xml", "r") as f:
    root = ET.fromstring(f.read())
    votaciones = root.findall(".//ns:Votacion", namespace)
    for votacion in votaciones:
        listaVotaciones.append(votacion.find("ns:Id", namespace).text)

listaDetalleVotaciones = []

for votacion in listaVotaciones:
    with open(f"votaciones/votacion_detalle_{votacion}", "w") as f:
        url = f"{BASE_URL}/retornarVotacionDetalle?prmVotacionId={votacion}"
        r = requests.get(url)
        f.write(r.text)