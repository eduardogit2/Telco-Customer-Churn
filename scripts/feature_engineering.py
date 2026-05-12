import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

class FeatureEngineering(BaseEstimator, TransformerMixin):
    """
    Transformador personalizado para el dataset Telco Customer Churn.
    Se encarga de estandarizar servicios, corregir tipos de datos ocultos 
    y crear nuevas variables analíticas (Binning).
    """

    def __init__(self, create_tenure_group=True, standardize_services=True):
        self.create_tenure_group = create_tenure_group
        self.standardize_services = standardize_services

    def fit(self, X, y=None):
        # El método fit no hace nada aquí porque no estamos "aprendiendo" 
        # parámetros de los datos (como lo haría un StandardScaler), 
        # solo aplicamos reglas lógicas.
        return self

    def transform(self, X):
        # Siempre trabajamos sobre una copia para evitar Data Leakage y warnings de Pandas
        X = X.copy()
        
        # ---------------------------------------------------------
        # 1. CORRECCIÓN ESTRUCTURAL (TotalCharges)
        # ---------------------------------------------------------
        if 'TotalCharges' in X.columns:
            # Reemplazamos los espacios vacíos tramposos por nulos matemáticos (NaN)
            X['TotalCharges'] = X['TotalCharges'].replace(r'^\s*$', np.nan, regex=True)
            # Forzamos la columna a tipo numérico (float)
            X['TotalCharges'] = pd.to_numeric(X['TotalCharges'], errors='coerce')
            
        # ---------------------------------------------------------
        # 2. ESTANDARIZACIÓN DE SERVICIOS
        # ---------------------------------------------------------
        if self.standardize_services:
            # Convertimos SeniorCitizen de 0/1 a No/Yes para que el ColumnTransformer 
            # lo trate como variable categórica junto con el resto
            if 'SeniorCitizen' in X.columns:
                X['SeniorCitizen'] = X['SeniorCitizen'].map({0: 'No', 1: 'Yes', '0': 'No', '1': 'Yes'}).fillna(X['SeniorCitizen'])

            # Estandarizamos respuestas redundantes a un simple 'No'
            columnas_servicios = [
                'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 
                'TechSupport', 'StreamingTV', 'StreamingMovies'
            ]
            for col in columnas_servicios:
                if col in X.columns:
                    X[col] = X[col].replace('No internet service', 'No')
                    
            if 'MultipleLines' in X.columns:
                X['MultipleLines'] = X['MultipleLines'].replace('No phone service', 'No')

        # ---------------------------------------------------------
        # 3. CREACIÓN DE NUEVAS VARIABLES (BINNING)
        # ---------------------------------------------------------
        if self.create_tenure_group and 'tenure' in X.columns:
            bins = [0, 12, 24, 36, 48, 60, 72]
            labels = ['0-1 año', '1-2 años', '2-3 años', '3-4 años', '4-5 años', '5-6 años']
            
            # Usamos pd.cut para crear los rangos, y lo pasamos a string (texto) 
            # para que scikit-learn lo entienda como una categoría en la siguiente fase
            X['Tenure_Years_Group'] = pd.cut(X['tenure'], bins=bins, labels=labels, include_lowest=True).astype(str)
            X['Tenure_Years_Group'] = X['Tenure_Years_Group'].replace('nan', np.nan)

        return X