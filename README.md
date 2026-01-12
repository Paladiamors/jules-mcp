# Jules MCP Server

A Model Context Protocol (MCP) server for the Google Jules API. This server enables LLM applications to interact with Jules - Google's AI coding assistant - to create sessions, send messages, and manage coding tasks programmatically.

## Features

- **List Sources**: Browse available GitHub repositories connected to Jules
- **Create Sessions**: Start new coding tasks with Jules
- **Send Messages**: Communicate with Jules during active sessions
- **Approve Plans**: Approve Jules's proposed plans before execution
- **List Activities**: View the work history and conversation for a session
- **Create Pull Requests**: Convenience tool to create sessions that result in PRs

## Prerequisites

- Python 3.10+
- A Jules API key (generate one from the [Jules Settings page](https://jules.google.com/settings))
- GitHub repositories installed in Jules

## Installation

### Using uv (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/jules-mcp.git
cd jules-mcp

# Install dependencies with uv
uv sync
```

### Using pip

```bash
# Clone the repository
git clone https://github.com/yourusername/jules-mcp.git
cd jules-mcp

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install fastmcp httpx pydantic
```

## Configuration

Set the `JULES_API_KEY` environment variable with your API key:

```bash
export JULES_API_KEY="your-api-key-here"
```

## Usage

### Running Standalone

```bash
# With uv
uv run python main.py

# With pip/venv
python main.py
```

### MCP Configuration

Add this server to your MCP client configuration. Below are examples for different setups.

#### Claude Desktop / Claude Code

Add to your `mcp.json` or `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "jules": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/jules-mcp",
        "run",
        "python",
        "main.py"
      ],
      "env": {
        "JULES_API_KEY": "your-jules-api-key"
      }
    }
  }
}
```

#### Alternative (without uv)

```json
{
  "mcpServers": {
    "jules": {
      "command": "/absolute/path/to/jules-mcp/.venv/bin/python",
      "args": [
        "/absolute/path/to/jules-mcp/main.py"
      ],
      "env": {
        "JULES_API_KEY": "your-jules-api-key"
      }
    }
  }
}
```

## Available Tools

### `list_sources`
List available GitHub repositories that Jules can work with.

**Parameters:**
- `page_size` (int, optional): Number of sources to return (1-100, default 30)
- `page_token` (str, optional): Pagination token

### `get_source`
Get details about a specific source repository.

**Parameters:**
- `source_name` (str, required): Resource name (e.g., "sources/github/owner/repo")

### `list_sessions`
List Jules sessions (coding tasks).

**Parameters:**
- `page_size` (int, optional): Number of sessions to return (1-100, default 30)
- `page_token` (str, optional): Pagination token
- `active_only` (bool, optional): Filter to only show active sessions

### `get_session`
Get details about a specific session.

**Parameters:**
- `session_name` (str, required): Resource name (e.g., "sessions/abc123")

### `create_session`
Create a new Jules session to work on a coding task.

**Parameters:**
- `prompt` (str, required): The coding task description
- `source` (str, required): Resource name of the repository
- `branch` (str, optional): Branch to use
- `title` (str, optional): Session title
- `require_plan_approval` (bool, optional): Wait for plan approval before executing

### `send_message`
Send a follow-up message to an active session.

**Parameters:**
- `session_name` (str, required): Resource name of the session
- `message` (str, required): Message to send

### `approve_plan`
Approve Jules's plan for a session in AWAITING_PLAN_APPROVAL state.

**Parameters:**
- `session_name` (str, required): Resource name of the session

### `list_activities`
List activities (work history) for a session.

**Parameters:**
- `session_name` (str, required): Resource name of the session
- `page_size` (int, optional): Number of activities to return (1-100, default 50)
- `page_token` (str, optional): Pagination token

### `create_pull_request`
Create a session that will result in a pull request.

**Parameters:**
- `prompt` (str, required): Description of changes to make
- `source` (str, required): Resource name of the repository
- `branch` (str, optional): Base branch for the PR
- `title` (str, optional): Title for the session/PR

## Session States

Sessions progress through these states:

- `QUEUED` - Session is waiting to start
- `PLANNING` - Jules is creating a plan
- `AWAITING_PLAN_APPROVAL` - Waiting for user to approve the plan
- `AWAITING_USER_FEEDBACK` - Waiting for user input
- `IN_PROGRESS` - Jules is working on the task
- `PAUSED` - Session is paused
- `FAILED` - Session failed
- `COMPLETED` - Session completed successfully

## Example Workflow

1. **List available repositories:**
   ```
   Use the list_sources tool to see which repos are available
   ```

2. **Create a coding task:**
   ```
   Use create_session with:
   - prompt: "Add a dark mode toggle to the settings page"
   - source: "sources/github/myorg/myrepo"
   ```

3. **Monitor progress:**
   ```
   Use get_session to check the session state
   Use list_activities to see what Jules is doing
   ```

4. **Interact with Jules:**
   ```
   Use send_message if Jules needs clarification
   Use approve_plan if plan approval is required
   ```

5. **Get the result:**
   ```
   Once session is COMPLETED, check the outputs field for PR URL
   ```

## API Reference

This server wraps the [Google Jules API (v1alpha)](https://developers.google.com/jules/api/reference/rest).

## License

MIT
