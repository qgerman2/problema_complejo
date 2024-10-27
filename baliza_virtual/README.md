## Baliza virtual

**Objetivo**

Enviar datos GPS generados en X-Plane por ESP-NOW

Recibe los datos por serial desde el plugin https://github.com/qgerman2/xplane-HITL

```mermaid
graph LR;
    X-Plane-->HITL-->ESP32;

```