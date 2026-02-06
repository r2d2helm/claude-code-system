# 📊 /pve-monitor - Monitoring & Métriques

## Description
Configuration du monitoring et collecte de métriques Proxmox VE 9+.

## Syntaxe
```
/pve-monitor [action] [options]
```

## Métriques Intégrées PVE 9

### Configuration InfluxDB
```bash
# /etc/pve/status.cfg
cat > /etc/pve/status.cfg << 'EOF'
influxdb: influx1
    server 10.0.0.50
    port 8086
    bucket proxmox
    organization myorg
    token YOUR_INFLUXDB_TOKEN
    influxdbproto https
EOF

# Vérifier
pvesh get /cluster/metrics/server
```

### Configuration Graphite
```bash
# /etc/pve/status.cfg
cat >> /etc/pve/status.cfg << 'EOF'

graphite: graphite1
    server 10.0.0.51
    port 2003
    path proxmox
EOF
```

## Prometheus Exporter

### Installation PVE Exporter (Docker)
```bash
# Sur node monitoring
docker run -d \
  --name pve-exporter \
  --restart unless-stopped \
  -p 9221:9221 \
  -e PVE_USER="monitoring@pve" \
  -e PVE_TOKEN_NAME="prometheus" \
  -e PVE_TOKEN_VALUE="xxxxx-xxxx-xxxx" \
  -e PVE_VERIFY_SSL="false" \
  prompve/prometheus-pve-exporter

# Test
curl http://localhost:9221/pve?target=192.168.1.10
```

### Installation PVE Exporter (Native)
```bash
# Sur chaque node PVE
apt install prometheus-pve-exporter -y

# Configuration
cat > /etc/prometheus/pve.yml << 'EOF'
default:
  user: monitoring@pve!prometheus
  token_value: "xxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
  verify_ssl: false
EOF

chmod 600 /etc/prometheus/pve.yml

# Service
systemctl enable --now prometheus-pve-exporter
```

### Prometheus scrape config
```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'proxmox'
    static_configs:
      - targets:
        - 192.168.1.10  # pve1
        - 192.168.1.11  # pve2
        - 192.168.1.12  # pve3
    metrics_path: /pve
    params:
      module: [default]
    relabel_configs:
      - source_labels: [__address__]
        target_label: __param_target
      - source_labels: [__param_target]
        target_label: instance
      - target_label: __address__
        replacement: pve-exporter:9221
```

## Grafana Dashboards

### Dashboards recommandés
| ID | Nom | Type |
|----|-----|------|
| 10347 | Proxmox VE Prometheus | Prometheus |
| 15356 | Proxmox VE Cluster | InfluxDB |
| 10048 | Proxmox Cluster | InfluxDB 2.x |
| 11664 | Proxmox VE | Prometheus |

### Import dashboard
```bash
# Via Grafana API
curl -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {api_key}" \
  -d '{"dashboard":{"id":null,"title":"Proxmox","import":{"gnetId":10347}}}' \
  http://grafana:3000/api/dashboards/import
```

## Alerting

### Alertmanager avec Prometheus
```yaml
# alertmanager.yml
global:
  smtp_smarthost: 'smtp.example.com:587'
  smtp_from: 'alertmanager@example.com'
  smtp_auth_username: 'alertmanager'
  smtp_auth_password: 'secret'

route:
  receiver: 'email-admin'
  group_by: ['alertname', 'instance']
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 3h

receivers:
  - name: 'email-admin'
    email_configs:
      - to: 'admin@example.com'
```

### Règles d'alerte Prometheus
```yaml
# proxmox_alerts.yml
groups:
  - name: proxmox
    rules:
      - alert: PVE_NodeDown
        expr: up{job="proxmox"} == 0
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "Proxmox node {{ $labels.instance }} is down"

      - alert: PVE_HighCPU
        expr: pve_cpu_usage_ratio > 0.9
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High CPU on {{ $labels.instance }}"

      - alert: PVE_HighMemory
        expr: (pve_memory_usage_bytes / pve_memory_size_bytes) > 0.9
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High memory on {{ $labels.instance }}"

      - alert: PVE_StorageFull
        expr: (pve_storage_usage_bytes / pve_storage_size_bytes) > 0.85
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Storage {{ $labels.storage }} nearly full"

      - alert: PVE_VMStopped
        expr: pve_guest_info{status="stopped"} == 1
        for: 10m
        labels:
          severity: info
        annotations:
          summary: "VM {{ $labels.name }} is stopped"

      - alert: Ceph_HealthWarn
        expr: ceph_health_status == 1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Ceph cluster health warning"

      - alert: Ceph_HealthCritical
        expr: ceph_health_status == 2
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Ceph cluster health critical"
```

