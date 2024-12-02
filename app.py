from typing import TypedDict, Annotated, List
from langchain_core.messages import HumanMessage, AIMessage
from model import llm
from prompt import prompt

from langgraph.graph import StateGraph, END

from langchain_core.runnables.graph import MermaidDrawMethod
from IPython.display import display, Image

from PIL import Image
import io


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
    print
    return {
        **state,
        "interests": user_message,
        "messages": state['messages'] + [HumanMessage(content = user_message)]
        }
    
def create_itenary(state: PlannerState) -> PlannerState:
    print(f"Creating an itinerary for {state['city']} based on interests: {state['interests']}...")
    response = llm.invoke(prompt.format_messages(city = state['city'], interests=state['interests'] ))
    print(response.content)
    return {
        **state,
        "messages": state["messages"] + [AIMessage(content=response.content)],
        "itinerary": response.content,
    }
    
# creating and compiling the Graph
workflow = StateGraph(PlannerState)

workflow.add_node("input_city", input_city)
workflow.add_node("input_interests", input_interest)
workflow.add_node("create_itinerary", create_itenary)

workflow.set_entry_point("input_city")

workflow.add_edge("input_city", "input_interests")
workflow.add_edge("input_interests", "create_itinerary")
workflow.add_edge("create_itinerary",END)

app = workflow.compile()

image_data = app.get_graph().draw_mermaid_png(draw_method=MermaidDrawMethod.API)

# Save the image to a file
with open("graph_output.png", "wb") as file:
    file.write(image_data)

# Optionally open the image for viewing (requires Pillow)
img = Image.open(io.BytesIO(image_data))
img.show()

print("Graph image saved as 'graph_output.png'.")


# defining the function that runs the graph 

def run_travel_planner(user_request: str):
    print(f"Initial Request: {user_request} \n")
    state = {
         "messages": [HumanMessage(content=user_request)],
        "city": "",
        "interests": [],
        "itinerary": "",
    }
    for output in app.stream(state):
        pass 


    
user_request = "I want to plan a day trip"
run_travel_planner(user_request)



    