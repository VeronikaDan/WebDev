# -*- coding: utf-8 -*-
DEFAULT_PORT = 5000
ADDITIVE_FOR_UID = 1000

try:
	from os import getuid

except ImportError:
	def getuid():
		return DEFAULT_PORT - ADDITIVE_FOR_UID

from flask import Flask, jsonify
from celery import Celery
from celery.result import AsyncResult


def make_celery(app):
    celery = Celery('backend.main', backend=app.config['CELERY_RESULT_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

app = Flask(__name__)
app.config.update(
    CELERY_BROKER_URL='amqp://',
    CELERY_RESULT_BACKEND='amqp://'
)
celery = make_celery(app)


@celery.task()
def hello(a, b):
    from time import sleep
    print('Start task with args {} {}'.format(a, b))
    sleep(10)
    result = a + b
    print('End task with result {}'.format(result))
    return result


@app.route("/run_tasks")
def run_tasks():
    print('Start function')
    tasks = list()
    for i in range(4):
        task = hello.delay(i, i * 2)
        tasks.append(str(task))
    print('End function')
    return jsonify({"tasks": tasks})

@app.route("/check_task/<task_id>")
def check_task(task_id):
    task = hello.AsyncResult(task_id)
    return jsonify({
        "task_id": task.id,
        "result": task.result,
        "state": task.state,
        "ready": task.ready()
    })


if __name__ == '__main__':
	app.run(port=getuid() + ADDITIVE_FOR_UID, debug=True)
