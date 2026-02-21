"""Defines the Config class for bot environment settings."""

from src.config.env import BaseEnvConfig


class Config(BaseEnvConfig):
    BOT_TOKEN: str
    EMBED_DESCRIPTION_LIMIT: int = 4096
    VIEW_V2_DESCRIPTION_LIMIT: int = 3000
    VIEW_V2_COMPONENTS_LIMIT: int = 40
    DELETE_MESSAGES_SECONDS: int = 604800
    MAX_GUILD_ROLES_COUNT: int = 250
    DEVELOPER_IDS: list[int] = [  # noqa: RUF012
        1280700292530176131,
        566255833684508672,
        451359852418039808,
    ]
    ALLOWED_GUILDS: list[int] = [  # noqa: RUF012
        693824534163488838,
    ]
