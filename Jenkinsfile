pipeline {
    agent any
    environment {
       
        PYTHON = 'C:\\Users\\majoc\\AppData\\Local\\Programs\\Python\\Python314\\python.exe'
    }
    stages {
        stage('Inicializar Entorno') {
            steps { bat "\"${PYTHON}\" scripts/1_inicializar.py" }
        }
        stage('Extraccion (Raw)') {
            steps { bat "\"${PYTHON}\" scripts/2_extraer.py" }
        }
        stage('Perfilado de Datos') {
            steps { bat "\"${PYTHON}\" scripts/3_perfilar.py" }
        }
        stage('Compuerta de Calidad (Quality Gate)') {
            steps { bat "\"${PYTHON}\" scripts/4_calidad.py" }
        }
        stage('Transformacion y Limpieza (Silver)') {
            steps { bat "\"${PYTHON}\" scripts/5_transformar.py" }
        }
        stage('Reconciliacion de Volumen') {
            steps { bat "\"${PYTHON}\" scripts/6_reconciliar.py" }
        }
        stage('Pase a Produccion (Gold)') {
            steps { bat "\"${PYTHON}\" scripts/7_publicar.py" }
        }
        stage('Observabilidad y Metricas') {
            steps { bat "\"${PYTHON}\" scripts/8_metricas.py" }
        }
    }
    post {
        success {
            echo '======================================================='
            echo 'DATAOPS PIPELINE COMPLETADO - DATOS LISTOS EN GOLD'
            echo '======================================================='
        }
        failure {
            echo '======================================================='
            echo 'ALERTA: EL PIPELINE FALLO. REVISAR LOGS DE QUALITY GATE'
            echo '======================================================='
        }
    }
}