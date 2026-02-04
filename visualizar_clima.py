import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv # <--- Importamos esto

# 1. CARGAR SECRETOS
# Esto busca el archivo .env y carga las variables en memoria
load_dotenv()

# Recuperamos las variables de forma segura
db_pass = os.getenv("DB_PASSWORD")
db_user = os.getenv("DB_USER")
db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")

# Verificamos que no estén vacías (buena práctica)
if not db_pass:
    raise ValueError("¡No encontré la contraseña en el archivo .env!")

# 2. CONEXIÓN (Usando f-strings para insertar las variables)
print("🔌 Conectando a la Base de Datos de forma segura...")
connection_string = f"postgresql://{db_user}:{db_pass}@{db_host}:5432/{db_name}"
engine = create_engine(connection_string)

# 3. LA ADQUISICIÓN (El resto sigue igual)
query = """
SELECT 
    fecha_hora,
    temperatura,
    lluvia_mm
FROM datos_meteorologicos.lecturas_puebla
ORDER BY fecha_hora ASC;
"""

# Pandas ejecuta el SQL y guarda el resultado en la variable 'df'
df = pd.read_sql(query, engine)

print(f"✅ Datos cargados: {len(df)} registros.")

# 3. EL PROCESAMIENTO (Ajuste de ejes)
# Convertimos la columna de texto a formato de Tiempo real de Python
df['fecha_hora'] = pd.to_datetime(df['fecha_hora'])

# 4. LA VISUALIZACIÓN (El Osciloscopio)
plt.figure(figsize=(12, 6)) # Tamaño de la pantalla

# Canal 1: Temperatura (Rojo)
plt.plot(df['fecha_hora'], df['temperatura'],
         label='Temperatura (°C)', color='tab:red', linewidth=2)

# Configuración de la "Pantalla"
plt.title('Monitor de Temperatura - Puebla (Desde PostgreSQL)')
plt.xlabel('Tiempo')
plt.ylabel('Amplitud (°C)')
plt.grid(True, linestyle='--', alpha=0.7) # La rejilla de fondo
plt.legend()
plt.xticks(rotation=45) # Rotar fechas para leerlas bien

# Ajuste automático para que no se corten los textos
plt.tight_layout()

print("📊 Generando gráfica...")
plt.show()