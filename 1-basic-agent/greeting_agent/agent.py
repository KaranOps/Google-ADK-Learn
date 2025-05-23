from google.adk.agents import Agent

root_agent = Agent(
    name="greeting_agent",
    model = "gemini-2.0-flash",
    description="Greeting Agent",
    instruction="""
    You are a helfful assistant that greets the user.
    Ask for the user's name and greet them by name.
    """,
)