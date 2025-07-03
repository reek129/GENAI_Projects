from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain.agents import initialize_agent,tool
from langchain_community.tools import TavilySearchResults


load_dotenv()

import openai
import os

# openai.api_key = "YOUR_API_KEY"
# openai.api_key = os.getenv("OPENAI_API_KEY")
# models = openai.models.list()

# for model in models:
#     print(model.id)
import datetime

@tool
def get_system_time(format: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Returns the current date and time in the specified format.
    """
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime(format)
    return formatted_time

llm = ChatOpenAI(model="gpt-3.5-turbo")

search_tools = TavilySearchResults(search_depth="basic")
agent = initialize_agent(tools=[search_tools, get_system_time],llm=llm, verbose=True,agent="zero-shot-react-description")

result = agent.invoke("When was spaceX last launch? How many days ago did it happen? ")
# print(result)