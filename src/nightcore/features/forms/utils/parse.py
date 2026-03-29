"""Utils for parsing needed text from components."""

import re

from discord import Component


def parse_form_text_from_components(components: list[Component]):  # type: ignore
    """Extracts the form text from a list of components."""
    for container in components:
        for item in container.children:  # type: ignore
            if item.id == 4:  # type: ignore
                match = re.search(r"```([\s\S]*?)```", item.content)  # type: ignore
                if match:
                    return match.group(1)

    return None


def parse_author_id_from_components(components: list[Component]):  # type: ignore
    """Extracts the author ID from a list of components."""
    for component in components:
        for item in component.children:  # type: ignore
            if item.id == 2:  # type: ignore
                match = re.search(r"<@!?(\d+)>", item.content)  # type: ignore
                if match:
                    return int(match.group(1))

    return None
