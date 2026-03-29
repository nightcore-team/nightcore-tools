"""Forms-related types."""

from typing import TypedDict


class OrganizationInfo(TypedDict):
    """Organization info."""

    name: str
    deputy_role_id: str
