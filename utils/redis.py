from typing import Optional

from redis import Redis

from .workflow import Workflow

REDUCTION_CONFIG_KEY = "reduction_config"


class RedisWorkflow(Workflow):
    def __init__(self, redis: Redis):
        self.redis = redis

    def submit_reduction_to_compute(self):
        pass

    def submit_fitting_to_compute(self):
        pass

    def check_flow_status(self, flow_id: str):
        pass

    def submit_job(
        self, deployment_name: str, parameters: Optional[dict] = None
    ) -> str:
        pass

    def get_workflow_names(self) -> dict:
        pass

    def get_full_deployment_names(self) -> dict:
        pass

    def save_reduction_config(self, config: dict):
        self.redis.set(REDUCTION_CONFIG_KEY, config)

    def from_settings(redis: Redis):
        return RedisWorkflow(redis)
