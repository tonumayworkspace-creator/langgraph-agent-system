from app.utils.llm import get_llm

def planner_agent(user_input: str) -> str:
    llm = get_llm()

    prompt = f"""
You are a planning agent.

Break the task into clear numbered steps.

Task:
{user_input}

Plan:
"""

    response = llm.invoke(prompt)
    return response.content