import dlt
import requests
from dotenv import load_dotenv

# CARGAR VARIABLES DE ENTORNO
load_dotenv()



# URL de la API (Puebla)
URL_CLIMA = "https://api.open-meteo.com/v1/forecast?latitude=19.0413&longitude=-98.2062&hourly=temperature_2m,rain&timezone=America%2FMexico_City"

@dlt.resource(
    table_name="lecturas_puebla",
    write_disposition="merge",
    primary_key="fecha_hora"
)

def obtener_clima():
    # ... (El resto de tu código sigue IGUAL, no lo toques) ...
    print("Conectando con la api")
    response = requests.get(URL_CLIMA)
    response.raise_for_status()
    data = response.json()

    hourly = data["hourly"]
    times = hourly["time"]
    temps = hourly["temperature_2m"]
    rains = hourly["rain"]

    print(f"Datos recibidos. Procesando {len(times)} registros.")

    for tiempo, temp, lluvia in zip(times, temps, rains):
        yield {
            "fecha_hora": tiempo,
            "temperatura": temp,
            "lluvia_mm": lluvia,
            "ciudad": "Puebla"
        }


if __name__ == "__main__":
    # Definimos el pipeline
    pipeline = dlt.pipeline(
        pipeline_name="clima_puebla_pipeline",
        destination="postgres",
        dataset_name="datos_meteorologicos"
    )

    # Ejecutamos
    print("Cargando a PostgreSQL")
    # El pipeline leerá automáticamente la variable de entorno que definimos arriba
    info = pipeline.run(obtener_clima())

    print("Carga completada")
    print(info)