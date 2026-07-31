from flask import Flask, jsonify
import time

import psutil

app = Flask(__name__)

GIB = 1024**3


def get_cpu_usage():
    return {
        "percent": psutil.cpu_percent(interval=0.1),
        "logical_count": psutil.cpu_count(),
        "physical_count": psutil.cpu_count(logical=False),
    }


def get_memory():
    mem = psutil.virtual_memory()

    return {
        "total_gb": round(mem.total / GIB, 2),
        "used_gb": round(mem.used / GIB, 2),
        "available_gb": round(mem.available / GIB, 2),
        "percent_used": mem.percent,
    }


def get_storage():
    paths = {
        "root": "/",
    }

    storage = {}

    for name, path in paths.items():
        disk = psutil.disk_usage(path)

        storage[name] = {
            "path": path,
            "total_gb": round(disk.total / GIB, 2),
            "used_gb": round(disk.used / GIB, 2),
            "free_gb": round(disk.free / GIB, 2),
            "percent_used": disk.percent,
        }

    return storage

import psutil


def get_temp():
    temperatures = psutil.sensors_temperatures()

    preferred_sensors = (
        "coretemp",
        "cpu_thermal",
        "k10temp",
        "zenpower",
    )

    for sensor_name in preferred_sensors:
        readings = temperatures.get(sensor_name)

        if readings:
            return round(readings[0].current, 1)

    for readings in temperatures.values():
        if readings:
            return round(readings[0].current, 1)

    return None

# def get_temp():
#     temperatures = {}

#     for sensor, entries in psutil.sensors_temperatures().items():
#         temperatures[sensor] = [
#             {
#                 "label": entry.label or sensor,
#                 "current_c": entry.current,
#                 "high_c": entry.high,
#                 "critical_c": entry.critical,
#             }
#             for entry in entries
#         ]

#     return temperatures


def get_uptime():
    uptime_seconds = int(time.time() - psutil.boot_time())

    days, remainder = divmod(uptime_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)

    return {
        "seconds": uptime_seconds,
        "days": days,
        "hours": hours,
        "minutes": minutes,
        "pretty": f"{days}d {hours}h {minutes}m",
    }


@app.get("/api/stats")
def stats():
    return jsonify(
        {
            "uptime": get_uptime(),
            "cpu": get_cpu_usage(),
            "mem": get_memory(),
            "disk": get_storage(),
            "temp": get_temp(),
        }
    )


@app.get("/api/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5555, debug=True)