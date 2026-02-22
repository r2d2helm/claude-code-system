"""Probes de monitoring systeme pour Heartbeat Phase 2.

Chaque probe retourne un dict standardise:
  {"status": "ok"|"warning"|"critical"|"error", "data": {...}, "message": str}

Design fail-open: chaque probe est wrappee en try/except.
Toutes les operations sont READ-ONLY (aucune modification systeme).

Inspire du Second Brain (Dynamous Community), adapte pour sysadmin Linux.
"""

import os
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Optional

from lib.paths import CONFIG_DIR


# ============================================================
# Configuration
# ============================================================

def _load_heartbeat_config() -> dict:
    """Charge la section heartbeat de memory_v2.yaml."""
    defaults = {
        "disk_warning_percent": 80,
        "disk_critical_percent": 95,
        "disk_mountpoints": [],
        "docker_restart_threshold": 5,
        "critical_services": ["ssh", "docker", "ufw"],
        "check_apt_updates": True,
        "log_lines_to_check": 100,
        "log_error_patterns": ["error", "failed", "critical", "out of memory", "segfault"],
        "memory_importance": 5.0,
        "memory_importance_critical": 8.0,
    }
    try:
        config_path = CONFIG_DIR / "memory_v2.yaml"
        if config_path.exists():
            import yaml
            raw = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
            hb = raw.get("heartbeat", {})
            if isinstance(hb, dict):
                defaults.update(hb)
    except Exception as e:
        import logging
        logging.warning("heartbeat_checks: config load failed, using defaults: %s", e)
    return defaults


_CONFIG = None


def _get_config() -> dict:
    global _CONFIG
    if _CONFIG is None:
        _CONFIG = _load_heartbeat_config()
    return _CONFIG


# ============================================================
# Probe: Disk Usage
# ============================================================

def check_disk() -> dict:
    """Verifie l'utilisation disque par point de montage.

    Retourne les montages depassant le seuil d'avertissement.
    Utilise shutil.disk_usage (pas de subprocess).
    """
    try:
        config = _get_config()
        warning_pct = config.get("disk_warning_percent", 80)
        critical_pct = config.get("disk_critical_percent", 95)
        mountpoints = config.get("disk_mountpoints", [])

        if not mountpoints:
            mountpoints = ["/"]
            # Auto-detect /home si separe
            if os.path.ismount("/home"):
                mountpoints.append("/home")

        results = []
        overall_status = "ok"

        for mp in mountpoints:
            try:
                usage = shutil.disk_usage(mp)
                pct = (usage.used / usage.total) * 100 if usage.total > 0 else 0
                free_gb = usage.free / (1024 ** 3)

                entry = {
                    "mountpoint": mp,
                    "usage_percent": round(pct, 1),
                    "free_gb": round(free_gb, 1),
                    "total_gb": round(usage.total / (1024 ** 3), 1),
                }

                if pct >= critical_pct:
                    entry["level"] = "critical"
                    overall_status = "critical"
                elif pct >= warning_pct:
                    entry["level"] = "warning"
                    if overall_status != "critical":
                        overall_status = "warning"
                else:
                    entry["level"] = "ok"

                results.append(entry)
            except (OSError, PermissionError):
                results.append({"mountpoint": mp, "level": "error", "message": "inaccessible"})

        alerts = [r for r in results if r.get("level") in ("warning", "critical")]
        if alerts:
            msg = "; ".join(
                f"{a['mountpoint']} {a.get('usage_percent', '?')}% ({a['level']})"
                for a in alerts
            )
        else:
            msg = "Disk usage normal"

        return {"status": overall_status, "data": {"mounts": results}, "message": msg}

    except Exception as e:
        return {"status": "error", "data": {}, "message": f"disk check failed: {e}"}


# ============================================================
# Probe: Docker Containers
# ============================================================

