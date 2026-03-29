"""Discord-objects related utils."""

import logging

from discord import Guild, Member
from discord.errors import HTTPException, NotFound
from discord.role import Role

logger = logging.getLogger(__name__)


async def ensure_role_exists(guild: Guild, role_id: int) -> Role | None:
    """Ensure that a role with the given ID exists in the guild."""
    role = guild.get_role(role_id)
    if role is None:
        try:
            role = await guild.fetch_role(role_id)
        except NotFound as e:
            logger.error(
                "[ensure_role_exists] Role %s not found in guild %s: %s",
                role_id,
                guild.id,
                e,
            )
            return None
        except HTTPException as e:
            logger.error(
                "[ensure_role_exists] Failed refetching role %s in guild %s: %s",  # noqa: E501
                role_id,
                guild.id,
                e,
            )
            return None
    return role


async def ensure_member_exists(
    guild: Guild, user_id: int | None = None
) -> Member | None:
    """Ensure that a member with the given user ID exists in the guild."""

    if not user_id:
        return None

    member = guild.get_member(user_id)

    if member is None:
        try:
            logger.info("Refetching member %s in guild %s", user_id, guild.id)
            member = await guild.fetch_member(user_id)
        except NotFound as e:
            logger.info(
                "[ensure_member_exists] Member %s not found in guild %s: %s",
                user_id,
                guild.id,
                e,
            )
            return None
        except HTTPException as e:
            logger.error(
                "[ensure_member_exists] Failed refetching member %s in guild %s: %s",  # noqa: E501
                user_id,
                guild.id,
                e,
            )
            return None

    return member
