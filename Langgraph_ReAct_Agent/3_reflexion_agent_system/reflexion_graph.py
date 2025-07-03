from typing import List

from langchain_core.messages import BaseMessage, ToolMessage,HumanMessage
from langgraph.graph import END, MessageGraph

# from dotenv import load_dotenv
# load_dotenv()

from chains import revisor_chain, first_responder_chain
from execute_tools import execute_tools

graph = MessageGraph()
MAX_ITERATIONS = 2

graph.add_node("draft", first_responder_chain)
graph.add_node("execute_tools", execute_tools)
graph.add_node("revisor", revisor_chain)

graph.add_edge("draft","execute_tools")
graph.add_edge("execute_tools","revisor")

def event_loop(state: List[BaseMessage]) -> str:
    count_tool_visits = sum(isinstance(item, ToolMessage) for item in state)
    num_iterations = count_tool_visits
    if num_iterations > MAX_ITERATIONS:
        return END
    return "execute_tools"

# def event_loop(state: List[BaseMessage]) -> str:
#     print("=== Event Loop ===")
#     # for msg in state:
#     #     print(type(msg), msg)
#     # Check if the latest message includes tool_calls (i.e., tool hasn't been invoked yet)
#     last_msg = state[-1]
#     if hasattr(last_msg, "tool_calls") and last_msg.tool_calls:
#         return "execute_tools"

#     # Count how many times tools have been run so far
#     count_tool_visits = sum(isinstance(item, ToolMessage) for item in state)
#     if count_tool_visits >= MAX_ITERATIONS:
#         return END

#     return "execute_tools"

graph.add_conditional_edges("revisor",event_loop)
graph.set_entry_point("draft")

app = graph.compile()

print(app.get_graph().draw_mermaid())

# response = app.invoke("Write about how small business can leverage AI to grow")
response = app.invoke([
    HumanMessage(content="Write about how small business can leverage AI to grow")
])

print(response[-1].tool_calls[0]["args"]["answer"])
print(response,"response")