from flask import Flask, render_template, request

from redis import Redis
from rq import Queue
from datetime import timedelta
from blink import BlinkAccount, arm_module, disarm_module

app = Flask(__name__)

q = Queue(connection=Redis())

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/fetch", methods=["POST"])
def fetch():
    data = request.get_json()

    return data["sleepminutes"]

@app.route("/status")
def status():
    BlinkAccount.refresh()
    sync = BlinkAccount.sync["Home1"]
    status = f"{sync.name}: {'Armed' if sync.arm else 'Disarmed'}"
    return status

@app.route("/sleep", methods=["POST"])
def sleep():
    # TODO: check if it's already disarmed, and send response
    data = request.get_json()

    if 'sleepminutes' in data:
        minutes = int(data['sleepminutes'])
        disarm_module()
        job = q.enqueue_in(timedelta(minutes=minutes), arm_module)
        return "OK"
    else:
        return "bad request"
        





