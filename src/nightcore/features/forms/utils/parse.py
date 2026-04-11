"""Utils for parsing needed text from components."""

import logging
import re
from typing import cast

from discord import Component

logger = logging.getLogger(__name__)


def parse_form_text_from_components(
    components: list[Component],
) -> str | None:  # type: ignore
    """Extracts the form text from a list of components."""
    for container in components:
        for item in container.children:  # type: ignore
            if item.id == 5:  # type: ignore
                content = cast(str | None, item.content)  # type: ignore
                if content:
                    return content

    return None


def parse_author_id_from_components(components: list[Component]):  # type: ignore
    """Extracts the author ID from a list of components."""
    for component in components:
        for item in component.children:  # type: ignore
            if item.id == 3:  # type: ignore
                match = re.search(r"<@!?(\d+)>", item.content)  # type: ignore
                if match:
                    return int(match.group(1))

    return None
