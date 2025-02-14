from abc import ABC, abstractmethod
from typing import Optional


class Workflow(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def submit_reduction_to_compute(self):
        pass

    @abstractmethod
    def submit_fitting_to_compute(self):
        pass

    @abstractmethod
    def check_flow_status(self, flow_id: str):
        pass

    @abstractmethod
    def submit_job(
        self, deployment_name: str, parameters: Optional[dict] = None
    ) -> str:
        pass

    @abstractmethod
    def get_full_deployment_names(self) -> dict:
        pass

    @abstractmethod
    def get_workflow_names(self) -> dict:
        pass


def workflow_factory(workflow_type: str) -> Workflow:
    if workflow_type == "redis":
        from redis import Redis

        from .redis import RedisWorkflow

        redis = Redis("localhost", 44444)
        return RedisWorkflow(redis)
    elif workflow_type == "prefect":
        from .prefect import PrefectWorkflow

        return PrefectWorkflow()
    else:
        raise ValueError(f"Invalid workflow type: {workflow_type}")


workflow = workflow_factory("redis")