def check_docker() -> dict:
    """Verifie l'etat des conteneurs Docker.

    Detecte: conteneurs arretes, unhealthy, restarts excessifs.
    Fail-open si Docker n'est pas installe.
    """
    try:
        # Verifier si docker est disponible
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True, timeout=20,
        )
        if result.returncode != 0:
            return {"status": "ok", "data": {"available": False}, "message": "Docker not running or not installed"}

        config = _get_config()
        restart_threshold = config.get("docker_restart_threshold", 5)

        # Lister les conteneurs avec format JSON-like
        result = subprocess.run(
            ["docker", "ps", "-a", "--format", "{{.Names}}\t{{.Status}}\t{{.State}}"],
            capture_output=True, text=True, timeout=20,
        )

        if result.returncode != 0:
            return {"status": "error", "data": {}, "message": f"docker ps failed: {result.stderr[:100]}"}

        containers = []
        issues = []

        for line in result.stdout.strip().split("\n"):
            if not line.strip():
                continue
            parts = line.split("\t")
            if len(parts) < 3:
                continue
            name, status, state = parts[0], parts[1], parts[2]

            container = {"name": name, "status": status, "state": state}

            # Verifier les restarts
            try:
                restart_result = subprocess.run(
                    ["docker", "inspect", "--format", "{{.RestartCount}}", name],
                    capture_output=True, text=True, timeout=20,
                )
                restart_count = int(restart_result.stdout.strip()) if restart_result.returncode == 0 else 0
                container["restart_count"] = restart_count
                if restart_count >= restart_threshold:
                    issues.append(f"{name}: {restart_count} restarts")
            except (ValueError, subprocess.TimeoutExpired):
                container["restart_count"] = -1

            if state != "running":
                issues.append(f"{name}: {state}")

            containers.append(container)

        if not containers:
            return {"status": "ok", "data": {"available": True, "containers": []}, "message": "No containers found"}

        overall = "critical" if issues else "ok"
        msg = "; ".join(issues) if issues else f"{len(containers)} containers running"

        return {"status": overall, "data": {"available": True, "containers": containers}, "message": msg}

    except FileNotFoundError:
        return {"status": "ok", "data": {"available": False}, "message": "Docker not installed"}
    except subprocess.TimeoutExpired:
        return {"status": "error", "data": {}, "message": "Docker command timeout"}
    except Exception as e:
        return {"status": "error", "data": {}, "message": f"docker check failed: {e}"}


# ============================================================
# Probe: Systemd Services
# ============================================================

def check_services() -> dict:
    """Verifie l'etat des services systemd critiques.

    Services configures dans memory_v2.yaml heartbeat.critical_services.
    Gere la socket activation (ex: ssh.socket sur Ubuntu).
    """
    try:
        config = _get_config()
        services = config.get("critical_services", ["ssh", "docker", "ufw"])

        results = []
        failed = []

        for svc in services:
            try:
                result = subprocess.run(
                    ["systemctl", "is-active", svc],
                    capture_output=True, text=True, timeout=20,
                )
                state = result.stdout.strip()

                # Socket activation fallback: si le .service est inactive,
                # verifier si le .socket correspondant est actif (ex: ssh.socket sur Ubuntu)
                if state != "active":
                    socket_result = subprocess.run(
                        ["systemctl", "is-active", f"{svc}.socket"],
                        capture_output=True, text=True, timeout=20,
                    )
                    if socket_result.stdout.strip() == "active":
                        state = "active (socket)"

                results.append({"service": svc, "state": state})
                if state not in ("active", "active (socket)"):
                    failed.append(f"{svc}: {state}")
            except (FileNotFoundError, subprocess.TimeoutExpired):
                results.append({"service": svc, "state": "unknown"})
                failed.append(f"{svc}: unknown")

        overall = "critical" if failed else "ok"
        msg = "; ".join(failed) if failed else f"{len(services)} services active"

        return {"status": overall, "data": {"services": results}, "message": msg}

    except Exception as e:
        return {"status": "error", "data": {}, "message": f"service check failed: {e}"}


# ============================================================
# Probe: Security Updates (APT)
# ============================================================

