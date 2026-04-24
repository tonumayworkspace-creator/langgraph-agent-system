from fastapi import FastAPI
from pydantic import BaseModel

from app.graph.workflow import build_graph
from app.utils.memory import save_memory
from app.utils.vector_store import save_to_vector_store
from app.utils.logger import setup_logger


app = FastAPI()
logger = setup_logger()

graph = build_graph()


class RequestModel(BaseModel):
    user_input: str


@app.post("/run-agent")
def run_agent(request: RequestModel):
    user_input = request.user_input

    logger.info(f"API CALL: {user_input}")

    input_data = {
        "user_input": user_input,
        "retries": 0
    }

    result = graph.invoke(input_data)

    # Save memory
    save_memory({
        "task": user_input,
        "plan": result.get("plan"),
        "status": result.get("status")
    })

    save_to_vector_store(
        text=f"Task: {user_input}\nPlan: {result.get('plan')}\nStatus: {result.get('status')}",
        metadata={"status": result.get("status")}
    )

    return {
        "plan": result.get("plan"),
        "results": result.get("results"),
        "status": result.get("status"),
        "retries": result.get("retries")
    }