"""Admin database tools for Pydantic AI agents using the MCP postgres server.

This module provides admin-only access to the postgres database through the MCP alchemy server.
"""

from django.conf import settings
from pydantic_ai.mcp import MCPServerStdio

from apps.ai.permissions import tool_requires_superuser


def get_database_url():
    """Convert Django DATABASES setting back to a connection string."""
    db_config = settings.DATABASES["default"]

    engine = db_config["ENGINE"]
    name = db_config["NAME"]
    user = db_config["USER"]
    password = db_config["PASSWORD"]
    host = db_config["HOST"]
    port = db_config["PORT"]

    # Map Django engines to URL schemes
    if "postgresql" in engine:
        scheme = "postgresql"
    elif "mysql" in engine:
        scheme = "mysql"
    elif "sqlite" in engine:
        return f"sqlite:///{name}"
    else:
        scheme = "postgresql"  # default fallback

    return f"{scheme}://{user}:{password}@{host}:{port}/{name}"


admin_db = MCPServerStdio(
    command="uvx",
    args=[
        "--from",
        "mcp-alchemy==2025.8.15.91819",
        "--with",
        "psycopg2-binary",
        "--refresh-package",
        "mcp-alchemy",
        "mcp-alchemy",
    ],
    env={
        "DB_URL": get_database_url(),
    },
    process_tool_call=tool_requires_superuser,
)