def check_security_updates() -> dict:
    """Verifie les mises a jour disponibles via apt.

    N'execute aucune installation. Lecture seule.
    """
    try:
        config = _get_config()
        if not config.get("check_apt_updates", True):
            return {"status": "ok", "data": {"skipped": True}, "message": "apt check disabled"}

        result = subprocess.run(
            ["apt", "list", "--upgradable"],
            capture_output=True, text=True, timeout=20,
            env={**os.environ, "LANG": "C"},
        )

        # apt list ecrit sur stderr un warning qu'on ignore
        lines = [l for l in result.stdout.strip().split("\n") if l and "Listing..." not in l]
        total_updates = len(lines)

        security_updates = [l for l in lines if "security" in l.lower()]

        data = {
            "total_updates": total_updates,
            "security_updates": len(security_updates),
            "packages": lines[:10],  # Top 10 pour le rapport
        }

        if len(security_updates) > 0:
            overall = "warning"
            msg = f"{total_updates} updates ({len(security_updates)} security)"
        elif total_updates > 0:
            overall = "ok"
            msg = f"{total_updates} updates available"
        else:
            overall = "ok"
            msg = "System up to date"

        return {"status": overall, "data": data, "message": msg}

    except FileNotFoundError:
        return {"status": "ok", "data": {}, "message": "apt not available"}
    except subprocess.TimeoutExpired:
        return {"status": "error", "data": {}, "message": "apt check timeout"}
    except Exception as e:
        return {"status": "error", "data": {}, "message": f"apt check failed: {e}"}


# ============================================================
# Probe: Log Anomalies
# ============================================================

def check_logs() -> dict:
    """Analyse les logs recents pour detecter des anomalies.

    Utilise journalctl pour les derniers messages. Lecture seule.
    """
    try:
        config = _get_config()
        max_lines = config.get("log_lines_to_check", 100)
        patterns = config.get("log_error_patterns", ["error", "failed", "critical"])

        result = subprocess.run(
            ["journalctl", "--no-pager", "-n", str(max_lines), "--priority=err..emerg"],
            capture_output=True, text=True, timeout=20,
        )

        if result.returncode != 0:
            return {"status": "error", "data": {}, "message": f"journalctl failed: {result.stderr[:100]}"}

        lines = result.stdout.strip().split("\n")
        # Filtrer les lignes vides et le header journalctl
        log_lines = [l for l in lines if l.strip() and "-- No entries --" not in l and "-- Journal begins" not in l]

        anomalies = []
        for line in log_lines:
            line_lower = line.lower()
            for pattern in patterns:
                if pattern.lower() in line_lower:
                    anomalies.append(line[:200])
                    break

        # Deduplication par service (garder le dernier de chaque)
        seen_services = set()
        unique_anomalies = []
        for a in reversed(anomalies):
            # Extraire le nom de service (format: "date host service[pid]: message")
            parts = a.split()
            svc_key = parts[4] if len(parts) > 4 else a[:50]
            if svc_key not in seen_services:
                seen_services.add(svc_key)
                unique_anomalies.append(a)
        unique_anomalies.reverse()

        data = {
            "total_errors": len(log_lines),
            "unique_anomalies": len(unique_anomalies),
            "samples": unique_anomalies[:5],
        }

        if len(unique_anomalies) > 10:
            overall = "warning"
            msg = f"{len(unique_anomalies)} unique error sources in recent logs"
        elif len(unique_anomalies) > 0:
            overall = "ok"
            msg = f"{len(unique_anomalies)} error sources (normal)"
        else:
            overall = "ok"
            msg = "No significant log anomalies"

        return {"status": overall, "data": data, "message": msg}

    except FileNotFoundError:
        return {"status": "ok", "data": {}, "message": "journalctl not available"}
    except subprocess.TimeoutExpired:
        return {"status": "error", "data": {}, "message": "journalctl timeout"}
    except Exception as e:
        return {"status": "error", "data": {}, "message": f"log check failed: {e}"}




