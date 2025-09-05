import json
from mcp.server.fastmcp import Context
from database.database import get_analyzed_documents


def register_unstructured_tools(mcp):
    @mcp.tool()
    async def create_source(ctx: Context, connector_name: str):
        """
        This tool help create a connector from data source to unstructured server where will be processed

        Args:
            connector_name (str): The name of the source connector to create.

        Returns:
            str: String
        """
        try:
            unstructured_pipeline = (
                ctx.request_context.lifespan_context.unstructured_pipeline
            )
            response = await unstructured_pipeline.create_source_connector(connector_name)
            return f"Source Connector name: {response.name} \n Source Connector id: {response.id}"
        except Exception as e:
            return json.dumps({"error": {"type": e.__class__.__name__, "message": str(e)}}, indent=2)

    @mcp.tool()
    async def create_destination(ctx: Context, connector_name: str):
        """
        This tool help create a connector from unstructured server  to destination where the data will be stored

        Args:
            connector_name (str): The name of the destination connector to create.

        Returns:
            str: String
        """
        try:
            unstructured_pipeline = (
                ctx.request_context.lifespan_context.unstructured_pipeline
            )
            response = await unstructured_pipeline.create_destination_connector(
                connector_name
            )
            return f"Connector name: {response.name} \n Connector id: {response.id}"
        except Exception as e:
            return json.dumps({"error": {"type": e.__class__.__name__, "message": str(e)}}, indent=2)

    @mcp.tool()
    async def create_workflow(
        ctx: Context, workflow_name: str, source_id: str, destination_id: str
    ):
        """
        This tool help create a workflow the workflow to process the data from the source connector to the destination connector

        Args:
            workflow_name (str): The name of the workflow to create.
            source_id (str): The id of the source connector.
            destination_id (str): The id of the destination connector.

        Returns:
            str: String
        """
        try:
            unstructured_pipeline = (
                ctx.request_context.lifespan_context.unstructured_pipeline
            )
            response = await unstructured_pipeline.create_workflow_unstructured(
                workflow_name, source_id, destination_id
            )
            return f"Workflow name: {response.name} \n Workflow id: {response.id} \n Workflow status: {response.status} \n Workflow type: {response.workflow_type} \n Source(s): {response.sources} \n Destination(s): {response.destinations} \n Schedule(s): {response.schedule.crontab_entries}"
        except Exception as e:
            return json.dumps({"error": {"type": e.__class__.__name__, "message": str(e)}}, indent=2)

    @mcp.tool()
    async def run_workflow(ctx: Context, workflow_id: str):
        """
        This tool help run a workflow.

        Args:
            workflow_id (str): The id of the workflow to run.

        Returns:
            str: String
        """
        try:
            unstructured_pipeline = (
                ctx.request_context.lifespan_context.unstructured_pipeline
            )
            response = await unstructured_pipeline.run_workflow_unstructured(workflow_id)
            return f"{response}"
        except Exception as e:
            return json.dumps({"error": {"type": e.__class__.__name__, "message": str(e)}}, indent=2)

    @mcp.tool()
    async def get_workflow_details(ctx: Context, workflow_id: str):
        """
        This tool help get a workflow details. such as name, id, status, type, sources, destinations, schedule.

        Args:
            workflow_id (str): The id of the workflow to get details.

        Returns:
            str: String
        """
        try:
            unstructured_pipeline = (
                ctx.request_context.lifespan_context.unstructured_pipeline
            )
            response = await unstructured_pipeline.get_workflow(workflow_id)
            return f"Workflow name: {response.name} \n Workflow id: {response.id} \n Workflow status: {response.status}"
        except Exception as e:
            return json.dumps({"error": {"type": e.__class__.__name__, "message": str(e)}}, indent=2)

    @mcp.tool()
    async def fetch_documents():
        """
        This tool will help fetch the document analyzed during the workflow execution

        Returns:
            str: String
        """
        try:
            return get_analyzed_documents()
        except Exception as e:
            return json.dumps({"error": {"type": e.__class__.__name__, "message": str(e)}}, indent=2)
