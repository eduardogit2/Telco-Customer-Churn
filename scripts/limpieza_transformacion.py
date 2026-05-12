import pandas as pd
import numpy as np
import logging
import os

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer

# Importamos las clases personalizadas
from feature_engineering import FeatureEngineering
from correlation_filter import CorrelationFilter
from winsorizer import Winsorizer

# Configuración de logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def tratar_duplicados(X: pd.DataFrame, drop=True):
    X = X.copy()
    if drop:
        # Validamos usando nuestra Llave Primaria (customerID)
        if 'customerID' in X.columns:
            X = X.drop_duplicates(subset=['customerID'], keep='last')
        else:
            X = X.drop_duplicates()
            
    # El customerID no es predictivo, así que lo borramos antes de entrenar
    if 'customerID' in X.columns:
        X = X.drop(columns=['customerID'])
        
    return X

if __name__ == "__main__":
    logging.info("--- INICIANDO DATA REFINERY PIPELINE (TELCO CHURN) ---")
    
    # 1. CARGA DE DATOS CRUDOS
    ruta_archivo = "data/raw/02_Base_WA_Fn-UseC_-Telco-Customer-Churn.csv"
    if not os.path.exists(ruta_archivo):
        logging.error("No se encontró el dataset crudo.")
        exit()
        
    data_for_preparation = pd.read_csv(ruta_archivo)
    logging.info(f"Datos originales cargados. Filas: {len(data_for_preparation)}")

    # ==========================================
    # EL PUNTO DE PARTIDA: AISLAR EL TARGET
    # ==========================================
    target = "Churn"
    
    # IMPORTANTE: Eliminamos duplicados ANTES de separar X e Y para evitar desfases en el algoritmo
    # Esto soluciona un bug clásico donde la 'Y' no se reduce si la 'X' elimina filas
    data_for_preparation = data_for_preparation.drop_duplicates(subset=['customerID'], keep='last')
    
    # Separación
    X = data_for_preparation.drop(columns=[target], errors="ignore")
    # Convertimos la variable objetivo a binario (Algoritmos no entienden 'Yes'/'No')
    y = data_for_preparation[target].map({'No': 0, 'Yes': 1})

    # ==========================================
    # ENRUTAMIENTO OBLIGATORIO (Variables Útiles)
    # ==========================================
    # Columnas Numéricas (para Winsorizer y StandardScaler)
    num_cols = ["tenure", "MonthlyCharges", "TotalCharges"]
    
    # Columnas Categóricas (para Imputer y OneHotEncoder)
    # Nota: Aquí SÍ agregamos 'Tenure_Years_Group' porque fue creada en Feature Engineering
    cat_cols = [
        "SeniorCitizen", "PhoneService", "MultipleLines", 
        "InternetService", "OnlineSecurity", "StreamingTV", 
        "StreamingMovies", "Contract", "Tenure_Years_Group"
    ]
    # Las 8 columnas descartadas NO están en estas listas, por ende, el sistema las destruirá.

    # Configuración del Transformador de Columnas
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", Pipeline([
                ("winsorizer", Winsorizer(limits=(0.01, 0.01))), # Tratamiento atípicos suave
                ("imputer", SimpleImputer(strategy="mean")),
                ("scaler", StandardScaler())
            ]), num_cols),

            ("cat", Pipeline([
                ("imputer", SimpleImputer(strategy="most_frequent")),
                # OneHotEncoder transforma las categorías en columnas de 0 y 1
                ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
            ]), cat_cols)
        ],
        remainder='drop' # Aquí se eliminan las variables "peso innecesario"
    )

    # ==========================================
    # ENSAMBLAJE DEL PIPELINE PRINCIPAL
    # ==========================================
    fe = FeatureEngineering(create_tenure_group=True, standardize_services=True)

    pipeline_preparacion = Pipeline(steps=[
        ("duplicados", FunctionTransformer(tratar_duplicados, kw_args={"drop": False})), # Ya se hizo arriba seguro
        ("feature_engineering", fe),
        ("preprocesador", preprocessor),
        ("colinealidad", CorrelationFilter(threshold=0.85)) # Eliminará si dos columnas se parecen más del 85%
    ])

    # ==========================================
    # ENTRENAMIENTO Y EJECUCIÓN (FIT & TRANSFORM)
    # ==========================================
    logging.info("Ejecutando Pipeline (Transformando, Escalando, y Filtrando Colinealidad)...")
    
    X_transformada = pipeline_preparacion.fit_transform(X)

    # Rescatar los nombres de las columnas que sobrevivieron al filtro
    try:
        feature_names = pipeline_preparacion.named_steps["preprocesador"].get_feature_names_out()
        pipeline_preparacion.named_steps["colinealidad"].set_feature_names(feature_names)
        cols_finales = pipeline_preparacion.named_steps["colinealidad"].features_
        nombres_finales = feature_names[cols_finales]
    except Exception as e:
        logging.warning("No se pudieron extraer los nombres de columnas. Usando genéricos.")
        nombres_finales = [f"feature_{i}" for i in range(X_transformada.shape[1])]

    logging.info(f"Transformación exitosa. Quedan {len(nombres_finales)} variables super-predictoras.")
    
    # ==========================================
    # GUARDAR DATOS PREPARADOS PARA EL MODELO
    # ==========================================
    df_modelo = pd.DataFrame(X_transformada, columns=nombres_finales)
    df_modelo['TARGET_Churn'] = y.reset_index(drop=True)
    
    os.makedirs("data/processed", exist_ok=True)
    ruta_salida = "data/processed/Telco_Customer_Churn_Clean.csv"
    df_modelo.to_csv(ruta_salida, index=False)
    
    logging.info(f"¡Data lista para Random Forest guardada en {ruta_salida}!")