# ============================================================
# Probe: Memory DB Health
# ============================================================

def check_memory_db() -> dict:
    """Verifie la sante de la base SQLite memory.db."""
    try:
        import sqlite3
        db_path = Path(os.path.expanduser("~")) / ".claude" / "hooks" / "data" / "memory.db"

        if not db_path.exists():
            return {"status": "warning", "data": {}, "message": "memory.db not found"}

        size_mb = db_path.stat().st_size / (1024 * 1024)
        if size_mb > 500:
            return {"status": "critical", "data": {"size_mb": round(size_mb, 1)},
                    "message": f"memory.db too large: {size_mb:.1f} MB"}

        conn = sqlite3.connect(str(db_path), timeout=5.0)
        conn.row_factory = sqlite3.Row

        result = conn.execute("PRAGMA integrity_check").fetchone()
        integrity = result[0] if result else "unknown"

        try:
            memories = conn.execute("SELECT COUNT(*) FROM memories").fetchone()[0]
            sessions = conn.execute("SELECT COUNT(*) FROM sessions").fetchone()[0]
            facts = conn.execute("SELECT COUNT(*) FROM facts").fetchone()[0]
            retrievals = conn.execute("SELECT COUNT(*) FROM retrieval_log").fetchone()[0]
        except Exception:
            memories = sessions = facts = retrievals = -1

        conn.close()

        data = {
            "size_mb": round(size_mb, 2),
            "integrity": integrity,
            "memories": memories, "sessions": sessions,
            "facts": facts, "retrievals": retrievals,
        }

        if integrity != "ok":
            return {"status": "critical", "data": data,
                    "message": f"DB integrity failed: {integrity}"}

        return {"status": "ok", "data": data,
                "message": f"DB healthy: {memories} memories, {sessions} sessions, {size_mb:.1f} MB"}

    except Exception as e:
        return {"status": "error", "data": {}, "message": f"DB check failed: {e}"}


# ============================================================
# Probe: Network VM 100
# ============================================================

def check_network_vm100() -> dict:
    """Ping la VM 100 (192.168.1.162) pour verifier la connectivite."""
    try:
        import platform
        host = "192.168.1.162"
        if platform.system().lower() == "windows":
            cmd = ["ping", "-n", "1", "-w", "3000", host]
        else:
            cmd = ["ping", "-c", "1", "-W", "3", host]

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=20)

        if result.returncode == 0:
            import re as re_mod
            time_match = re_mod.search(r"time[=<](\d+(?:\.\d+)?)", result.stdout)
            latency = float(time_match.group(1)) if time_match else -1
            data = {"host": host, "reachable": True, "latency_ms": latency}
            if latency > 100:
                return {"status": "warning", "data": data,
                        "message": f"VM 100 slow: {latency}ms"}
            return {"status": "ok", "data": data,
                    "message": f"VM 100 reachable ({latency}ms)"}
        else:
            return {"status": "critical", "data": {"host": host, "reachable": False},
                    "message": "VM 100 unreachable"}

    except subprocess.TimeoutExpired:
        return {"status": "critical", "data": {"host": "192.168.1.162"},
                "message": "VM 100 ping timeout"}
    except Exception as e:
        return {"status": "error", "data": {}, "message": f"VM 100 check failed: {e}"}


# ============================================================
# Probe: Vault Integrity
# ============================================================

