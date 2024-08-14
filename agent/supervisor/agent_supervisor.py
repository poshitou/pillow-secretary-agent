from dotenv import load_dotenv
from langchain_community.tools import TavilySearchResults
from langchain_core.messages import HumanMessage
from langchain_google_vertexai import ChatVertexAI
from langchain_openai import ChatOpenAI

from agent.utils.agent_util import build_supervisor

# Load the .env file
load_dotenv()

llm = ChatOpenAI(model="gpt-4-turbo")
# llm = ChatVertexAI(model="gemini-1.5-flash-001")

members = {
    "Researcher": {
        "llm": llm,
        "tools": [TavilySearchResults(max_results=5)],
        "prompt": "You are a web researcher."
    },
    "SqlGenerator": {
        "llm": llm,
        "tools": [],
        "prompt": "You are a SQL generator."
    }
}

supervisor = build_supervisor(llm, members)

user_inputs = {"messages": [HumanMessage(content="帮我写一个查询所有员工的SQL语句")]}

for s in supervisor.stream(user_inputs):
    if "__end__" not in s:
        print(s)
        print("----")
