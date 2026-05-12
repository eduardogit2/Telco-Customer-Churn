import pandas as pd
from quality_check import QualityCheck

def evaluar_calidad():
    print("========================================")
    print("🔍 AUDITORÍA DE CALIDAD DE DATOS")
    print("========================================\n")
    
    # 1. Evaluar el archivo RAW (Crudo)
    try:
        df_raw = pd.read_csv("data/raw/02_Base_WA_Fn-UseC_-Telco-Customer-Churn.csv")
        auditor_raw = QualityCheck(df_raw)
        print("📄 REPORTE DE ZONA RAW (DATOS CRUDOS):")
        print(auditor_raw.quality_report())
    except FileNotFoundError:
        print("Aún no hay datos en la zona RAW.")

    print("\n----------------------------------------\n")

    # 2. Evaluar el archivo PROCESSED (Limpio)
    try:
        df_clean = pd.read_csv("data/processed/Telco_Customer_Churn_Clean.csv")
        
        # Parametrización: Le decimos al código de la profe que ignore estas columnas 
        # al buscar inconsistencias, porque es normal que los cobros varíen mucho.
        columnas_a_ignorar = ['TotalCharges', 'MonthlyCharges']
        
        auditor_clean = QualityCheck(df_clean, exclude_inconsistencies=columnas_a_ignorar)
        
        print("✨ REPORTE DE ZONA PROCESSED (DATOS LIMPIOS):")
        print(auditor_clean.quality_report())
    except FileNotFoundError:
        print("Aún no hay datos en la zona PROCESSED. Ejecuta limpieza.py primero.")
        
    print("\n========================================")

if __name__ == "__main__":
    evaluar_calidad()