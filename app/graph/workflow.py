from langgraph.graph import StateGraph, END
from typing import TypedDict

from app.agents.planner import planner_agent
from app.agents.executor import executor_agent
from app.agents.validator import validator_agent


class AgentState(TypedDict):
    user_input: str
    plan: str
    results: list
    status: str
    retries: int


# Nodes
def planner_node(state: AgentState):
    plan = planner_agent(state["user_input"])
    return {"plan": plan, "retries": 0}


def executor_node(state: AgentState):
    results = executor_agent(state["plan"])
    return {"results": results}


def validator_node(state: AgentState):
    status = validator_agent(state["results"])
    return {"status": status}


# 🔥 Conditional routing with retry control
def route_decision(state: AgentState):
    if state["status"] == "SUCCESS":
        return "end"

    if state["retries"] >= 2:
        return "fail"

    return "retry"


# 🔁 Retry node (increments counter)
def retry_node(state: AgentState):
    return {"retries": state["retries"] + 1}


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("planner", planner_node)
    graph.add_node("executor", executor_node)
    graph.add_node("validator", validator_node)
    graph.add_node("retry_handler", retry_node)

    graph.set_entry_point("planner")

    graph.add_edge("planner", "executor")
    graph.add_edge("executor", "validator")

    graph.add_conditional_edges(
        "validator",
        route_decision,
        {
            "end": END,
            "retry": "retry_handler",
            "fail": END
        }
    )

    graph.add_edge("retry_handler", "executor")

    return graph.compile()