## Monitoring SMART Disques

### Configurer smartmontools
```bash
# Installer
apt install smartmontools -y

# Configuration
cat > /etc/smartd.conf << 'EOF'
DEVICESCAN -a -o on -S on -n standby,q -s (S/../.././02|L/../../6/03) -W 4,35,45 -m admin@example.com -M exec /usr/share/smartmontools/smartd-runner
EOF

# Activer
systemctl enable --now smartd
```

### Script check SMART
```bash
#!/bin/bash
# /usr/local/bin/check-smart.sh

for disk in /dev/sd?; do
    HEALTH=$(smartctl -H $disk 2>/dev/null | grep -i "overall" | awk '{print $NF}')
    TEMP=$(smartctl -A $disk 2>/dev/null | grep -i temperature | head -1 | awk '{print $10}')
    
    echo "Disk: $disk - Health: $HEALTH - Temp: ${TEMP}°C"
    
    if [ "$HEALTH" != "PASSED" ]; then
        echo "ALERT: $disk health check failed!"
        # Envoyer alerte
    fi
    
    if [ "$TEMP" -gt 50 ]; then
        echo "ALERT: $disk temperature too high!"
    fi
done
```

## Node Exporter (métriques système)

### Installation
```bash
# Sur chaque node
apt install prometheus-node-exporter -y

# Activer
systemctl enable --now prometheus-node-exporter

# Test
curl http://localhost:9100/metrics
```

### Prometheus config
```yaml
scrape_configs:
  - job_name: 'node'
    static_configs:
      - targets:
        - 192.168.1.10:9100
        - 192.168.1.11:9100
        - 192.168.1.12:9100
```

## Monitoring Ceph

### Activer Prometheus module Ceph
```bash
ceph mgr module enable prometheus

# Endpoint
curl http://{ceph_mgr}:9283/metrics
```

### Prometheus scrape Ceph
```yaml
scrape_configs:
  - job_name: 'ceph'
    static_configs:
      - targets:
        - 192.168.1.10:9283
        - 192.168.1.11:9283
```

## Métriques Disponibles

### PVE Exporter
| Métrique | Description |
|----------|-------------|
| `pve_up` | Node disponible |
| `pve_cpu_usage_ratio` | Usage CPU |
| `pve_memory_usage_bytes` | RAM utilisée |
| `pve_storage_usage_bytes` | Stockage utilisé |
| `pve_guest_info` | Info VMs/CTs |
| `pve_node_info` | Info node |

### Node Exporter
| Métrique | Description |
|----------|-------------|
| `node_cpu_seconds_total` | CPU détaillé |
| `node_memory_*` | RAM détaillée |
| `node_disk_*` | I/O disques |
| `node_network_*` | Trafic réseau |
| `node_filesystem_*` | Filesystems |

## Stack Monitoring Complète

### Docker Compose
```yaml
# docker-compose.yml
version: '3.8'

services:
  prometheus:
    image: prom/prometheus:latest
    volumes:
      - ./prometheus:/etc/prometheus
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.retention.time=30d'
    ports:
      - "9090:9090"

  grafana:
    image: grafana/grafana:latest
    volumes:
      - grafana_data:/var/lib/grafana
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    ports:
      - "3000:3000"

  alertmanager:
    image: prom/alertmanager:latest
    volumes:
      - ./alertmanager:/etc/alertmanager
    ports:
      - "9093:9093"

  pve-exporter:
    image: prompve/prometheus-pve-exporter:latest
    environment:
      - PVE_USER=monitoring@pve
      - PVE_TOKEN_NAME=prometheus
      - PVE_TOKEN_VALUE=${PVE_TOKEN}
      - PVE_VERIFY_SSL=false
    ports:
      - "9221:9221"

volumes:
  prometheus_data:
  grafana_data:
```

## Best Practices

1. **Rétention** : 30 jours minimum, 90 jours recommandé
2. **Scrape interval** : 15s pour PVE, 60s pour SMART
3. **Alerting** : Définir seuils réalistes
4. **Dashboards** : Un par rôle (cluster, storage, VMs)
5. **Séparation** : Monitoring sur node dédié ou externe
