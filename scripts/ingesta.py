import pandas as pd
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def ingestar_con_pandas():
    logging.info("Iniciando ingesta de datos")
    
    nombre_archivo = "02_Base_WA_Fn-UseC_-Telco-Customer-Churn.csv"
    origen = f"data/{nombre_archivo}"
    destino = f"data/raw/{nombre_archivo}"
    
    os.makedirs(os.path.dirname(destino), exist_ok=True)

    try:
        df = pd.read_csv(origen)
        logging.info("Datos cargados correctamente en memoria.")
        
        df.to_csv(destino, index=False)
        logging.info(f"Éxito: Archivo exportado y guardado en {destino}")
        
    except FileNotFoundError:
        logging.error(f"Fallo en la ingesta: No se encontró el archivo en {origen}")
    except Exception as e:
        logging.error(f"Error inesperado: {e}")

if __name__ == "__main__":
    ingestar_con_pandas()