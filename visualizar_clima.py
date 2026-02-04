import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv


load_dotenv()

# Recuperamos las variables de forma segura
db_pass = os.getenv("DB_PASSWORD")
db_user = os.getenv("DB_USER")
db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")

# Verificamos que no estén vacías
if not db_pass:
    raise ValueError("archivo sin contraseña .env!")

# CONEXIÓN (Usando f-strings para insertar las variables)
print("🔌 Conectando a la Base de Datos de forma segura...")
connection_string = f"postgresql://{db_user}:{db_pass}@{db_host}:5432/{db_name}"
engine = create_engine(connection_string)

# ADQUISICIÓN
query = """
SELECT 
    fecha_hora,
    temperatura,
    lluvia_mm
FROM datos_meteorologicos.lecturas_puebla
ORDER BY fecha_hora ASC;
"""


df = pd.read_sql(query, engine)

print(f"Datos cargados: {len(df)} registros.")

# PROCESAMIENTO
# Convertimos la columna de texto a formato de Tiempo real de Python
df['fecha_hora'] = pd.to_datetime(df['fecha_hora'])

# VISUALIZACIÓN
plt.figure(figsize=(12, 6)) # Tamaño de la pantalla


plt.plot(df['fecha_hora'], df['temperatura'],
         label='Temperatura (°C)', color='tab:red', linewidth=2)


plt.title('Monitor de Temperatura - Puebla (Desde PostgreSQL)')
plt.xlabel('Tiempo')
plt.ylabel('Amplitud (°C)')
plt.grid(True, linestyle='--', alpha=0.7) # La rejilla de fondo
plt.legend()
plt.xticks(rotation=45) # Rotar fechas para leerlas bien

# Ajuste automático para que no se corten los textos
plt.tight_layout()


plt.show()