"""Script to log time entries for MSE Practicum 2025 on Clockify."""

import logging
from datetime import datetime, timedelta

import click
import requests

# MSE Practicum 2025
WORKSPACE_ID = "68a7cf46e201a71118ccc40f"

# Koppers Project
PROJECT_ID = "68a7d0031fc540325e9abcd6"

CLOCKIFY_API_URL = "https://api.clockify.me/api/v1"


# Each entry: day (0=Mon), start, end, description
WEEKLY_SCHEDULE = [
    # Monday
    {"day": 0, "start": (11, 0), "end": (15, 0), "description": "core hours"},
    # Tuesday
    {"day": 1, "start": (12, 0), "end": (16, 0), "description": "core hours"},
    # Wednesday
    {"day": 2, "start": (10, 0), "end": (14, 0), "description": "core hours"},
    {"day": 2, "start": (14, 0), "end": (16, 0), "description": "client meeting"},
    {"day": 2, "start": (18, 0), "end": (20, 0), "description": "mentor meeting"},
    # Thursday
    {"day": 3, "start": (12, 0), "end": (16, 0), "description": "core hours"},
    # Friday
    {"day": 4, "start": (9, 0), "end": (13, 0), "description": "core hours"},
]

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_week_start():
    """Get the start of the current week (Monday)."""
    today = datetime.today()
    return today - timedelta(days=today.weekday())  # Monday


def create_time_entry(entry, week_start, clockify_api_key, commit):
    """Create a time entry on Clockify.

    Args:
        entry (dict): Dictionary with keys 'day', 'start', 'end', 'description'.
        week_start (datetime): The start of the week (Monday).
        clockify_api_key (str): Clockify API key.
        commit (bool): If True, actually create the entry; if False, just print.
    """
    entry_date = week_start + timedelta(days=entry["day"])
    start_time = entry_date.replace(
        hour=entry["start"][0], minute=entry["start"][1], second=0, microsecond=0
    )
    end_time = entry_date.replace(
        hour=entry["end"][0], minute=entry["end"][1], second=0, microsecond=0
    )
    data = {
        "start": start_time.isoformat() + "Z",
        "end": end_time.isoformat() + "Z",
        "description": entry["description"],
        "projectId": PROJECT_ID,
        "workspaceId": WORKSPACE_ID,
    }
    url = f"{CLOCKIFY_API_URL}/workspaces/{WORKSPACE_ID}/time-entries"
    header = {"X-Api-Key": clockify_api_key, "Content-Type": "application/json"}

    logger.info(f"Preparing to log: {start_time} - {end_time} ({entry['description']})")
    if not commit:
        return
    response = requests.post(url, headers=header, json=data)
    if response.status_code == 201:
        logger.info(
            f"Logged: {start_time.strftime('%A %Y-%m-%d %H:%M')} - {end_time.strftime('%H:%M')} ({entry['description']})"
        )
    else:
        logger.error(f"Failed for {start_time.date()}: {response.text}")


@click.command()
@click.option(
    "--clockify-api-key",
    "clockify_api_key",
    envvar="CLOCKIFY_API_KEY",
    type=str,
    required=True,
    help="Clockify API key",
)
@click.option("--commit", is_flag=True, help="Actually create the time entries")
def cli(clockify_api_key, commit):
    """CLI to log time entries for MSE Practicum 2025 on Clockify.

    Args:
        clockify_api_key (str): Clockify API key.
        commit (bool): If set, actually create the time entries.
    """
    week_start = get_week_start()
    for entry in WEEKLY_SCHEDULE:
        create_time_entry(entry, week_start, clockify_api_key, commit)


if __name__ == "__main__":
    cli()
