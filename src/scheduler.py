"""Task scheduler using APScheduler."""

import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from src.tasks.fetch_github import fetch_github_data
from src.tasks.fetch_slack import fetch_slack_data
from src.tasks.summarize_github import summarize_github_data
from src.tasks.summarize_slack import summarize_slack_data

logger = logging.getLogger(__name__)


def run_daily_tasks():
    """Run all daily tasks in sequence."""
    logger.info("Starting daily tasks...")

    try:
        logger.info("Task 1: Fetching GitHub data")
        fetch_github_data()
    except Exception as e:
        logger.error(f"Error in fetch_github_data: {e}")

    try:
        logger.info("Task 2: Fetching Slack data")
        fetch_slack_data()
    except Exception as e:
        logger.error(f"Error in fetch_slack_data: {e}")

    try:
        logger.info("Task 3: Summarizing GitHub data")
        summarize_github_data()
    except Exception as e:
        logger.error(f"Error in summarize_github_data: {e}")

    try:
        logger.info("Task 4: Summarizing Slack data")
        summarize_slack_data()
    except Exception as e:
        logger.error(f"Error in summarize_slack_data: {e}")

    logger.info("Daily tasks completed")


def setup_scheduler() -> BackgroundScheduler:
    """Set up and configure the task scheduler.

    Returns:
        BackgroundScheduler: Configured scheduler instance
    """
    scheduler = BackgroundScheduler()

    # Schedule daily tasks at 2:00 AM
    scheduler.add_job(
        run_daily_tasks,
        trigger=CronTrigger(hour=2, minute=0),
        id="daily_tasks",
        name="Daily data collection and summarization",
        replace_existing=True,
    )

    logger.info("Scheduler configured: Daily tasks will run at 2:00 AM")
    return scheduler
