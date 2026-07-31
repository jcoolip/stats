from flask import Flask, jsonify
import psutil

app = Flask(__name__)


def get_cpu_usage():
    return {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "cpu_count": psutil.cpu_count(),
    }

def get_memory():
    mem = psutil.virtual_memory()
    return {
        "mem_total": (mem.total / (1024**3)),
        "mem_available": (mem.available / (1024**3)),
        "mem_percent_used": mem.percent,
    }

def get_storage():
    disk = psutil.disk_usage('/')
    return {
        "disk_total": (disk.total / (1024**3)),
        "disk_free": (disk.free / (1024**3)),
        "disk_percent_used": (disk.percent),
    }

def get_temp():
    temp = psutil.sensors_temperatures()
    return temp

@app.route("/api/stats")
def stats():
    return jsonify({
        "mem": get_memory(),
        "disk": get_storage(),
        "temp": get_temp(),
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5555, debug=True)