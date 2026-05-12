import pandas as pd
from pymongo import MongoClient
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def cargar_datos_limpios():
    try:
        # Lee el archivo legible que generó limpieza.py
        df = pd.read_csv("data/processed/Telco_Customer_Churn_Clean.csv") 
        data_dict = df.to_dict("records")
        
        client = MongoClient("mongodb://mongo-server:27017/")
        db = client["telco_db"]
        
        # Sube a la colección limpia
        collection = db["Telco_Customer_Churn_Clean"] 
        collection.drop()
        collection.insert_many(data_dict)
    except Exception as e:
        logging.error(f"Error: {e}")

if __name__ == "__main__":
    cargar_datos_limpios()