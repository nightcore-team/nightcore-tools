"""Forms handlers."""

from typing import TYPE_CHECKING, cast

from discord.interactions import Interaction

from src.nightcore.features.forms.components.view import SentFormView
from src.nightcore.features.forms.utils.parse import (
    parse_author_id_from_components,
    parse_form_text_from_components,
)

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


async def handle_reject_modal_submit(
    interaction: Interaction["NightcoreTools"],
    type: str,
):
    """Handle the reject modal submit button interaction."""

    await interaction.response.defer(ephemeral=True)

    reason = cast(
        str,
        interaction.data["components"][0]["components"][0]["value"],  # type: ignore
    )

    form_text = parse_form_text_from_components(interaction.message.components)  # type: ignore
    author_id = parse_author_id_from_components(interaction.message.components)  # type: ignore

    view = SentFormView(
        form_text=form_text,  # type: ignore
        type=type,
        author_id=author_id,  # type: ignore
        answer=reason,
        user_answer_id=interaction.user.id,
        status="Отклонено",
        disable_buttons=True,
    )

    await interaction.message.edit(view=view)  # type: ignore
