from google.adk.agents import Agent
from pydantic import BaseModel, Field

#--- Define Output Schema ---
class EmailContent(BaseModel):
    subject: str = Field(
        description="The subject line of the email. Should be concise and descriptive."
    )
    body: str = Field(
        description="The main content of the email. Should be well-fromatted with proper greeting, paragraphs and signature"
    )

#--- Create Email Generator Agent ---
root_agent = Agent(
    name="email_agent",
    model="gemini-2.0-flash",
    instruction="""
        You are an email Generator Assistant.
        Your task is to generate professional email based on the user's request.
        
        GUIDELINES:
        - Create an appropriate subject line (concise and relevant)
        - Write a well-structured email body with:
            * Professional greeting
            * Clear and concise main content
            * Appropriate closing
            * Your name as Signature
        - Suggest relevant attachements if applicable (empty list if none needed)
        - Email tone should be match the purpose (formal for business, friendly for colleageues)
        - Keep email concise but complete
        
        IMPORTANT: Your response must be  valid JSON matching this structure:
        {
            "subject": "Subject line here",
            "body": "Email body here with proper paragraphs and formatting",
            }
        
        DO NOT include any explanation or additional text outside the JSON response.
        """,
        description="Generate professional email with structured subject and body",
        output_schema=EmailContent,
        output_key="email"
)