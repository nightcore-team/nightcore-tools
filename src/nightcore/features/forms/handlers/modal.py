"""Forms handlers."""

import logging
from typing import TYPE_CHECKING, cast

from discord import Guild
from discord.interactions import Interaction

from nightcore.utils.object import ensure_member_exists, ensure_role_exists
from src.nightcore.features.forms.components.view import SentFormView
from src.nightcore.features.forms.constants import (
    GLOBAL_DEPUTY_ILLEGAL_ROLE_ID,
    TITLE_DICTIONARY,
)
from src.nightcore.features.forms.utils.parse import (
    parse_author_id_from_components,
    parse_form_text_from_components,
)

if TYPE_CHECKING:
    from src.nightcore.bot import NightcoreTools

logger = logging.getLogger(__name__)


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
        view=SentFormView(
            title=TITLE_DICTIONARY.get(type, "Анкета"),
            form_text=form,
            type=type,
            author_id=interaction.user.id,
        )
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

    title = TITLE_DICTIONARY.get(type, "Анкета")
    form_text = cast(
        str,
        parse_form_text_from_components(interaction.message.components),  # type: ignore
    )
    author_id = cast(
        int,
        parse_author_id_from_components(interaction.message.components),  # type: ignore
    )

    view = SentFormView(
        title=title,
        form_text=form_text,
        type=type,
        author_id=author_id,
        answer=reason,
        user_answer_id=interaction.user.id,
        status="Отклонено",
        disable_buttons=True,
    )

    await interaction.message.edit(view=view)  # type: ignore


async def handle_give_roles_modal_submit(
    interaction: Interaction["NightcoreTools"],
):
    """Handle the give roles modal submit button interaction."""

    await interaction.response.defer(ephemeral=True)
    guild = cast(Guild, interaction.guild)

    user_id = cast(
        int,
        int(interaction.data["components"][0]["components"][0]["value"]),  # type: ignore
    )
    organization_id = cast(
        int,
        int(interaction.data["components"][1]["components"][0]["value"]),  # type: ignore
    )

    member = await ensure_member_exists(guild, user_id)
    if not member:
        await interaction.followup.send(
            "Пользователь не найден в гильдии.", ephemeral=True
        )
        return

    has_role = any(
        role.id in (GLOBAL_DEPUTY_ILLEGAL_ROLE_ID, organization_id)
        for role in member.roles
    )

    if has_role:
        await interaction.followup.send(
            "Пользователь уже имеет эти роли.", ephemeral=True
        )
        return

    main_illegal_role = await ensure_role_exists(
        guild, GLOBAL_DEPUTY_ILLEGAL_ROLE_ID
    )
    if not main_illegal_role:
        await interaction.followup.send(
            "Роль для выдачи не найдена в гильдии.", ephemeral=True
        )
        return

    sub_illegal_role = await ensure_role_exists(guild, organization_id)
    if not sub_illegal_role:
        await interaction.followup.send(
            "Роль для выдачи не найдена в гильдии.", ephemeral=True
        )
        return

    try:
        await member.add_roles(
            main_illegal_role, sub_illegal_role, atomic=False
        )
    except Exception as e:
        logger.error("Failed to give roles: %s", e)
        await interaction.followup.send(
            "Не удалось выдать роли пользователю.", ephemeral=True
        )
        return

    await interaction.followup.send(
        f"Роли успешно выданы пользователю <@{user_id}>", ephemeral=True
    )
