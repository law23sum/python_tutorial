from django.core.exceptions import PermissionDenied


def tool_requires_superuser(ctx, direct_call_tool, name, tool_args):
    """Check if the current user has admin access.

    Args:
        ctx: The run context containing user dependencies.
        direct_call_tool: The tool to call if authorized.
        name: Name of the tool being called.
        tool_args: Arguments for the tool call.

    Returns:
        The result of calling the tool if authorized.

    Raises:
        PermissionError: If user is not authorized.
    """
    # Get user from the context dependencies
    user = ctx.deps.user if hasattr(ctx, "deps") and hasattr(ctx.deps, "user") else None

    if not user or not (user.is_superuser and user.is_staff):
        raise PermissionDenied("Admin access required for database operations")

    return direct_call_tool(name, tool_args)
