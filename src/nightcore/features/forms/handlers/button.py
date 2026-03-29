"""Button handlers for forms."""

from typing import TYPE_CHECKING, cast

from discord import Message
from discord.interactions import Interaction

from nightcore.features.forms.constants import TITLE_DICTIONARY
from src.nightcore.features.forms.components.modal import (
    InsertFormModal,
    RejectFormModal,
)
from src.nightcore.features.forms.components.view import SentFormView
from src.nightcore.features.forms.utils.parse import (
    parse_author_id_from_components,
    parse_form_text_from_components,
)

if TYPE_CHECKING:
    from src.nightcore.bot import NightcoreTools


async def handle_forms_button(
    interaction: Interaction["NightcoreTools"], type: str, action: str
) -> None:
    """Handle forms button interaction."""

    message = cast(Message, interaction.message)

    match action:
        case "approve":
            title = TITLE_DICTIONARY.get(type, "Анкета")
            form_text = cast(
                str, parse_form_text_from_components(message.components)
            )
            author_id = cast(
                int, parse_author_id_from_components(message.components)
            )

            view = SentFormView(
                title=title,
                form_text=form_text,
                type=type,
                author_id=author_id,
                status="Одобрено",
                disable_buttons=True,
            )

            await interaction.response.edit_message(view=view)

        case "reject":
            await interaction.response.send_modal(RejectFormModal(type=type))

        case _:
            return


async def handle_forms_insert_button(
    interaction: Interaction["NightcoreTools"], type: str
) -> None:
    """Handle forms insert button interaction."""

    await interaction.response.send_modal(InsertFormModal(type=type))
