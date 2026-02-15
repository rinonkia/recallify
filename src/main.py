"""Main application entry point for scheduler daemon."""

import logging
import signal
import sys
import time

from src.config import config
from src.database.connection import Database
from src.scheduler import setup_scheduler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def signal_handler(signum, frame):
    """Handle shutdown signals gracefully."""
    logger.info(f"Received signal {signum}, shutting down...")
    sys.exit(0)


def main():
    """Start the scheduler daemon."""
    logger.info("Starting Recallify scheduler daemon...")

    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Initialize database
    logger.info(f"Initializing database at {config.DATABASE_PATH}")
    db = Database(config.DATABASE_PATH)
    db.init_db()
    logger.info("Database initialized")

    # Set up and start scheduler
    scheduler = setup_scheduler()
    scheduler.start()
    logger.info("Scheduler started successfully")

    # Keep the application running
    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        logger.info("Shutting down scheduler...")
        scheduler.shutdown()
        logger.info("Scheduler shut down successfully")


if __name__ == "__main__":
    main()