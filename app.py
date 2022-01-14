from flask import Flask, render_template, request
from redis import Redis
from rq import Queue
from rq.registry import ScheduledJobRegistry
from rq.job import Job
from datetime import datetime, timedelta


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
    #check if sleeping first
    registry = ScheduledJobRegistry(queue=q)
    scheduledIDs = registry.get_job_ids()
    if len(scheduledIDs) > 1:
        return "more than one job scheduled, something isn't right"
    elif len(scheduledIDs) == 1:
        time_sleeping_until = registry.get_scheduled_time(scheduledIDs[0])
    else:
        time_sleeping_until = False

    BlinkAccount.refresh()
    sync = BlinkAccount.sync["Home1"]

    if time_sleeping_until and sync.arm == False:
        return "Module sleeping"
    elif sync.arm:
        return "Armed"
    else:
        return "Disarmed"


@app.route("/sleep", methods=["POST"])
def sleep():
    data = request.get_json()

    registry = ScheduledJobRegistry(queue=q)
    scheduledIDs = registry.get_job_ids()

    if 'sleepminutes' in data and len(scheduledIDs) == 0:
        minutes = int(data['sleepminutes'])
        disarm_module()
        job = q.enqueue_in(timedelta(minutes=minutes), arm_module)
        return "Going to sleep"
    elif len(scheduledIDs) > 0:
        return "already sleeping"
    else:
        return "bad request"
        





