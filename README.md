# Google Jules API MCP Server

A Model Context Protocol (MCP) server for the Google Jules API (v1alpha). This server allows LLMs to interact with the Jules API to manage sessions, sources, and activities.

## Features

- **List Sources**: Fetch available repositories.
- **Create Session**: Start a new task with a user prompt.
- **List Sessions**: specific filtering and sorting options.
- **Send Message**: Send follow-up messages to an active session.
- **Approve Plan**: Approve a session's plan.
- **Get Activities**: Retrieve the history/activities of a session.

## Configuration

This server requires the `JULES_API_KEY` environment variable to be set. This key is used to authenticate requests to the Google Jules API.

## Installation

This project uses `uv` for dependency management, but can also be installed via pip.

```bash
pip install .
```

## Usage with MCP

To use this server with an MCP host (like Claude Desktop or other MCP clients), add the following configuration to your `mcp.json` (or `mcp_settings.json`):

### Example `mcp.json`

```json
{
  "mcpServers": {
    "jules": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/jules-mcp-server",
        "run",
        "jules-mcp-server"
      ],
      "env": {
        "JULES_API_KEY": "your-google-jules-api-key"
      }
    }
  }
}
```

*Note: Replace `/path/to/jules-mcp-server` with the actual absolute path to this repository, and `your-google-jules-api-key` with your actual API key.*

Alternatively, if you have installed the package into a virtual environment or globally:

```json
{
  "mcpServers": {
    "jules": {
      "command": "python3",
      "args": [
        "-m",
        "main"
      ],
      "env": {
        "JULES_API_KEY": "your-google-jules-api-key"
      }
    }
  }
}
```

## Tools

### `list_sources`
Fetches available repositories.

### `create_session`
Starts a new task.
- `source`: The resource name of the source repository.
- `user_prompt`: The initial user prompt.

### `list_sessions`
Lists sessions.
- `orderBy_recent`: (bool, default=True) Sort by creation time descending.
- `active_only`: (bool, default=True) Filter out COMPLETED or FAILED sessions.

### `send_message`
Follow up in an active session.
- `session_name`: The resource name of the session.
- `message`: The message content.

### `approve_plan`
Approves a session's plan.
- `session_name`: The resource name of the session.

### `get_activities`
Retrieves session history.
- `session_name`: The resource name of the session.
