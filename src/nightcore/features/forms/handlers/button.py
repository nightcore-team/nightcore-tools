"""Button handlers for forms."""

from typing import TYPE_CHECKING, cast

from discord import Message
from discord.interactions import Interaction

from src.nightcore.features.forms.components.modal import FormModal
from src.nightcore.features.forms.components.view import SentFormView

if TYPE_CHECKING:
    from src.nightcore.bot import NightcoreTools


async def handle_forms_button(
    interaction: Interaction["NightcoreTools"], action: str
) -> None:
    """Handle forms button interaction."""

    message = cast(Message, interaction.message)

    match action:
        case "approve":
            view = cast(SentFormView, SentFormView.from_message(message))
            _view = SentFormView(
                form_text=view.form_text,  # type: ignore
                type=view.type,  # type: ignore
                status="Одобрено",
                disable_buttons=True,
                author_id=view.author_id,  # type: ignore
            )

            await interaction.response.edit_message(view=_view)

        case "reject":
            view = cast(SentFormView, SentFormView.from_message(message))
            _view = SentFormView(
                form_text=view.form_text,  # type: ignore
                type=view.type,  # type: ignore
                status="Отклонено",
                disable_buttons=True,
                author_id=view.author_id,  # type: ignore
            )

            await interaction.response.edit_message(view=_view)

        case _:
            return


async def handle_forms_insert_button(
    interaction: Interaction["NightcoreTools"], type: str
) -> None:
    """Handle forms insert button interaction."""

    await interaction.response.send_modal(FormModal(type=type))
