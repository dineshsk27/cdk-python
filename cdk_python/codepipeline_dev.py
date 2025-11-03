from aws_cdk import (
    Stack,
    aws_codecommit as codecommit,
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as cp_actions,
)
from constructs import Construct

# Import module values from existing stack file. Adjust names to match your cdk_python_stack.py exports.
try:
    from .cdk_python_stack import module_info
except Exception:
    # Fallback: provide a placeholder module_info so this file doesn't break import during review.
    module_info = {
        "repo_name": "my-repo",
        "repo_owner": "my-owner",
    }

class CodePipelineDevStack(Stack):
    """CDK Stack that defines a CodePipeline for the 'development' branch.

    Important notes:
    - Uses a CodeCommit source action targeting branch 'development'.
    - Sets codestar_connection_arn to an empty string as requested; update with a real ARN when available.
    - Reads repo name from module_info imported from cdk_python_stack.py.
    """

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        repo_name = module_info.get("repo_name", "my-repo")

        # Look up or create the CodeCommit repository reference. Adjust to your environment.
        repo = codecommit.Repository.from_repository_name(self, "SourceRepo", repository_name=repo_name)

        source_output = codepipeline.Artifact(artifact_name="SourceOutput")

        # Empty CodeStar connection ARN as requested
        codestar_connection_arn = ""

        source_action = cp_actions.CodeCommitSourceAction(
            action_name="CodeCommit_Source_Development",
            repository=repo,
            branch="development",
            output=source_output,
        )

        pipeline = codepipeline.Pipeline(self, "PipelineDev", pipeline_name=f"{repo_name}-dev-pipeline")
        pipeline.add_stage(stage_name="Source", actions=[source_action])

        # Add additional stages (build/deploy) as needed. Placeholder here.

        # Export pipeline name as an attribute for other stacks or inspection
        self.pipeline_name = pipeline.pipeline_name
