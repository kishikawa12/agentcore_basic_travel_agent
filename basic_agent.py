from dynatrace import init
init()

from travel_agent import agent_invocation, run_agent_with_task
from bedrock_agentcore import BedrockAgentCoreApp

app = BedrockAgentCoreApp()

@app.entrypoint
def invoke(payload):
    user_message = payload.get("prompt", "Hello! How can I help you today?")
    result = agent_invocation(user_message)
    return {"result": result.get("result")}

if __name__ == "__main__":
    app.run()