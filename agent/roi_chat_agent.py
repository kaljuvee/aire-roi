import os
from typing import Annotated, Any, Dict, List, Optional, Sequence, TypedDict, Union, Literal
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode
from langchain_mistralai.chat_models import ChatMistralAI
from langgraph.checkpoint.memory import MemorySaver
import json
import logging
from dotenv import load_dotenv
from agent.tools import calculate_roi, calculate_inflation_adjusted_cash_flows, search_roi_examples

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize Mistral client
model = ChatMistralAI(
    model="mistral-large-latest",
    temperature=0.1,
    api_key=os.getenv("MISTRAL_API_KEY")
)

# Define the state
class MessagesState(TypedDict):
    messages: List[BaseMessage]

# Load system prompt
def load_system_prompt():
    try:
        with open('prompts/system_prompt.md', 'r') as file:
            return file.read().strip()
    except Exception as e:
        logger.error(f"Error loading system prompt: {str(e)}")
        return "You are an AI ROI calculation assistant specialized in helping businesses evaluate investments in AI and robotics solutions."

# Initialize tools
tools = [calculate_roi, calculate_inflation_adjusted_cash_flows, search_roi_examples]
tool_node = ToolNode(tools)

# Initialize the model with tools
model = model.bind_tools(tools)

# Define routing logic
def should_continue(state: MessagesState) -> Literal["tools", END]:
    """Determine if we should continue using tools or end the conversation."""
    messages = state['messages']
    last_message = messages[-1]
    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        return "tools"
    return END

# Define model calling logic
def call_model(state: MessagesState):
    """Call the model with the current state."""
    messages = state['messages']
    
    # Add system message if not present
    if not any(isinstance(msg, SystemMessage) for msg in messages):
        messages = [SystemMessage(content=load_system_prompt())] + messages
    
    response = model.invoke(messages)
    return {"messages": [response]}

# Create and configure the graph
workflow = StateGraph(MessagesState)

# Add nodes
workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)

# Add edges
workflow.add_edge(START, "agent")
workflow.add_conditional_edges(
    "agent",
    should_continue,
)
workflow.add_edge("tools", "agent")

# Initialize memory
checkpointer = MemorySaver()

# Compile the graph
agent = workflow.compile(checkpointer=checkpointer)

# Export the agent
__all__ = ['agent'] 