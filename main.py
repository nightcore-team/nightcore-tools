"""Main entry point for the Nightcore bot."""

from src.config._global import config
from src.nightcore.setup import create_bot
from src.utils.logging.setup import setup_logging


def main() -> None:
    """Main function to start the Nightcore bot."""
    logger, discord_logger = setup_logging()
    bot = create_bot()

    logger.info("Starting Nightcore bot...")
    try:
        bot.run(config.bot.BOT_TOKEN, log_handler=discord_logger.handlers[0])
    except Exception as e:
        logger.error("Error occurred: %s", e)
    finally:
        logger.info("Nightcore bot has been stopped.")


if __name__ == "__main__":
    main()
