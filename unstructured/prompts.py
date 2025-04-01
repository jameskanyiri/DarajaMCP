def register_unstructured_prompts(mcp):
    @mcp.prompt()
    async def create_and_run_workflow_prompt(user_input: str):
        """
        This prompt help to create a source connector and a destination connector, then setting up the workflow and executing it.

        Args:
            user_input (str): The user input.

        Returns:
            str: String
        """
        return f"The user wants to achieve {user_input}. Assist them by creating a source connector and a destination connector, then setting up the workflow and executing it."
