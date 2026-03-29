"""Utils for parsing needed text from components."""

import logging
import re

from discord import Component

logger = logging.getLogger(__name__)


def parse_form_text_from_components(components: list[Component]):  # type: ignore
    """Extracts the form text from a list of components."""
    for container in components:
        logger.info("Childrens of container: %s", container.children)  # type: ignore
        for item in container.children:  # type: ignore
            logger.info("Item: %s", item)  # type: ignore
            if item.id == 5:  # type: ignore
                match = re.search(r"```([\s\S]*?)```", item.content)  # type: ignore
                if match:
                    return match.group(1)

    return None


def parse_author_id_from_components(components: list[Component]):  # type: ignore
    """Extracts the author ID from a list of components."""
    for component in components:
        logger.info("Children of component: %s", component.children)  # type: ignore
        for item in component.children:  # type: ignore
            logger.info("Item: %s", item)  # type: ignore
            if item.id == 3:  # type: ignore
                match = re.search(r"<@!?(\d+)>", item.content)  # type: ignore
                if match:
                    return int(match.group(1))

    return None
