"""Form V2 view component."""

from datetime import UTC, datetime
from typing import Self, cast

from discord import ButtonStyle, Color, Interaction, Member
from discord.ui import (
    ActionRow,
    Button,
    Container,
    LayoutView,
    Separator,
    TextDisplay,
)

from src.nightcore.features.forms.constants import FORM_TEXT
from src.nightcore.features.forms.utils.permissions import (
    check_member_permissions,
)
from src.nightcore.utils.time import discord_ts


class FormView(LayoutView):
    def __init__(self, type: str) -> None:
        super().__init__(timeout=None)

        """Build the form view layout."""

        container = Container[Self]()

        container.add_item(
            TextDisplay(
                "## Анкета на пост заместителя нелегальных организаций"
            )
        )
        container.add_item(Separator())

        container.add_item(
            TextDisplay(f"### Форма для заполнения:\n```{FORM_TEXT}```")
        )
        container.add_item(
            TextDisplay(
                "-# Нажмите на кнопку ниже, чтобы вставить заполненную анкету."
            )
        )
        container.add_item(Separator())

        container.add_item(
            ActionRow(
                Button[Self](
                    label="Вставить анкету",
                    style=ButtonStyle.secondary,
                    custom_id=f"forms:{type}:insert",
                )
            )
        )

        self.add_item(container)


class SentFormView(LayoutView):
    def __init__(
        self,
        form_text: str,
        type: str,
        author_id: int,
        status: str = "На рассмотрении",
        user_answer_id: int | None = None,
        answer: str | None = None,
        disable_buttons: bool = False,
    ) -> None:
        super().__init__(timeout=None)

        self.type = type

        """Build the sent form view layout."""
        accent_color = None
        if status == "Одобрено":
            accent_color = Color.green()
        elif status == "Отклонено":
            accent_color = Color.red()
        container = Container[Self](accent_color=accent_color)
        container.add_item(
            TextDisplay(
                "## Анкета на пост заместителя нелегальных организаций"
            )
        )
        container.add_item(TextDisplay(f"> Автор: <@{author_id}>"))
        container.add_item(Separator())
        container.add_item(TextDisplay(f"```{form_text}```"))
        container.add_item(Separator())

        container.add_item(
            ActionRow(
                Button[Self](
                    label="Одобрить",
                    emoji="<:approve:1487439505727422674>",
                    style=ButtonStyle.secondary,
                    custom_id=f"forms:{type}:approve",
                    disabled=disable_buttons,
                ),
                Button[Self](
                    label="Отклонить",
                    emoji="<:remove:1487439841183535235>",
                    style=ButtonStyle.secondary,
                    custom_id=f"forms:{type}:reject",
                    disabled=disable_buttons,
                ),
            )
        )
        container.add_item(Separator())

        now = datetime.now(UTC)
        if user_answer_id and answer:
            container.add_item(
                TextDisplay(
                    f"### Решение от <@{user_answer_id}> ({discord_ts(now)}):\n```{answer}```"  # noqa: E501
                )
            )
        else:
            container.add_item(TextDisplay(f"-# Статус: {status}"))

        self.add_item(container)

    async def interaction_check(self, interaction: Interaction) -> bool:
        """Check if the user has permissions to interact with the buttons."""

        member = cast(Member, interaction.user)

        if not await check_member_permissions(member, self.type):
            await interaction.response.send_message(
                "У вас нет прав для взаимодействия с этими кнопками.",
                ephemeral=True,
            )
            return False

        return True
