"""Form modal."""

from typing import Self

from discord import TextStyle
from discord.ui import Modal, TextInput


class FormModal(Modal, title="Заполнение анкеты"):
    def __init__(self, type: str) -> None:
        super().__init__(custom_id=f"forms_modal:{type}:sent")

        """Build the form modal layout."""

    form = TextInput[Self](
        label="Анкета для заполнения",
        style=TextStyle.paragraph,
        placeholder="Скопируйте и вставьте заполненную анкету сюда.",
        required=True,
        max_length=1000,
    )
