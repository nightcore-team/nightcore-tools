"""Nightcore Glendale Tools Bot."""

import contextlib
import logging
import time
from datetime import UTC, datetime

import discord
from aiohttp import TCPConnector
from discord import app_commands
from discord.ext.commands import Bot  # type: ignore

from src.config._global import config
from src.nightcore.utils.on_ready_log import log_tree_summary

logger = logging.getLogger(__name__)


class GuildOnlyTree(app_commands.CommandTree):
    async def interaction_check(
        self, interaction: discord.Interaction
    ) -> bool:
        """Check if the interaction is from a specified guild."""
        if (
            interaction.guild is None
            or interaction.guild.id not in config.bot.ALLOWED_GUILDS
        ):
            with contextlib.suppress(discord.InteractionResponded):
                await interaction.response.send_message(
                    "Commands are only available in Arizona RolePlay Glendale.",  # noqa: E501
                    ephemeral=True,
                )
            return False

        return True


class NightcoreTools(Bot):
    def __init__(
        self,
        *,
        cog_modules: list[str],
    ):
        self.cog_modules = cog_modules

        super().__init__(
            command_prefix=".",
            intents=discord.Intents.all(),
            help_command=None,
            tree_cls=GuildOnlyTree,
        )
        self.startup_time: datetime = datetime.now(UTC)

    @property
    def _http_connector(self) -> TCPConnector:
        return TCPConnector(
            limit=100,  # max 100 connections
            ttl_dns_cache=300,  # Cache DNS for 5 minutes
            enable_cleanup_closed=True,
            force_close=False,  # Don't close connection after each request  # noqa: E501
            keepalive_timeout=60,  # Keep connection alive for 60 seconds
        )

    # def _validate_commands_permissions(
    #     self,
    #     commands: list[
    #         app_commands.Command[Any, ..., Any]
    #         | app_commands.Group
    #         | app_commands.ContextMenu
    #     ],
    # ) -> None:
    #     """Validate that all commands have __permissions_flag__ attribute.

    #     Args:
    #         commands: List of commands to validate

    #     Raises:
    #         CommandDontHavePermissionsFlagError: If command doesn't have permission flag  # noqa: E501
    #     """

    #     def _check_command(
    #         cmd: app_commands.Command[Any, ..., Any], path: str = ""
    #     ) -> None:
    #         """Recursively check command for permission flag."""

    #         if not hasattr(cmd.callback, "__permissions_flag__"):
    #             raise CommandDontHavePermissionsFlagError(
    #                 f"Command '{path}' is missing __permissions_flag__ attribute"  # noqa: E501
    #             )
    #         else:
    #             logger.info(
    #                 f"Command {path} has __permissions_flag__: {cmd.callback.__permissions_flag__}"  # noqa: E501 # type: ignore
    #             )

    #     def _check_group(group: app_commands.Group, path: str = "") -> None:
    #         """Recursively check group and its subcommands."""
    #         current_path = f"{path} {group.name}".strip()

    #         for sub_cmd in group.commands:
    #             if isinstance(sub_cmd, app_commands.Group):
    #                 _check_group(sub_cmd, current_path)
    #             else:
    #                 _check_command(sub_cmd, f"{current_path} {sub_cmd.name}")

    #     for cmd in commands:
    #         if isinstance(cmd, app_commands.Group):
    #             _check_group(cmd)
    #         elif isinstance(cmd, app_commands.Command):
    #             _check_command(cmd, cmd.name)
    #         else:
    #             logger.warning(
    #                 "Ignore app_commands.ContextMenu in permission validation: %s",  # noqa: E501
    #                 cmd.name,
    #             )

    #         logger.info(
    #             "Validating permissions flag for command: %s", cmd.name
    #         )

    async def load_extensions(self) -> None:
        """Load all bot extensions (cogs)."""
        logger.info("Starting to load extensions...")

        if self.cog_modules:
            for module in self.cog_modules:
                try:
                    logger.info(f"Loading cog: {module}")
                    await self.load_extension(module)
                    logger.info(f"[success] Successfully loaded {module}")
                except Exception as e:
                    logger.error(f"[failed] Failed to load {module}: {e}")
        else:
            logger.warning("No cogs to load")

    async def setup_hook(self):
        """Setup hook called when the bot is ready to start."""
        logger.info("Setup hook started...")

        await self.load_extensions()

        start = time.perf_counter()
        self.http.connector = self._http_connector
        await self.http.get_bot_gateway()
        end = time.perf_counter()
        logger.info(
            f"[gateway] Fetched bot gateway in {(end - start) * 1000:.2f}ms"
        )

        # commands = self.tree.get_commands()

        # self._validate_commands_permissions(commands)

        try:
            logger.info("Starting command sync...")
            synced = await self.tree.sync()
            logger.info(
                f"[success] Successfully synced {len(synced)} commands"
            )

        except Exception as e:
            logger.error(f"[failed] Sync failed: {e}")
            import traceback

            logger.error(traceback.format_exc())

        log_tree_summary(self.tree, logger=logger)

    async def on_ready(self):
        """Event called when the bot is ready."""
        logger.info(f"Loaded cogs: {list(self.cogs.keys())}")
        logger.info(f"Connected to {len(self.guilds)} guilds")
        logger.info("🚀 Nightcore Glendale Tools bot started successfully!")
