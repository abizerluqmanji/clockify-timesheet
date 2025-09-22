"""Script to log time entries for MSE Practicum 2025 on Clockify."""

from datetime import datetime, timedelta

import click
import requests

# MSE Practicum 2025
WORKSPACE_ID = "68a7cf46e201a71118ccc40f"

# Koppers Project
PROJECT_ID = "68a7d0031fc540325e9abcd6"

CLOCKIFY_API_URL = "https://api.clockify.me/api/v1"


def get_week_dates():
    today = datetime.today()
    start = today - timedelta(days=today.weekday())  # Monday
    return [start + timedelta(days=i) for i in range(5)]  # Mon-Fri


def create_time_entry(date, clockify_api_key):
    start_time = date.replace(hour=9, minute=0, second=0, microsecond=0)
    end_time = date.replace(hour=12, minute=0, second=0, microsecond=0)
    data = {
        "start": start_time.isoformat() + "Z",
        "end": end_time.isoformat() + "Z",
        "description": "Core hours",
        "projectId": PROJECT_ID,
        # "type": "REGULAR",
        "workspaceId": WORKSPACE_ID,
    }
    url = f"{CLOCKIFY_API_URL}/workspaces/{WORKSPACE_ID}/time-entries"
    header = {"X-Api-Key": clockify_api_key, "Content-Type": "application/json"}
    response = requests.post(url, headers=header, json=data)
    if response.status_code == 201:
        print(f"Logged: {start_time.date()} 9am-12pm")
    else:
        print(f"Failed for {start_time.date()}: {response.text}")


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
    if commit:
        week_dates = get_week_dates()
        for date in week_dates:
            create_time_entry(date, clockify_api_key)


if __name__ == "__main__":
    cli()
