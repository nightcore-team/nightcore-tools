"""Utils for permissions."""

from discord import Member

from src.nightcore.features.forms.constants import (
    GHETTO_ACCESS_ROLES,
    MAFIA_ACCESS_ROLES,
)


async def check_member_permissions(member: Member, type: str):
    """Check if the member has permissions for the given action."""

    match type:
        case "ghetto" | "territory":
            return any(role.id in GHETTO_ACCESS_ROLES for role in member.roles)
        case "mafia" | "business":
            return any(role.id in MAFIA_ACCESS_ROLES for role in member.roles)
        case _:
            return False
