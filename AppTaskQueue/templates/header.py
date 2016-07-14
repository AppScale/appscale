""" Implements a task queue worker and routing. This is just
    a template and not the actual script which is run. Actual scripts 
    can be found in /etc/appscale/celery/workers.

    Find and replace the following:
    APP_ID: Set this to the current application ID.
    CELERY_CONFIGURATION: The name of the celery configuration file.
"""
import datetime
import httplib
import sys
import yaml

def setup_environment():
  ENVIRONMENT_FILE = "/etc/appscale/environment.yaml"
  FILE = open(ENVIRONMENT_FILE)
  env = yaml.load(FILE.read())
  APPSCALE_HOME = env["APPSCALE_HOME"]
  sys.path.append(APPSCALE_HOME + "/AppTaskQueue")
  sys.path.append(APPSCALE_HOME + "/AppServer")
  sys.path.append(APPSCALE_HOME + "/lib")

setup_environment()
from celery import Celery
from celery.utils.log import get_task_logger

from urlparse import urlparse

from tq_config import TaskQueueConfig
from tq_lib import TASK_STATES
from distributed_tq import TaskName


sys.path.append(TaskQueueConfig.CELERY_CONFIG_DIR)
sys.path.append(TaskQueueConfig.CELERY_WORKER_DIR)

app_id = 'APP_ID'

config = TaskQueueConfig(TaskQueueConfig.RABBITMQ, app_id)
module_name = TaskQueueConfig.get_celery_worker_module_name(app_id)
celery = Celery(module_name, broker=config.get_broker_string(),
  backend='amqp://')

celery.config_from_object('CELERY_CONFIGURATION')

logger = get_task_logger(__name__)

# This template header and tasks can be found in appscale/AppTaskQueue/templates
