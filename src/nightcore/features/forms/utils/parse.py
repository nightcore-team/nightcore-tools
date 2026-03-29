"""Utils for parsing needed text from components."""

import re

from discord import Component


def parse_form_text_from_components(components: list[Component]):  # type: ignore
    """Extracts the form text from a list of components."""
    for component in components:
        # Recursively check for children/components if present
        children = (  # type: ignore
            getattr(component, "children", None)
            or getattr(component, "components", None)
            or []
        )
        if children:
            result = parse_form_text_from_components(children)  # type: ignore
            if result is not None:
                return result  # type: ignore
        # Try to extract from TextDisplay
        text = getattr(component, "text", None)
        if text:
            match = re.search(r"```([\s\S]*?)```", text)
            if match:
                return match.group(1).strip()
    return None


def parse_author_id_from_components(components: list[Component]):  # type: ignore
    """Extracts the author ID from a list of components."""
    for component in components:
        children = (  # type: ignore
            getattr(component, "children", None)
            or getattr(component, "components", None)
            or []
        )
        if children:
            result = parse_author_id_from_components(children)  # type: ignore
            if result is not None:
                return result  # type: ignore
        text = getattr(component, "text", None)
        if text:
            match = re.search(r"<@([0-9]+)>", text)
            if match:
                return int(match.group(1))
    return None
