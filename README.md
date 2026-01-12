# Amazon Bedrock AgentCore - Basic Travel Agent

This repository contains a basic travel agent implementation based on the [Dynatrace Amazon Bedrock AgentCore example](https://github.com/dynatrace-oss/dynatrace-ai-agent-instrumentation-examples/tree/main/aws-agent-sample/agent-core), modified to support invocation through the AgentCore Runtime.

## Deploy

Set the following environment variables:

- **DT_OTEL_ENDPOINT**: OpenTelemetry ingest endpoint, eg. https://abc12345.live.dynatrace.com/api/v2/otlp
- **DT_TOKEN_SECRET_NAME**: AWS Secrets Manager secret name of the Dynatrace API token with OpenTelemetry ingest permissions
- ***(Optional)*** **DT_TOKEN_SECRET_REGION**: AWS region of the Secrets Manager (default: us-east-1)

To deploy the agent to AWS, use the AgentCore CLI. First, run `agentcore configure` to set up your project and define deployment parameters. Then, execute `agentcore deploy` to complete the deployment.
