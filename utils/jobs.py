# Adapter functions for managing how jobs are created and monitored by the UI
# Supports prefect (monitored orchestration) and arroyo (live-time execution)
import os
from abc import ABC, abstractmethod

PREFECT_ENABLED = os.getenv("PREFECT_ENABLED", "true").lower() == "true"


class JobManager(ABC):
    """
    Abstract base class for job management.
    Subclasses should implement the methods for scheduling and checking job status.
    """

    @abstractmethod
    def schedule_job(self, job_name: str, parameters: dict) -> str:
        """
        Schedules a job with the given name and parameters.
        Returns the job ID.
        """
        pass

    @abstractmethod
    def check_job_status(self, job_id: str) -> str:
        """
        Checks the status of a scheduled job with the given ID.
        Returns the job status.
        """
        pass


job_manager: JobManager = None

if PREFECT_ENABLED:
    from utils.prefect import check_status_flow_run, schedule_prefect_flow

    class PrefectJobManager(JobManager):
        def schedule_job(self, job_name: str, parameters: dict) -> str:
            return schedule_prefect_flow(job_name, parameters)

        def check_job_status(self, job_id: str) -> str:
            return check_status_flow_run(job_id)

    job_manager = PrefectJobManager()

else:
    from utils.redis import RedisConn

    class ArroyoJobManager(JobManager):
        def __init__(self, redis_conn: RedisConn):
            self.redis_conn: RedisConn = redis_conn

        def schedule_job(self, job_name: str, parameters: dict) -> str:
            return self.redis_conn.schedule_job(job_name, parameters)

        def check_job_status(self, job_id: str) -> str:
            return self.redis_conn.check_job_status(job_id)

    job_manager = ArroyoJobManager()
