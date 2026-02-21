"""Error event handlers."""

import logging
from typing import TYPE_CHECKING

from discord.app_commands import AppCommandError
from discord.errors import RateLimited
from discord.interactions import Interaction

if TYPE_CHECKING:
    from src.nightcore.bot import NightcoreTools

logger = logging.getLogger(__name__)


async def on_app_command_error(
    interaction: Interaction["NightcoreTools"],
    error: AppCommandError,
):
    """Handle errors for application commands."""

    original = getattr(error, "original", error)

    if isinstance(original, RateLimited):
        logger.warning(
            "%s handled guild=%s user=%s",
            original.__class__.__name__,
            interaction.guild.id if interaction.guild else "DM",
            interaction.user.id,
        )
        if not interaction.response.is_done():
            await interaction.response.send_message(
                f"Ошибка при обработке команды: слишком много запросов. Пожалуйста, попробуйте снова через: {original.retry_after} секунд.",  # noqa: E501
                ephemeral=True,
            )
        else:
            await interaction.response.send_message(
                f"Ошибка при обработке команды: слишком много запросов. Пожалуйста, попробуйте снова через: {original.retry_after} секунд.",  # noqa: E501
                ephemeral=True,
            )
        return


async def setup(bot: "NightcoreTools") -> None:
    """Setup the error event handlers."""
    bot.add_listener(on_app_command_error, "app_command_error")
