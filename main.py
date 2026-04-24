from app.graph.workflow import build_graph
from app.utils.memory import save_memory
from app.utils.vector_store import save_to_vector_store
from app.utils.logger import setup_logger


def main():
    logger = setup_logger()

    app = build_graph()

    user_input = "Analyze sales data and generate report"

    input_data = {
        "user_input": user_input,
        "retries": 0
    }

    logger.info(f"START TASK: {user_input}")

    result = app.invoke(input_data)

    print("\n========== FINAL OUTPUT ==========")
    print(result)

    print("\n========== STATUS ==========")
    print("FINAL STATUS:", result.get("status"))
    print("RETRY COUNT:", result.get("retries"))

    # 🔹 Logging details
    logger.info(f"PLAN: {result.get('plan')}")
    logger.info(f"RESULTS: {result.get('results')}")
    logger.info(f"STATUS: {result.get('status')}")
    logger.info(f"RETRIES: {result.get('retries')}")

    # 🔹 Save structured memory
    save_memory({
        "task": user_input,
        "plan": result.get("plan"),
        "status": result.get("status")
    })

    # 🔹 Save vector memory
    save_to_vector_store(
        text=f"Task: {user_input}\nPlan: {result.get('plan')}\nStatus: {result.get('status')}",
        metadata={"status": result.get("status")}
    )

    logger.info("END TASK\n")


if __name__ == "__main__":
    main()