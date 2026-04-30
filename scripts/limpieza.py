import pandas as pd
import numpy as np
import os
import logging

# Configuración de trazabilidad
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def limpiar_y_transformar():
    logging.info("--- INICIANDO LIMPIEZA Y TRANSFORMACIÓN ---")
    
    nombre_archivo = "02_Base_WA_Fn-UseC_-Telco-Customer-Churn.csv"
    ruta_raw = f"data/raw/{nombre_archivo}"
    ruta_processed = "data/processed/Telco_Customer_Churn_Clean.csv"
    
    if not os.path.exists(ruta_raw):
        logging.error(f"Error: No se encontró el archivo crudo en {ruta_raw}")
        return

    try:
        df = pd.read_csv(ruta_raw)
        logging.info(f"Dataset cargado. Filas originales: {len(df)}")
        
        # ==========================================
        # FASE 1: LIMPIEZA GLOBAL GENÉRICA
        # ==========================================
        df = df.replace(r'^\s*$', np.nan, regex=True)
        df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
        logging.info("Fase 1: Espacios vacíos convertidos a NaN y TotalCharges forzado a numérico.")
        
        # ==========================================
        # FASE 2: TRANSFORMACIONES DEL NEGOCIO
        # ==========================================
        df['SeniorCitizen'] = df['SeniorCitizen'].map({0: 'No', 1: 'Yes'})
        
        columnas_servicios = ['OnlineSecurity', 'StreamingTV', 'StreamingMovies']
        for col in columnas_servicios:
            df[col] = df[col].replace('No internet service', 'No')
            
        df['MultipleLines'] = df['MultipleLines'].replace('No phone service', 'No')
        
        bins = [0, 12, 24, 36, 48, 60, 72]
        labels = ['0-1 año', '1-2 años', '2-3 años', '3-4 años', '4-5 años', '5-6 años']
        df['Tenure_Years_Group'] = pd.cut(df['tenure'], bins=bins, labels=labels, include_lowest=True)
        logging.info("Fase 2: Estandarización y creación de 'Tenure_Years_Group' completada.")

        # ==========================================
        # FASE 3: SELECCIÓN DE CARACTERÍSTICAS
        # ==========================================
        columnas_a_eliminar = [
            'gender', 'Partner', 'Dependents', 'PaperlessBilling'
        ]
        df = df.drop(columns=columnas_a_eliminar)
        logging.info(f"Fase 3: Se eliminaron {len(columnas_a_eliminar)} columnas por baja relevancia.")

        # ==========================================
        # FASE 4: TRATAMIENTO DE NULOS Y DUPLICADOS
        # ==========================================
        # 4.1 Reparación de Nulos lógicos (Clientes nuevos sin cobros)
        nulos_reparables = df['TotalCharges'].isnull().sum()
        df['TotalCharges'] = df['TotalCharges'].fillna(0)
        logging.info(f"Fase 4: Se repararon {nulos_reparables} nulos en TotalCharges cambiándolos por 0 (clientes nuevos).")

        # 4.2 Eliminación de Nulos IRREPARABLES (Si es que quedó alguno en el resto de la tabla)
        nulos_restantes = df.isnull().sum().sum()
        if nulos_restantes > 0:
            df = df.dropna()
            logging.info(f"Fase 4: Se eliminaron {nulos_restantes} registros con nulos irreparables.")
            
        # 4.3 Duplicados
        duplicados = df.duplicated(subset=['customerID']).sum()
        if duplicados > 0:
            df = df.drop_duplicates(subset=['customerID'], keep='last')
            logging.info(f"Fase 4: Se eliminaron {duplicados} registros duplicados según customerID.")
        else:
            logging.info("Fase 4: No se encontraron IDs duplicados.")
            
        # ==========================================
        # FASE 5: EXPORTAR RESULTADO
        # ==========================================
        os.makedirs(os.path.dirname(ruta_processed), exist_ok=True)
        df.to_csv(ruta_processed, index=False)
        
        logging.info(f"¡Éxito! Dataset procesado guardado en {ruta_processed}")
        logging.info(f"Filas finales: {len(df)}. Columnas finales: {len(df.columns)}")
        
    except Exception as e:
        logging.error(f"Error inesperado durante la ejecución: {e}")

if __name__ == "__main__":
    limpiar_y_transformar()