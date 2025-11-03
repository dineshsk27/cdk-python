from aws_cdk import (
    Stack,
    aws_codecommit as codecommit,
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as cp_actions,
    aws_iam as iam,
)
from constructs import Construct

# Parse GitHub URL metadata
git_url = "https://github.com/dineshsk27/cdk-python.git"
parts = git_url.rstrip(".git").split("/")
repo_owner = parts[-2]
repo_name = parts[-1]

# Import the application stack class to be deployed by the pipeline
from .cdk_python_stack import CdkPythonStack

class CodePipelineProdStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Use CodeCommit repository as source; if you want GitHub use CodeStar connections action instead
        repo = codecommit.Repository.from_repository_name(self, "SourceRepo", repository_name=repo_name)

        source_output = codepipeline.Artifact(artifact_name="SourceOutput")

        source_action = cp_actions.CodeCommitSourceAction(
            action_name="CodeCommit_Source_Master",
            repository=repo,
            branch="master",
            output=source_output,
        )

        pipeline = codepipeline.Pipeline(self, "PipelineProd", pipeline_name=f"{repo_name}-prod-pipeline")
        pipeline.add_stage(stage_name="Source", actions=[source_action])

        # Add a CloudFormation deploy action that deploys the CdkPythonStack synthesized template
        # We will use a CloudFormationCreateUpdateStackAction that looks for a template file in the source artifact.
        # The CDK synth step must produce the template at 'CdkPythonStack.template.json' path in the artifact.

        # Add a synth step (placeholder) - in real setup you'd run 'cdk synth' in a build action to output templates
        # For simplicity here we demonstrate creating a deploy role and a deploy action that assumes a template path.

        deploy_role = iam.Role(self, "CFNDeployRole",
            assumed_by=iam.ServicePrincipal("cloudformation.amazonaws.com")
        )

        deploy_action = cp_actions.CloudFormationCreateUpdateStackAction(
            action_name="CFN_Deploy",
            stack_name=f"{repo_name}-prod-stack",
            template_path=source_output.at_path("CdkPythonStack.template.json"),
            admin_permissions=True,
            role=deploy_role,
        )

        pipeline.add_stage(stage_name="Deploy", actions=[deploy_action])

        self.pipeline_name = pipeline.pipeline_name
