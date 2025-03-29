import os
import asyncio
from dotenv import load_dotenv
from unstructured_client import UnstructuredClient
from unstructured_client.models.operations import (
    CreateDestinationRequest,
    CreateSourceRequest,
    CreateWorkflowRequest,
    RunWorkflowRequest,
    GetWorkflowRequest,
)
from unstructured_client.models.shared import (
    SourceConnectorType,
    CreateSourceConnector,
    DestinationConnectorType,
    CreateDestinationConnector,
    S3SourceConnectorConfigInput,
    MongoDBConnectorConfigInput,
    CreateWorkflow,
    WorkflowType,
    WorkflowNode,
    WorkflowNodeType,
)

#Load environment variables
load_dotenv(override=True)


class UnstructuredPipeline:
    def __init__(self):
        """Initialize UnstructuredClient and environment variables"""
        self.client = UnstructuredClient(api_key_auth=os.getenv("UNSTRUCTURED_API_KEY"))
        
        # Load environment variables once
        self.aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
        self.aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        self.aws_s3_endpoint = os.getenv("AWS_S3_ENDPOINT")
        self.s3_bucket_name = os.getenv("S3_BUCKET_NAME")

        self.db_name = os.getenv("DATABASE_NAME")
        self.collection_name = os.getenv("COLLECTION_NAME")
        self.mongodb_uri = os.getenv("MONGODB_URI")
        self.s3_remote_url = os.getenv("S3_REMOTE_URL")
        


    async def create_source_connector(self,connector_name: str):
        """Create an s3 source connector"""
      
        #Create source connector
        source_connector = CreateSourceConnector(
            name=connector_name,
            type=SourceConnectorType.S3,
            config=S3SourceConnectorConfigInput(
                key=self.aws_access_key,
                secret=self.aws_secret_key,
                remote_url=self.s3_remote_url,
                endpoint_url=self.aws_s3_endpoint,
                recursive=True,
            ),
        )

        #Create source connector
        response = await self.client.sources.create_source_async(
            request=CreateSourceRequest(create_source_connector=source_connector)
        )

        #Return source connector information
        return response.source_connector_information



    # Create a destination connector
    async def create_destination_connector(self,connector_name: str):
        """Create a mongodb destination connector"""

        #Create destination connector
        destination_connector = CreateDestinationConnector(
            name=connector_name,
            type=DestinationConnectorType.MONGODB,
            config=MongoDBConnectorConfigInput(
                database=self.db_name,
                collection=self.collection_name,
                uri=self.mongodb_uri,
            ),
        )

        #Create destination connector
        response = await self.client.destinations.create_destination_async(
            request=CreateDestinationRequest(
                create_destination_connector=destination_connector
            )
        )

        #Return destination connector information
        return response.destination_connector_information



    async def create_workflow_unstructured(
        self,
        workflow_name: str,
        source_id: str,
        destination_id: str
    ):
        """Create a custom workflow"""

        #Create high resolution partitioner workflow node
        high_res_paritioner_workflow_node = WorkflowNode(
            name="Partitioner",
            subtype="unstructured_api",
            type=WorkflowNodeType.PARTITION,
            settings={
                "strategy": "hi_res",
                "include_page_breaks": True,
                "pdf_infer_table_structure": True,
                "xml_keep_tags": True,
                "encoding": "utf-8",
                "ocr_languages": ["eng", "fra"],
                "extract_image_block_types": ["image", "table"],
                "infer_table_structure": True,
            },
        )

        #Create ner enrichment workflow node
        ner_enrichment_workflow_node = WorkflowNode(
            name="NER Enrichment",
            subtype="openai_ner",
            type=WorkflowNodeType.PROMPTER,
            settings={
                "prompt_interface_overrides": {
                    "prompt": {
                        "user": "Please identify and classify named entities in the following text. Focus on identifying organizations, people, locations, dates, and other relevant entities. Provide the entities and their corresponding types as a structured JSON response.\n\n[START OF TEXT]"
                    }
                }
            },
        )

        #Create workflow
        workflow = CreateWorkflow(
            name=workflow_name,
            source_id=source_id,
            destination_id=destination_id,
            workflow_type=WorkflowType.CUSTOM,
            workflow_nodes=[
                high_res_paritioner_workflow_node,
                ner_enrichment_workflow_node,
            ],
        )

        #Create workflow
        response = await self.client.workflows.create_workflow_async(
            request=CreateWorkflowRequest(create_workflow=workflow)
        )

        #Return workflow information
        return response.workflow_information



    async def run_workflow_unstructured(self,workflow_id: str):
        """Run a workflow"""

        #Run workflow
        response = await self.client.workflows.run_workflow_async(
            request=RunWorkflowRequest(workflow_id=workflow_id)
        )

        #Return workflow information
        return response.raw_response


    async def get_workflow(self,workflow_id: str):
        """Get a workflow"""

        #Get workflow
        response = await self.client.workflows.get_workflow_async(
            request=GetWorkflowRequest(
                workflow_id=workflow_id
            )
        )

        #Return workflow information
        return response.workflow_information
