"""
Monitor de referencia para un servicio VQA.
Modo demo: genera métricas sintéticas y permite simular degradación y latencia.
Modo integración: sustituir la fuente sintética por métricas reales del servicio.
"""
import os, time, random, argparse, logging
from datetime import datetime, timezone
from prometheus_client import start_http_server, Gauge, Counter, Histogram

REQUESTS = Counter("vqa_requests_total", "Solicitudes VQA", ["status"])
LATENCY = Histogram("vqa_request_latency_seconds", "Latencia de inferencia",
                    buckets=(.05,.1,.2,.35,.5,.75,1,2,5,10))
ACCURACY = Gauge("vqa_validation_accuracy", "Exactitud en conjunto etiquetado")
ERROR_RATE = Gauge("vqa_error_rate", "Tasa de error")
DRIFT = Gauge("vqa_data_drift_psi", "Population Stability Index")
GPU_MEMORY = Gauge("vqa_gpu_memory_percent", "Uso de memoria GPU (%)")
MODEL_VERSION = Gauge("vqa_model_version_info", "Versión activa del modelo", ["version"])

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("vqa-monitor")

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--port", type=int, default=8000)
    p.add_argument("--scenario", choices=["normal","degraded","slow"], default="normal")
    p.add_argument("--interval", type=float, default=2.0)
    args = p.parse_args()
    start_http_server(args.port)
    MODEL_VERSION.labels(version="vqa-1.0.0").set(1)
    log.info("Exporter Prometheus disponible en :%s/metrics; escenario=%s", args.port, args.scenario)

    while True:
        if args.scenario == "normal":
            latency = random.uniform(.08,.35); accuracy = random.uniform(.88,.94)
            error = random.uniform(.002,.015); drift = random.uniform(.01,.08)
            gpu = random.uniform(25,60); status = "success"
        elif args.scenario == "degraded":
            latency = random.uniform(.10,.40); accuracy = random.uniform(.58,.70)
            error = random.uniform(.02,.06); drift = random.uniform(.22,.38)
            gpu = random.uniform(30,65); status = "success"
        else:  # slow
            latency = random.uniform(2.0,4.5); accuracy = random.uniform(.88,.93)
            error = random.uniform(.03,.08); drift = random.uniform(.02,.09)
            gpu = random.uniform(85,98); status = "timeout" if random.random()<.15 else "success"

        time.sleep(min(latency, 1.0))  # limita la pausa real del demo
        LATENCY.observe(latency)        # registra la latencia simulada completa
        REQUESTS.labels(status=status).inc()
        ACCURACY.set(accuracy); ERROR_RATE.set(error); DRIFT.set(drift); GPU_MEMORY.set(gpu)
        log.info("scenario=%s latency_s=%.3f accuracy=%.3f error_rate=%.3f PSI=%.3f gpu_pct=%.1f",
                 args.scenario, latency, accuracy, error, drift, gpu)
        time.sleep(args.interval)

if __name__ == "__main__":
    main()
