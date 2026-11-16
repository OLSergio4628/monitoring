"""Evaluador de reglas de alerta de referencia. Integrar con Alertmanager/webhook."""
def evaluate(m):
    alerts=[]
    if m["accuracy"] < 0.80: alerts.append(("CRITICAL","VQAAccuracyLow","Activar rollback/cuarentena"))
    if m["p95_latency"] > 1.50: alerts.append(("CRITICAL","VQALatencyHigh","Aplicar mitigación de tráfico"))
    if m["error_rate"] > 0.05: alerts.append(("HIGH","VQAErrorRateHigh","Revisar logs y dependencias"))
    if m["psi"] > 0.25: alerts.append(("HIGH","VQADataDrift","Validar datos y evaluar reentrenamiento"))
    if m["gpu_memory"] > 90: alerts.append(("MEDIUM","GPUCapacityHigh","Escalar capacidad"))
    return alerts

if __name__ == "__main__":
    sample={"accuracy":0.64,"p95_latency":0.42,"error_rate":0.03,"psi":0.31,"gpu_memory":55}
    for severity,name,action in evaluate(sample):
        print(f"[{severity}] {name}: {action}")
