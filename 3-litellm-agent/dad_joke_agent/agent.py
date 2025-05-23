import os
import random

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

model = LiteLlm(
    model="openrouter/openai/gpt-4.1",
    api_key = os.getenv("OPENROUTER_API_KEY"),
)

def get_dad_joke():
    jokes = [
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "I told my wife she was drawing her eyebrows too high. She looked surprised.",
        "Why don't skeletons fight each other? They don't have the guts.",
        "I'm on a whiskey diet. I've lost three days already.",
        "I used to play piano by ear, but now I use my hands.",
    ]
    return random.choice(jokes)

root_agent = Agent(
    name="dad_joke_agent",
    model=model,
    description="Dad Joke Agent",
    instruction="""
    You are a helpful assistant that can tell dad jokes.
    Only use the tool `get_dad_joke` to tell joke.
    """,
    tools=[get_dad_joke],
)