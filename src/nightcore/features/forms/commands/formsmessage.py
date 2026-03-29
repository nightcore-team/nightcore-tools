"""Sent forms message command."""

from typing import TYPE_CHECKING

from discord import app_commands
from discord.ext.commands import Cog  # type: ignore
from discord.interactions import Interaction

from src.nightcore.features.forms.components.view import FormView

if TYPE_CHECKING:
    from src.nightcore.bot import NightcoreTools


class FormsMessage(Cog):
    def __init__(self):
        super().__init__()

    @app_commands.command(
        name="forms_message",
        description="Sends the forms message in the current channel.",
    )
    @app_commands.choices(
        form_type=[
            app_commands.Choice(name="Мафия", value="mafia"),
            app_commands.Choice(name="Гетто", value="ghetto"),
        ],
    )
    @app_commands.rename(form_type="тип")
    @app_commands.checks.has_permissions(administrator=True)
    async def forms_message(
        self,
        interaction: Interaction["NightcoreTools"],
        form_type: app_commands.Choice[str],
    ) -> None:
        """Sends the forms message in the current channel."""

        view = FormView(type=form_type.value)

        await interaction.channel.send(view=view)  # type: ignore

        await interaction.response.send_message(
            "Сообщение с формами успешно отправлено!", ephemeral=True
        )


async def setup(bot: "NightcoreTools") -> None:
    """Setup the FormsMessage cog."""
    await bot.add_cog(FormsMessage())
