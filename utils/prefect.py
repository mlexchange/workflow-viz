import asyncio
from typing import Optional

from prefect import get_client

from .workflow import Workflow


class PrefectWorkflow(Workflow):
    def __init__(self):
        super().__init__()

    async def _schedule(
        self,
        deployment_name: str,
        flow_run_name: str,
        parameters: Optional[dict] = None,
    ):
        async with get_client() as client:
            deployment = await client.read_deployment_by_name(deployment_name)
            assert (
                deployment
            ), f"No deployment found in config for deployment_name {deployment_name}"
            flow_run = await client.create_flow_run_from_deployment(
                deployment.id, parameters=parameters, name=flow_run_name
            )

        return flow_run.id

    def schedule_prefect_flow(
        self,
        deployment_name: str,
        parameters: Optional[dict] = None,
    ):
        if "input_data_uri" in parameters:
            input_data_uri = parameters["input_data_uri"]
            flow_run_name = f"{deployment_name}: {input_data_uri}"
        else:
            flow_run_name = None
        flow_run_id = asyncio.run(
            self._schedule(deployment_name, flow_run_name, parameters)
        )
        return flow_run_id

    async def _check(self, flow_run_id):
        async with get_client() as client:
            flow_run = await client.read_flow_run(flow_run_id)
            if flow_run.state.is_final():
                if flow_run.state.is_completed():
                    return "completed"
                else:
                    # This means the run failed, crashed or was cancelled
                    return "failed"
            else:
                return "pending"

    def check_status_flow_run(self, flow_run_id):
        """Checks on the current status of the flow with the given id."""
        return asyncio.run(self._check(flow_run_id))

    async def _deployment_names(self):
        deployments_by_name = dict()
        async with get_client() as client:
            deployments = await client.read_deployments()
            for deployment in deployments:
                name = deployment.name
                flow_id = deployment.flow_id
                flow = await client.read_flow(flow_id)
                full_name = f"{flow.name}/{name}"
                deployments_by_name[name] = full_name
            return deployments_by_name

    def get_full_deployment_names(self):
        return asyncio.run(self._deployment_names())
