import os
import boto3
from botocore.exceptions import ClientError

OTEL_ENDPOINT = os.environ.get("DT_OTEL_ENDPOINT")
SECRET_NAME = os.environ.get("DT_TOKEN_SECRET_NAME")
SECRET_AWS_REGION = os.environ.get("DT_TOKEN_SECRET_REGION", "us-east-1")

if not all([OTEL_ENDPOINT, SECRET_NAME]):
    raise ValueError(
        "Missing required Dynatrace configuration. Please set these environment variables:\n"
        "  - DT_OTEL_ENDPOINT\n"
        "  - DT_TOKEN_SECRET_NAME\n"
        "  - DT_TOKEN_SECRET_REGION (optional, defaults to us-east-1)"
    )

def read_secret(secret_name: str, region_name: str = "us-east-1"):
    """
    Retrieve secret from AWS Secrets Manager.
    For Agentcore Runtime deployment, ensure the runtime has IAM permissions:
    secretsmanager:GetSecretValue on the secret ARN.
    """
    try:
        session = boto3.session.Session()
        client = session.client(service_name='secretsmanager', region_name=region_name)
        response = client.get_secret_value(SecretId=secret_name)
        return response['SecretString'].rstrip()
    except ClientError as e:
        print(f"Error retrieving secret '{secret_name}': {e}")
        return ""
    except Exception as e:
        print(f"Unexpected error retrieving secret: {e}")
        return ""

def init():
    os.environ['TRACELOOP_TELEMETRY'] = "false"
    os.environ["OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE"] = "delta"
    
    from traceloop.sdk import Traceloop
    
    token = read_secret(SECRET_NAME, region_name=SECRET_AWS_REGION)
    
    if not token:
        raise ValueError(f"Dynatrace API token not found in AWS Secrets Manager. Secret: {SECRET_NAME}, Region: {SECRET_AWS_REGION}")
    
    headers = {"Authorization": f"Api-Token {token}"}
    Traceloop.init(
        app_name="agentcore_basic_travel_agent",
        api_endpoint=OTEL_ENDPOINT,
        disable_batch=True,
        headers=headers,
        should_enrich_metrics=True,
    )
    