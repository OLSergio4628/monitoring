# Paquete de observabilidad VQA

## Contenido
- scripts/: exporter de métricas, PSI y evaluador de alertas.
- config/: configuración de Prometheus y reglas de alertas.
- docker-compose.yml: arranque básico de Prometheus y Grafana.
- evidencia/: gráficas sintéticas de dos incidentes.

## Ejecución rápida
1. Instalar dependencias: `pip install prometheus-client numpy mlflow`
2. Ejecutar monitor: `python scripts/monitor_vqa.py --scenario normal`
3. Simular degradación: `python scripts/monitor_vqa.py --scenario degraded`
4. Simular latencia: `python scripts/monitor_vqa.py --scenario slow`
5. En otra terminal: `docker compose up -d`
6. Prometheus: http://localhost:9090 ; Grafana: http://localhost:3000

## Advertencia de evidencia
El monitor genera telemetría sintética para probar la lógica. No representa un servicio productivo real.
Para evidencia de implementación real, conectar las métricas al endpoint VQA, desplegar Prometheus/Grafana,
configurar los dashboards y exportar capturas con fecha/hora. Añadir MLflow Tracking a la rutina de evaluación.
