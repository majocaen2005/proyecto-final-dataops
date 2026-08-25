import json
from datetime import datetime

def cargar_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

profile = cargar_json("reports/profile.json")
quality = cargar_json("reports/quality.json")
reconciliation = cargar_json("reports/reconciliation.json")

metrics = {
    "timestamp": datetime.now().isoformat(),
    "pipeline_status": "SUCCESS",
    "total_registros_iniciales": profile["total_registros"],
    "quality_score_percent": quality["quality_score"],
    "registros_basura_descartados": quality["registros_invalidos"],
    "registros_finales_produccion": reconciliation["silver_count"],
    "reconciliacion_aprobada": reconciliation["reconciled"]
}

with open("reports/pipeline_metrics.json", "w", encoding="utf-8") as f:
    json.dump(metrics, f, indent=4, ensure_ascii=False)

print("=" * 60)
print("OBSERVABILIDAD Y MÉTRICAS")
print("=" * 60)

for key, value in metrics.items():
    print(f"{key}: {value}")

print("\n¡Pipeline de DataOps finalizado exitosamente!")