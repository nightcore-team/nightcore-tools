"""Command to change status of Chief Administrator channel."""

from typing import TYPE_CHECKING, cast

from discord import (
    Guild,
    PermissionOverwrite,
    Role,
    VoiceChannel,
    app_commands,
)
from discord.ext.commands import Cog  # type: ignore
from discord.interactions import Interaction

if TYPE_CHECKING:
    from src.nightcore.bot import NightcoreTools

from src.nightcore.features.ga.constants import (
    ADMINISTRATOR_ROLES_IDS,
    CHIEF_ADMINISTRATOR_CHANNEL_DICT,
    CHIEF_ADMINISTRATOR_CHANNEL_ID,
    CHIEF_ADMINISTRATOR_CHANNEL_NAME,
    CHIEF_ADMINISTRATOR_ID,
)


class GA(Cog):
    def __init__(self, bot: "NightcoreTools") -> None:
        self.bot = bot

    CLOSE_EMOJI: str = CHIEF_ADMINISTRATOR_CHANNEL_DICT["close_emoji"]
    OPEN_EMOJI: str = CHIEF_ADMINISTRATOR_CHANNEL_DICT["open_emoji"]
    SEPARATOR: str = CHIEF_ADMINISTRATOR_CHANNEL_DICT["separator"]

    async def close_channel(
        self,
        channel: VoiceChannel,
        administrator_roles: list[Role],
    ):
        """Close the channel."""
        overwrites = channel.overwrites.copy()
        for role in administrator_roles:
            overwrites[role] = PermissionOverwrite(connect=False)

        new_name = (
            f"{self.CLOSE_EMOJI}{self.SEPARATOR}"
            f"{CHIEF_ADMINISTRATOR_CHANNEL_NAME}"
        )
        await channel.edit(overwrites=overwrites, name=new_name)

    async def open_channel(
        self,
        channel: VoiceChannel,
        administrator_roles: list[Role],
    ):
        """Open the channel."""
        overwrites = channel.overwrites.copy()
        for role in administrator_roles:
            overwrites[role] = PermissionOverwrite(connect=True)

        new_name = (
            f"{self.OPEN_EMOJI}{self.SEPARATOR}"
            f"{CHIEF_ADMINISTRATOR_CHANNEL_NAME}"
        )
        await channel.edit(overwrites=overwrites, name=new_name)

    @app_commands.command(
        name="ga", description="Открыть/закрыть голосовой канал ГА."
    )
    async def ga(self, interaction: Interaction):
        """Send a message displaying the bot's current latency."""

        guild = cast(Guild, interaction.guild)

        # check if user is GA
        if interaction.user.id != CHIEF_ADMINISTRATOR_ID:
            return await interaction.response.send_message(
                "У вас нет прав для использования этой команды.",
                ephemeral=True,
            )

        # check for needed permissions
        if not guild.me.guild_permissions.manage_channels:
            return await interaction.response.send_message(
                "У бота нет прав для управления каналами.",
                ephemeral=True,
            )

        # check if channel exists
        channel = guild.get_channel(CHIEF_ADMINISTRATOR_CHANNEL_ID)
        if not channel:
            return await interaction.response.send_message(
                "Канал не найден.", ephemeral=True
            )

        channel = cast(VoiceChannel, channel)

        administrator_roles = [
            cast(Role, guild.get_role(role_id))
            for role_id in ADMINISTRATOR_ROLES_IDS
            if guild.get_role(role_id) is not None
        ]

        channel_permissions = channel.overwrites

        if all(
            channel_permissions.get(
                role, PermissionOverwrite(connect=None)
            ).connect
            for role in administrator_roles
        ):
            # close
            await self.close_channel(channel, administrator_roles)
            await interaction.response.send_message(
                "Канал закрыт.", ephemeral=True
            )
        else:
            # open
            await self.open_channel(channel, administrator_roles)
            await interaction.response.send_message(
                "Канал открыт.", ephemeral=True
            )


async def setup(bot: "NightcoreTools"):
    """Setup the GA cog."""
    await bot.add_cog(GA(bot))
