# Starter skeleton for homework 1: externalizing in-memory session state
# so any app instance can serve any request.
#
# BEFORE (what to refactor away from): a plain in-memory dict like
#   sessions = {}
# tied to a single process's memory means only the instance that created
# a session can read it back — that's what breaks when you put a second
# instance behind a load balancer.
#
# AFTER (this skeleton): sessions live in Redis, shared by every instance.
# Fill in the pieces marked TODO.

from flask import Flask, request, make_response
import redis
import uuid
import json

app = Flask(__name__)
store = redis.Redis(host="localhost", port=6379, decode_responses=True)

SESSION_TTL_SECONDS = 3600


@app.route("/login", methods=["POST"])
def login():
    # TODO: validate request.form["user"] / credentials however your
    # toy app is doing auth today.
    session_id = str(uuid.uuid4())
    session_data = {"user": request.form["user"]}

    store.set(session_id, json.dumps(session_data), ex=SESSION_TTL_SECONDS)

    resp = make_response({"ok": True})
    resp.set_cookie("session_id", session_id)
    return resp


@app.route("/whoami")
def whoami():
    session_id = request.cookies.get("session_id")
    if not session_id:
        return {"error": "no session cookie"}, 401

    raw = store.get(session_id)
    if raw is None:
        return {"error": "session not found or expired"}, 401

    return json.loads(raw)


# TODO: add a /logout route that deletes the key from `store`.
# TODO: run two instances of this app on different ports (e.g. FLASK_RUN_PORT=3001
# and 3002) pointed at the SAME Redis instance, put a load balancer in front
# (see topic 16's nginx example), and prove a session created via instance A
# is readable from instance B.

if __name__ == "__main__":
    app.run(port=3001)
