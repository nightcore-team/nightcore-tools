"""Organizations utils."""

from typing import TYPE_CHECKING

from src.nightcore.features.forms.constants import ORGANIZATIONS_DICTIONARY

if TYPE_CHECKING:
    from src.nightcore.features.forms.types import OrganizationInfo


def get_organizations_dicts(type: str) -> list["OrganizationInfo"]:
    """Get the organization name by type."""

    return ORGANIZATIONS_DICTIONARY.get(type, [])
