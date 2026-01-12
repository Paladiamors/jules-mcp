import logging
import sys
from typing import List, Dict, Any
from mcp.server.fastmcp import FastMCP
from client import JulesClient

# Configure logging to stderr
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stderr
)
logger = logging.getLogger("jules-mcp")

# Initialize FastMCP server
mcp = FastMCP("jules-mcp")

# Initialize the Jules client
client = JulesClient()

@mcp.tool()
async def list_sources() -> List[Dict[str, Any]]:
    """
    Fetch available repositories (sources) from the Jules API.

    Returns:
        A list of source objects containing name, displayName, and branch.
    """
    logger.info("Executing list_sources")
    try:
        sources = await client.list_sources()
        return [s.model_dump() for s in sources]
    except Exception as e:
        logger.error(f"Error in list_sources: {e}")
        raise

@mcp.tool()
async def create_session(source: str, user_prompt: str) -> Dict[str, Any]:
    """
    Start a new task (session).

    Args:
        source: The resource name of the source repository (e.g., 'sources/my-repo').
        user_prompt: The initial instruction or prompt for the session.

    Returns:
        The created session object, including its resource name, ID, and initial state.
    """
    logger.info(f"Executing create_session with source='{source}'")
    try:
        session = await client.create_session(source, user_prompt)
        return session.model_dump()
    except Exception as e:
        logger.error(f"Error in create_session: {e}")
        raise

@mcp.tool()
async def list_sessions(order_by_recent: bool = True, active_only: bool = True) -> List[Dict[str, Any]]:
    """
    List sessions with optional filtering and sorting.

    Args:
        order_by_recent: If True, sort results by creation time (most recent first). Defaults to True.
        active_only: If True, filter results to only include sessions NOT in COMPLETED or FAILED states. Defaults to True.

    Returns:
        A list of session objects.
    """
    logger.info(f"Executing list_sessions(order_by_recent={order_by_recent}, active_only={active_only})")
    try:
        sessions = await client.list_sessions(order_by_recent=order_by_recent, active_only=active_only)
        return [s.model_dump() for s in sessions]
    except Exception as e:
        logger.error(f"Error in list_sessions: {e}")
        raise

@mcp.tool()
async def send_message(session_name: str, message: str) -> str:
    """
    Follow up in an active session with a message.

    Args:
        session_name: The resource name of the session (e.g., 'sessions/12345').
        message: The message content to send.

    Returns:
        A confirmation string. Use get_activities to see the agent's response.
    """
    logger.info(f"Executing send_message for session='{session_name}'")
    try:
        await client.send_message(session_name, message)
        return "Message sent successfully. Call get_activities to view the response."
    except Exception as e:
        logger.error(f"Error in send_message: {e}")
        raise

@mcp.tool()
async def approve_plan(session_name: str) -> Dict[str, Any]:
    """
    Approve a session's plan.

    Args:
        session_name: The resource name of the session.

    Returns:
        The response from the API.
    """
    logger.info(f"Executing approve_plan for session='{session_name}'")
    try:
        result = await client.approve_plan(session_name)
        return result
    except Exception as e:
        logger.error(f"Error in approve_plan: {e}")
        raise

@mcp.tool()
async def get_activities(session_name: str) -> List[Dict[str, Any]]:
    """
    Retrieve session history (activities).

    Args:
        session_name: The resource name of the session.

    Returns:
        A list of activity objects associated with the session. Each activity contains details such as
        agent messages, user messages, generated plans, or progress updates.
    """
    logger.info(f"Executing get_activities for session='{session_name}'")
    try:
        activities = await client.get_activities(session_name)
        return [a.model_dump() for a in activities]
    except Exception as e:
        logger.error(f"Error in get_activities: {e}")
        raise

if __name__ == "__main__":
    mcp.run()
