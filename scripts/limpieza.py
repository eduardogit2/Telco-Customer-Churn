import pandas as pd
import numpy as np
import os
import logging

# ¡AQUÍ IMPORTAMOS LAS HERRAMIENTAS DE LA PROFE!
from winsorizer import Winsorizer
from feature_engineering import FeatureEngineering

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def limpiar_datos():
    logging.info("--- INICIANDO LIMPIEZA CON HERRAMIENTAS DE LA PROFE ---")
    ruta_origen = "data/raw/02_Base_WA_Fn-UseC_-Telco-Customer-Churn.csv"
    ruta_destino = "data/processed/Telco_Customer_Churn_Clean.csv"

    try:
        df = pd.read_csv(ruta_origen)
        
        # 1. ARREGLAR NULOS OCULTOS Y ESTANDARIZAR TEXTOS
        df['TotalCharges'] = df['TotalCharges'].replace(r'^\s*$', np.nan, regex=True)
        df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
        
        df['SeniorCitizen'] = df['SeniorCitizen'].map({0: 'No', 1: 'Yes'})
        
        servicios = ['OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 
                     'TechSupport', 'StreamingTV', 'StreamingMovies']
        for col in servicios:
            if col in df.columns:
                df[col] = df[col].replace('No internet service', 'No')
                
        if 'MultipleLines' in df.columns:
            df['MultipleLines'] = df['MultipleLines'].replace('No phone service', 'No')

        # 2. ELIMINAR NULOS Y DUPLICADOS ANTES DE TRANSFORMAR
        df = df.dropna()
        df = df.drop_duplicates(subset=['customerID'], keep='last')

        # 3. USAR EL WINSORIZER DE LA PROFE (Para los atípicos)
        # Instanciamos la clase que ella creó
        tratador_atipicos = Winsorizer(limits=(0.01, 0.01))
        
        # Le decimos qué columnas tratar
        cols_numericas = ['tenure', 'MonthlyCharges', 'TotalCharges']
        df_numerico = df[cols_numericas].copy()
        
        # El Winsorizer de la profe requiere un fit y un transform
        tratador_atipicos.fit(df_numerico)
        df[cols_numericas] = tratador_atipicos.transform(df_numerico)

        # 4. USAR EL FEATURE ENGINEERING (Para los grupos de años)
        # Asumiendo que adaptaste este archivo como lo hicimos antes
        ingeniero_caracteristicas = FeatureEngineering(create_tenure_group=True, standardize_services=False)
        df = ingeniero_caracteristicas.transform(df)

        # 5. GUARDAR RESULTADO
        os.makedirs(os.path.dirname(ruta_destino), exist_ok=True)
        df.to_csv(ruta_destino, index=False)
        logging.info(f"Limpieza finalizada. Datos procesados guardados en {ruta_destino}")

    except Exception as e:
        logging.error(f"Error en la limpieza: {e}")

if __name__ == "__main__":
    limpiar_datos()