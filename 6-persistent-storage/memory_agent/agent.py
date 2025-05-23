from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext


def add_reminder(reminder: str, tool_context: ToolContext) -> dict:
    """Add a new reminder to the user's list.

    Args:
        reminder: The reminder text to add
        tool_context: Context for accessing and updating session state

    Returns:
        A confirmation message
    """

    print(f"--- Tool: add_reminder called for '{reminder}' ---")

    # Get the current reminders from the state
    reminders = tool_context.state.get("reminders", [])

    # Add the new reminder to the list
    reminders.append(reminder)

    #update state with the new list of reminders
    tool_context.state["reminders"] = reminders

    return {
        "action": "add_reminder",
        "reminder": reminder,
        "message:" : f"Added reminder: '{reminder}'",
    }

def view_reminders(tool_context: ToolContext) -> dict:
    """View all current reminders.

    Args:
        tool_context: Context for accessing session state
    Returns:
        The list of reminders
    """
    print("--- Tool: view_reminders called ---")

    #get the reminders from the state
    reminders = tool_context.state.get("reminders", [])

    return {"action": "view_reminders", "reminders": reminders, "count": len(reminders)}

def update_reminder(index: int, updated_text: str, tool_context: ToolContext) -> dict:
    """Update an exising reminder.

    Args:
        index: The 1-based index of the reminder to update
        updated_text: The new text for the reminder
        tool_context: Context for accessing and updating session state
    Returns:
        A confirmation message
    """
    print(
        f"--- Tool: update_reminder called for index {index} with text '{updated_text}' ---"    
    )

    # Get the current reminders from the state
    reminders = tool_context.state.get("reminders", [])

    # Check if the index is valid
    if not reminders or index < 1 or index > len(reminders):
        return {
            "action" : "update_reminder",
            "status": "error",
            "message": f"Could not find the reminder at index {index}. Currently their are {len(reminders)} reminders.",
        }
    
    # Update the reminder (adjusting for 0-based index)
    old_reminder = reminders[index-1]
    reminders[index-1] = updated_text

    #update state with modified list
    tool_context.state["reminders"] = reminders

    return {
        "action": "update_reminder",
        "index": index,
        "old_reminder": old_reminder,
        "updated_text": updated_text,
        "message": f"Updated reminder at index {index} from '{old_reminder}' to '{updated_text}'",
    }

def delete_reminder(index: int, tool_context: ToolContext) -> dict:
    """Delete a reminder.

    Args:
        index: The 1-based index of the reminder to delete
        tool_context: Context for accessing and updating session state

    Returns:
        A confirmation message 
    """
    print(f"--- Tool: delete_reminder called for index {index} ---")

    # Get the current reminders from the state
    reminders = tool_context.state.get("reminders", [])

    # Check if the index is valid
    if not reminders or index < 1 or index > len(reminders):
        return {
            "action": "delete_reminder",
            "status": "error",
            "message": f"Could not find the reminder at index {index}. Currently their are {len(reminders)} reminders.",
        }
    # Delete the reminder (adjusting for 0-based index)
    deleted_reminder = reminders.pop(index-1)

    # Update the state with the modified list
    tool_context.state["reminders"] = reminders

    return {
        "action": "delete_reminder",
        "index": index,
        "deleted_reminder": deleted_reminder,
        "message": f"Deleted reminder at index {index}: '{deleted_reminder}'",
    }

def update_user_name(user_name: str, tool_context: ToolContext) -> dict:
    """Update the user's name.
    
    Args:
        user_name: The new name for the user
        tool_context: Context for accessing and updating session state
    Returns:
        A confirmation message
    """
    print(f"--- Tool: update_user_name called for '{user_name}' ---")

    #Get the current user name from the state
    old_name = tool_context.state.get("user_name", "")

    # Update the user's name in the state
    tool_context.state["user_name"] = user_name
    return {
        "action": "update_user_name",
        "old_name": old_name,
        "new_name": user_name,
        "message": f"Updated user name from '{old_name}' to '{user_name}'",
    }





#Create a simple persistent agent
memory_agent = Agent(
    name="memory_agent",
    model="gemini-2.0-flash",
    description="A smart reminder agent with persistent memory.",
    instruction=""""
    You are a friendly reminder assistant that remembers users across conversations.

    The user's information is stored in state:
    - User's name : {user_name}
    - Reminders : {reminders}

    You can help users manage their reminders with the following capabilities:
    1. Add new reminders.
    2. View existing reminders.
    3. Update reminders.
    4. Delete reminders.
    5. Update the user's name.

    Alwaya be friendly and address the user by their name. If you don't know their name yet,
    use the update_user_name tool to store it when they introduce themselves.

    **REMINDER MANAGEMENT GUIDELINES:**

    When dealing with reminders, you need to be smart about finding the right reminder:

    1. When the user asks to update or delete a reminder but doesn't provide an index:
        - If they mention the content of the reminder (e.g., "delete my meeting reminder"),
        look through the reminders to find a match
        - If you find an exact or close match, use that index
        - Never clarify which reminder the user is referring to, kust use the first match
        - If no match is found, list all reminders and ask the user to specify
    
    2. When the user mention a number or position:
        - Use that as the index (e.g., "delete reminder 2" means index 2)
        - Remember that indexing starts at 1 for the user
    
    3. For relative positions:
        - Handle "first", "last", "second", etc. appropriately
        - "First reminder" = index 1
        - "Last reminder" = the highest index
        - "Second reminder" = index 2 and so on
    
    4. For viewing:
        - Always use the view_reminders tool when the user asks to see their reminders
        - Format the response in a numbered list for clarity
        - If their are no reminders, suggest adding some
    
    5. For addition:
        - Extract the actual reminder text from the user's request
        - Remove the phrases like "add a reminder to" or "remind me to"
        - Focus on the task itself (e.g., "add a reminder to call mom" -> add_reminder("call mom"))
    
    6. For updates:
        - Identify both which reminder to update and what the new text should be
        - For example, "change my second reminder to pick up groceries" → update_reminder(2, "pick up groceries")
    
    7. For deletion:
        - Confirm deletion when complete and mention which reminder was removed
        - For example, "I've deleted your reminder to 'buy milk'"
    
    Remember to explain that you can remember their infomation across conversations

    IMPORTANT:
    - use you best judgement to determine which reminder the user is referring to.
    - You don't have to be 100% correct, but try to be as close as possible.
    - Never ask the user to clarify which reminder they are referring to.
    """,
    tools=[
        add_reminder,
        view_reminders,
        update_reminder,
        delete_reminder,
        update_user_name,   
    ],

)