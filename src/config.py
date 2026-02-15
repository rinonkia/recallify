"""Configuration management."""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Application configuration."""

    # Database
    DATABASE_PATH = os.getenv("DATABASE_PATH", "./data/recallify.db")

    # GitHub
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
    GITHUB_REPOS = os.getenv("GITHUB_REPOS", "").split(",")

    # Slack
    SLACK_TOKEN = os.getenv("SLACK_TOKEN", "")
    SLACK_CHANNELS = os.getenv("SLACK_CHANNELS", "").split(",")

    # AWS Bedrock
    AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")
    BEDROCK_MODEL_ID = os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-5-sonnet-20241022-v2:0")


config = Config()
