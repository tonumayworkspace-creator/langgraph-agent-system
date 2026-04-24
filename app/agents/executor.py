from app.utils.llm import get_llm
from app.tools.tools import TOOLS


def executor_agent(plan: str):
    llm = get_llm()

    tool_list = ", ".join(TOOLS.keys())

    prompt = f"""
You are an AI executor.

Available tools:
{tool_list}

Your job:
- Read the plan
- Decide which tools to call
- Return ONLY a comma-separated list of tool names

Example output:
load_data, analyze_data, generate_report

Plan:
{plan}

Tools to use:
"""

    response = llm.invoke(prompt)
    tool_names = response.content.strip().lower().replace(" ", "").split(",")

    results = []

    for tool in tool_names:
        if tool in TOOLS:
            results.append(TOOLS[tool]())

    return results