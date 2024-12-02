from typing import TypedDict, Annotated, List
from langchain_core.messages import HumanMessage, AIMessage
from model import llm
from prompt import prompt

from langgrapph.graph import StateGraph, END

from langchain_core.runnables.graph import MermaidDrawMethod
from IPython.display import display, Image


# defining the agent state
class PlannerState(TypedDict):
    messages: Annotated[List[HumanMessage | AIMessage], "The messages in the conversation"]
    city: str
    interests: List[str]
    itinerary: str
    
    
# defining agent functions 
def input_city(state: PlannerState) -> PlannerState:
    print("Please enter the city you want to visit for your day trip:")
    user_message = input("your input: ")
    return {
        **state, 
        "city": user_message,
        "messages": state['messages'] + [HumanMessage(content = user_message)]
    }


def input_interest(state: PlannerState) -> PlannerState:
    print(f" Please enter your interests for the trip to {state['city']} ")
    user_message = input("enter your interests")
    return {
        **state,
        "interests": [interest.strip() for interest in user_message],
        "messages": state['messages'] + [HumanMessage(content = user_message)]
        }
    
def create_itenary(state: PlannerState) -> PlannerState:
    print(f"Creating an itinerary for {state['city']} based on interests: {', '.join(state['interests'])}...")
    response = llm.invoke(prompt.format_messages(city = state['city'], interests=", ".join(state['interests']) ))
    print(response.content)
    return {
        **state,
        "messages": state["messages"] + [AIMessage(content=response.content)],
        "itinerary": response.content,
    }
    
    
    
    