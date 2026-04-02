# Predicción de Abandono de Clientes (Customer Churn)

Este proyecto tiene como objetivo anticipar, mediante un modelo de Machine Learning, si un cliente de la compañía de telecomunicaciones abandonará el servicio en el corto plazo. Utiliza variables clave como el historial de facturación, el tipo de contrato y los servicios adicionales contratados.

---

## Componentes del sistema

- **Scripts de procesamiento**: módulos en Python para la ingesta, limpieza (ETL) y transformación de datos al español.
- **Base de datos NoSQL (MongoDB)**: para el almacenamiento dinámico y estructurado de los perfiles de los clientes.
- **Modelo de IA (Machine Learning)**: algoritmo de clasificación binaria para predecir la probabilidad de abandono (Churn).
- **Infraestructura y Despliegue**: entorno aislado con Docker, automatización con GitHub Actions y hosting en Render.
- **Documentación**: planificación PMBOK y diseño técnico completo de la arquitectura híbrida.

---

## Tecnologías utilizadas

- Python 3 
- Pandas / Scikit-learn 
- MongoDB (Base de datos NoSQL)
- Docker (Contenerización)
- GitHub Actions (Integración y despliegue continuo - CI/CD)
- Render (Plataforma de despliegue Cloud)
- Git / GitHub (Control de versiones)

---

## Pipeline implementado

| Etapa | Descripción |
|-------|-------------|
| 1. Configuración | Setup del entorno en Codespaces, definición de arquitectura base. |
| 2. Ingesta | Lectura del dataset crudo (`Telco-Customer-Churn.csv`) mediante Python. |
| 3. Limpieza y Transformación | Tratamiento de nulos, eliminación de variables irrelevantes y estandarización de columnas/valores a formato `snake_case` en español. |
| 4. Carga en MongoDB | Inyección de los perfiles de clientes limpios como documentos en la base de datos NoSQL. |
| 5. Entrenamiento IA | Modelado de clasificación binaria para la variable objetivo `churn`, excluyendo el `customerID` del entrenamiento. |
| 6. Validación (CI/CD) | Revisión de métricas (accuracy, recall) y ejecución de pruebas automáticas en GitHub Actions. |
| 7. Despliegue Cloud | Empaquetado en contenedor Docker y despliegue del servicio backend en Render. |

---

## 📂 Estructura del repositorio

```text
Telco-Customer-Churn/
├── README.md
├── docs/
│   ├── Planificacion_Proyecto_Grupo_7.pdf
│   └── Documento_Diseno_Tecnico_Grupo_7.pdf
├── scripts/
│   ├── ingesta.py
│   ├── limpieza.py
│   ├── transformacion.py
│   └── entrenamiento.py
├── data/
│   └── 01_Metadata.txt
│   └── 02_Base_WA_Fn-UseC_-Telco-Customer-Churn.csv
├── .github/
│   └── workflows/
│       └── main.yml
├── docker-compose.yml
├── requirements.txt
└── .env.example
```

---

## Cómo ejecutar el sistema (entorno ya instalado)

1. Clonar el repositorio  
   `git clone https://github.com/usuario/agotamiento-stock.git`

2. Entrar a la carpeta del proyecto  
   `cd agotamiento-stock`

3. Ejecutar el pipeline manualmente por etapas  
   Ejemplo:  
   `python scripts/ingesta.py`  
   `python scripts/limpieza.py`  
   `python scripts/entrenamiento.py`

4. Visualizar los resultados y métricas desde consola o dashboard

---

## Documentación técnica

El documento de diseño técnico está disponible en:  
[`docs/Documento_Diseno_Tecnico_Grupo_7.pdf`]

---

## Equipo

- Integrante 1 – Procesamiento y limpieza  
- Integrante 2 – Modelado y entrenamiento  
- Integrante 3 – Visualización y documentación
