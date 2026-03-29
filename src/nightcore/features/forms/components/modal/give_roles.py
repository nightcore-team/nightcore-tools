"""Give Roles Form modal."""

from typing import Self

from discord import SelectOption, TextStyle
from discord.ui import Modal, Select, TextInput

from src.nightcore.features.forms.utils.organizations import (
    get_organizations_dicts,
)


class GiveRolesFormModal(Modal, title="Выдача ролей"):
    def __init__(self, type: str) -> None:
        super().__init__(custom_id=f"forms_modal:{type}:give_roles")

        """Build the form modal layout."""

        orgs = get_organizations_dicts(type)

        self.add_item(
            TextInput[Self](
                label="ID пользователя",
                style=TextStyle.short,
                placeholder="123456789012345678",
                required=True,
                max_length=20,
            )
        )

        self.add_item(
            Select[Self](
                placeholder="Выберите организацию",
                required=True,
                options=[
                    SelectOption(label=key, value=value) for key, value in orgs
                ],
            )
        )
