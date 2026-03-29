"""Form modal."""

from typing import Self

from discord import TextStyle
from discord.ui import Modal, TextInput


class RejectFormModal(Modal, title="Отклонение анкеты"):
    def __init__(self, type: str) -> None:
        super().__init__(custom_id=f"forms_modal:{type}:reject")

        """Build the form modal layout."""

    reason = TextInput[Self](
        label="Причина отклонения",
        style=TextStyle.paragraph,
        placeholder="Введите причину отклонения анкеты.",
        required=True,
        max_length=100,
    )
