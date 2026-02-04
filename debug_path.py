import os

print("--- DIAGNÓSTICO DE RUTAS ---")
print(f"1. Directorio de trabajo actual (CWD): {os.getcwd()}")

ruta_carpeta = os.path.join(os.getcwd(), ".dlt")
ruta_archivo = os.path.join(ruta_carpeta, "secrets.toml")

print(f"2. Buscando carpeta en: {ruta_carpeta}")
if os.path.exists(ruta_carpeta):
    print("   ✅ La carpeta .dlt EXISTE.")
else:
    print("   ❌ La carpeta .dlt NO EXISTE aquí.")

print(f"3. Buscando archivo en: {ruta_archivo}")
if os.path.exists(ruta_archivo):
    print("   ✅ El archivo secrets.toml EXISTE.")
    # Vamos a leerlo para ver si tiene algo adentro
    with open(ruta_archivo, "r") as f:
        contenido = f.read()
        if "[destination.postgres]" in contenido:
            print("   ✅ El contenido parece correcto (tiene el header).")
        else:
            print(f"   ⚠️ El archivo existe pero NO encuentro '[destination.postgres]'. Contenido:\n{contenido}")
else:
    print("   ❌ El archivo secrets.toml NO EXISTE (o tiene otro nombre).")