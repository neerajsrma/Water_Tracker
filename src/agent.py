# from langchain.chat_models import init_chat_model
import os
from langchain.schema import HumanMessage
from dotenv import load_dotenv

load_dotenv()

from langchain.chat_models import init_chat_model

llm = init_chat_model(
    "groq:llama-3.1-8b-instant"
)   

class WaterIntakeAgent:
    def __init__(self):
        self.history = []

    def analyze_intake(self, intake_ml):
        prompt = f"""
        you are a hydration assistant. The user has consumed {intake_ml} ml of water today.
        provide a hydration status and suggest if they need to drink more water
        """

        response = llm.invoke([HumanMessage(content=prompt)])

        return response.content
    
if __name__ =="__main__":
    agent = WaterIntakeAgent()
    intake = 1500
    feedback = agent.analyze_intake(intake)
    print(f"Hydration Analysis : {feedback}")