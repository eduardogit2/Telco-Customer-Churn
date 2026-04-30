import pandas as pd
from quality_check import QualityCheck

def evaluar_calidad():
    print("========================================")
    print("🔍 AUDITORÍA DE CALIDAD DE DATOS")
    print("========================================\n")
    
    # 1. Evaluar el archivo crudo
    try:
        df_raw = pd.read_csv("data/raw/02_Base_WA_Fn-UseC_-Telco-Customer-Churn.csv")
        auditor_raw = QualityCheck(df_raw)
        print("reporte datos crudos:")
        print(auditor_raw.quality_report())
    except FileNotFoundError:
        print("Aún no hay datos Ejecuta ingesta.py primero.")

    print("\n----------------------------------------\n")

    # 2. Evaluar el archivo limpio
    try:
        df_clean = pd.read_csv("data/processed/Telco_Customer_Churn_Clean.csv")
        
        
        auditor_clean = QualityCheck(df_clean)
        
        print("reporte datos limpios:")
        print(auditor_clean.quality_report())
    except FileNotFoundError:
        print("Aún no hay datos. Ejecuta limpieza.py primero.")
        
    print("\n========================================")

if __name__ == "__main__":
    evaluar_calidad()