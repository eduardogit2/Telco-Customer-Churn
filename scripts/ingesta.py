import pandas as pd
import os
import logging
from pymongo import MongoClient

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def obtener_coleccion():
    MONGO_URI = "mongodb://mongo-server:27017/" 
    try:
        cliente = MongoClient(MONGO_URI)
        db = cliente['telco_db']
        coleccion = db['clientes_telco_raw']
        return coleccion
    except Exception as e:
        logging.error(f"Error al conectar con MongoDB: {e}")
        return None

def ingestar_datos():
    logging.info("Iniciando pipeline de ingesta...")
    nombre_archivo = "02_Base_WA_Fn-UseC_-Telco-Customer-Churn.csv"
    ruta_origen = f"data/{nombre_archivo}"
    ruta_destino_raw = f"data/raw/{nombre_archivo}"
    
    if not os.path.exists(ruta_origen):
        logging.error(f"Error: No se encontró el archivo en {ruta_origen}")
        return

    try:
        os.makedirs(os.path.dirname(ruta_destino_raw), exist_ok=True)
        df_sucio = pd.read_csv(ruta_origen)
        logging.info(f"Archivo extraído de origen. Total de registros: {len(df_sucio)}")
        df_sucio.to_csv(ruta_destino_raw, index=False)
        logging.info(f"Copia de seguridad (raw) creada exitosamente en {ruta_destino_raw}")
        coleccion = obtener_coleccion()
        
        if coleccion is not None:
            registros_json = df_sucio.to_dict(orient='records')
            
            coleccion.delete_many({}) 
            coleccion.insert_many(registros_json)
            
            logging.info("¡Éxito! Los datos crudos se insertaron correctamente en la base de datos.")
        else:
            logging.error("El CSV se guardó en raw, pero falló la conexión a MongoDB.")
            
    except Exception as e:
        logging.error(f"Error inesperado durante la ejecución: {e}")

if __name__ == "__main__":
    ingestar_datos()