def check_vault_integrity() -> dict:
    """Verifie l'integrite basique du vault Obsidian."""
    try:
        import glob as glob_mod
        vault_path = Path(os.path.expanduser("~")) / "Documents" / "Knowledge"

        if not vault_path.exists():
            return {"status": "critical", "data": {},
                    "message": "Vault path not found"}

        md_files = glob_mod.glob(str(vault_path / "**" / "*.md"), recursive=True)
        total = len(md_files)

        no_frontmatter = 0
        sample = md_files[:50]
        for f in sample:
            try:
                with open(f, "r", encoding="utf-8", errors="replace") as fh:
                    first_line = fh.readline().strip()
                    if first_line != "---":
                        no_frontmatter += 1
            except Exception:
                continue

        estimated_no_fm = int(no_frontmatter * total / len(sample)) if sample else 0

        data = {
            "total_notes": total,
            "no_frontmatter_sample": no_frontmatter,
            "no_frontmatter_estimated": estimated_no_fm,
        }

        if total < 10:
            return {"status": "warning", "data": data,
                    "message": f"Vault nearly empty: {total} notes"}
        if estimated_no_fm > total * 0.2:
            return {"status": "warning", "data": data,
                    "message": f"{estimated_no_fm}/{total} notes missing frontmatter"}

        return {"status": "ok", "data": data,
                "message": f"Vault healthy: {total} notes"}

    except Exception as e:
        return {"status": "error", "data": {}, "message": f"Vault check failed: {e}"}


# ============================================================
# Probe: Hook Latency
# ============================================================

def check_hook_latency() -> dict:
    """Analyse les logs d'audit pour detecter des hooks lents."""
    try:
        import json as json_mod
        audit_log = Path(os.path.expanduser("~")) / ".claude" / "hooks" / "logs" / "hooks-audit.jsonl"

        if not audit_log.exists():
            return {"status": "ok", "data": {"available": False},
                    "message": "No audit log available"}

        lines = []
        with open(audit_log, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                lines.append(line)
        lines = lines[-200:]

        durations = {}
        for line in lines:
            try:
                entry = json_mod.loads(line)
                hook = entry.get("hook", "")
                dur = entry.get("duration_ms")
                if dur is not None and hook:
                    durations.setdefault(hook, []).append(dur)
            except Exception:
                continue

        if not durations:
            return {"status": "ok", "data": {"hooks_tracked": 0},
                    "message": "No duration data yet (QF1 needed)"}

        slow_hooks = []
        stats = {}
        for hook, durs in durations.items():
            avg = sum(durs) / len(durs)
            stats[hook] = {"avg_ms": round(avg, 1), "samples": len(durs)}
            if avg > 2000:
                slow_hooks.append(f"{hook}: {avg:.0f}ms")

        data = {"hooks_tracked": len(durations), "stats": stats}

        if slow_hooks:
            return {"status": "warning", "data": data,
                    "message": f"Slow hooks: {'; '.join(slow_hooks)}"}

        return {"status": "ok", "data": data,
                "message": f"{len(durations)} hooks tracked, all within limits"}

    except Exception as e:
        return {"status": "error", "data": {}, "message": f"Hook latency check failed: {e}"}


# ============================================================
# Registry des probes
# ============================================================

ALL_PROBES = {
    "disk": check_disk,
    "docker": check_docker,
    "services": check_services,
    "security_updates": check_security_updates,
    "logs": check_logs,
    "memory_db": check_memory_db,
    "network_vm100": check_network_vm100,
    "vault_integrity": check_vault_integrity,
    "hook_latency": check_hook_latency,
}


def run_all_probes() -> dict:
    """Execute toutes les probes et retourne un rapport structure."""
    report = {
        "timestamp": datetime.now().isoformat(),
        "probes": {},
        "overall_status": "ok",
        "alerts": [],
    }

    for name, probe_fn in ALL_PROBES.items():
        try:
            result = probe_fn()
        except Exception as e:
            result = {"status": "error", "data": {}, "message": f"probe {name} crashed: {e}"}

        report["probes"][name] = result

        # Agréger le statut global
        if result["status"] == "critical":
            report["overall_status"] = "critical"
            report["alerts"].append(f"[CRITICAL] {name}: {result['message']}")
        elif result["status"] == "warning" and report["overall_status"] != "critical":
            report["overall_status"] = "warning"
            report["alerts"].append(f"[WARNING] {name}: {result['message']}")
        elif result["status"] == "error":
            report["alerts"].append(f"[ERROR] {name}: {result['message']}")

    return report
