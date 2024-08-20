import requests
import xml.etree.ElementTree as ET
import os
from html import unescape  #  HTML entities

BASE_URL = os.environ.get("OPENDATA_BASE_URL", "https://opendata.camara.cl/camaradiputados/WServices/WSLegislativo.asmx")  # Replace 'example.com' with your actual base URL

try:
    # HTTP request para XML data
    response = requests.get(f"{BASE_URL}/retornarVotacionesXAnno?prmAnno=2022")
    response.raise_for_status() 

    # test 1
    print("XML Content:", response.text)

    #  XML to replace HTML entities
    xml_content = unescape(response.text)

    # Parse xml
    root = ET.fromstring(xml_content)

    namespace = {"ns": "http://opendata.camara.cl/camaradiputados/v1"}
    listaVotaciones = []

    # Iterate through XML elements to extract law IDs
    votaciones = root.findall(".//ns:Votacion", namespace)
    for votacion in votaciones:
        listaVotaciones.append(votacion.find("ns:Id", namespace).text)

    # agarra todo
    for votacion in listaVotaciones:
        filename = f"votaciones/votacion_detalle_{votacion}.xml"
        os.makedirs(os.path.dirname(filename), exist_ok=True)  
        with open(filename, "w") as f:
            url = f"{BASE_URL}/retornarVotacionDetalle?prmVotacionId={votacion}"
            try:
                response = requests.get(url)
                response.raise_for_status()  
                f.write(response.text)
            except requests.exceptions.RequestException as e:
                print(f"Error fetching data for votacion {votacion}: {e}")

except requests.exceptions.RequestException as e:
    print(f"Error fetching data: {e}")
except ET.ParseError as e:
    print(f"Error parsing XML: {e}")