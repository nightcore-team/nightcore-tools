"""Setup module for creating and configuring the Nightcore bot instance."""

from src.nightcore.bot import NightcoreTools


def create_bot() -> NightcoreTools:
    """Create and return an instance of the Nightcore bot."""

    cog_modules: list[str] = [
        # commands
        "src.nightcore.features.meta.commands.about",
        "src.nightcore.features.meta.commands.ping",
        "src.nightcore.features.ga.commands.ga",
        "src.nightcore.features.forms.commands.formsmessage",
        # events
        "src.nightcore.events.interaction",
        "src.nightcore.events.error",
    ]

    return NightcoreTools(
        cog_modules=cog_modules,
    )
