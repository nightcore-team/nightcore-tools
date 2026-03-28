"""Forms handlers."""

from typing import TYPE_CHECKING, cast

from discord.interactions import Interaction

from src.nightcore.features.forms.components.view import SentFormView

if TYPE_CHECKING:
    from src.nightcore.bot import NightcoreTools


async def handle_registration_modal_submit(
    interaction: Interaction["NightcoreTools"],
    type: str,
):
    """Handle the registration modal submit button interaction."""

    await interaction.response.defer(ephemeral=True)

    form = cast(
        str,
        interaction.data["components"][0]["components"][0]["value"],  # type: ignore
    )

    await interaction.followup.send(
        view=SentFormView(form, type=type, author_id=interaction.user.id)
    )
