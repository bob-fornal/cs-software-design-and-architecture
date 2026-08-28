# Starter skeleton for homework 2: a minimal service discovery registry.
#
# This is deliberately tiny — a single Flask app acting as a shared registry
# that other toy services register themselves with and query to find each
# other's current address. Real systems (Consul, etcd, Kubernetes Services)
# do this with far more robustness, but the core idea is the same: don't
# hardcode addresses, look them up at runtime, and drop stale entries.

from flask import Flask, request, jsonify
import time

app = Flask(__name__)

# name -> {"host": ..., "port": ..., "last_seen": <timestamp>}
registry = {}

HEARTBEAT_WINDOW_SECONDS = 15


@app.post("/register")
def register():
    body = request.json
    name = body["name"]
    registry[name] = {
        "host": body["host"],
        "port": body["port"],
        "last_seen": time.time(),
    }
    return jsonify({"ok": True})


@app.get("/lookup/<name>")
def lookup(name):
    entry = registry.get(name)
    if entry is None:
        return jsonify({"error": "not found"}), 404

    age = time.time() - entry["last_seen"]
    if age > HEARTBEAT_WINDOW_SECONDS:
        # TODO: decide whether to actively evict here, or just treat
        # stale entries as unavailable on lookup.
        return jsonify({"error": "stale", "age_seconds": age}), 404

    return jsonify(entry)


@app.get("/services")
def list_services():
    # TODO: helpful for debugging — return all currently-registered
    # (non-stale) services.
    return jsonify(registry)


# TODO in your toy services (not this file):
#   1. On startup, POST /register with your own name/host/port.
#   2. On an interval (e.g. every 5s), POST /register again as a heartbeat.
#   3. Before calling another service, GET /lookup/<name> instead of using
#      a hardcoded address.
#   4. Kill one service and show it drops out of /services within
#      HEARTBEAT_WINDOW_SECONDS.

if __name__ == "__main__":
    app.run(port=5000)
