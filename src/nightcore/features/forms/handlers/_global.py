"""Global handlers for forms."""

from typing import TYPE_CHECKING

from discord.interactions import Interaction

from .button import handle_forms_button, handle_forms_insert_button
from .modal import handle_registration_modal_submit

if TYPE_CHECKING:
    from src.nightcore.bot import NightcoreTools


async def global_forms_handler(
    interaction: Interaction["NightcoreTools"], custom_id: str
) -> None:

    try:
        prefix, type, action = custom_id.split(":")
    except ValueError:
        return

    match prefix:
        case "forms":
            if action == "insert":
                await handle_forms_insert_button(interaction, type)
            match type:
                case "ghetto":
                    await handle_forms_button(interaction, type, action)
                case "mafia":
                    await handle_forms_button(interaction, type, action)
                case _:
                    return

        case "forms_modal":
            await handle_registration_modal_submit(interaction, type)
        case _:
            return
