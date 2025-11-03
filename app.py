from aws_cdk import App
from cdk_python.cdk_python_stack import module_info

# Import the pipeline stacks we added/maintain
from cdk_python.codepipeline_dev import CodePipelineDevStack
from cdk_python.codepipeline_prod import CodePipelineProdStack

# CDK app entrypoint that instantiates both pipelines.
# Each pipeline's source action is configured to a specific branch so
# pushes to 'development' will trigger the dev pipeline and pushes to
# 'master' will trigger the prod pipeline.

app = App()

# Ensure module_info in cdk_python_stack.py defines at least 'repo_name'.
# Instantiate both pipeline stacks so they are part of the synthesized app.
CodePipelineDevStack(app, "CodePipelineDevStack")
CodePipelineProdStack(app, "CodePipelineProdStack")

app.synth()