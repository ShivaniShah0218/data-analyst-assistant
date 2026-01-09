from celery import Celery
import time
import redis
from ..design_workflow import AgentFlow_Design
from ..agent import AgentState
import pandas as pd



da_agent = AgentFlow_Design()
agent_call = da_agent.define_workflow()

# Configuring celery
celery_app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
)

# redis client
redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)


@celery_app.task(name="app.tasks.process_csv_task")
def process_csv_task(task_id: str, file_path: str):
    try:
        # Simulate a delay for processing
        time.sleep(5)
        initial_state = AgentState(file_path=file_path, data=None, preprocessing_steps=[], info=[], error_message="", anomalies=None, correlations=None)
        result = agent_call.invoke(initial_state)
        print(result)

        # Set result in redis
        redis_client.set(task_id, result)

        return {"status": "completed", "task_id": task_id}

    except Exception as e:
        redis_client.set(task_id, f"Failed: {str(e)}")
        return {"status": "failed", "error": str(e)}
