from app.utils.llm import get_llm
from app.utils.vector_store import search_similar


def planner_agent(user_input: str) -> str:
    llm = get_llm()

    similar_tasks = search_similar(user_input)

    memory_text = "\n".join(similar_tasks)

    prompt = f"""
You are a planning agent.

Use similar past tasks to improve your plan.

Similar Tasks:
{memory_text}

Current Task:
{user_input}

Generate a concise numbered plan.
"""

    response = llm.invoke(prompt)
    return response.content