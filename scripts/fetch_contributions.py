from pathlib import Path
import json
import re
import requests
from bs4 import BeautifulSoup


USERNAME = "kunalvish08"

OUTPUT = Path("data/contributions.json")

URL = f"https://github.com/users/{USERNAME}/contributions"


def main():

    print()
    print("========================================")
    print("Fetching GitHub contribution data")
    print("========================================")
    print()

    headers = {
        "User-Agent": (
            "Mozilla/5.0 "
            "(Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/151.0 Safari/537.36"
        )
    }

    response = requests.get(
        URL,
        headers=headers,
        timeout=30
    )

    response.raise_for_status()

    print(
        f"GitHub response: {response.status_code}"
    )

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    days = []

    # GitHub contribution cells
    cells = soup.select(
        "td.ContributionCalendar-day"
    )

    if not cells:
        # Fallback selector
        cells = soup.select(
            "[data-date][data-level]"
        )

    print(
        f"Contribution cells found: {len(cells)}"
    )

    for cell in cells:

        date = cell.get(
            "data-date"
        )

        level = cell.get(
            "data-level"
        )

        if date is None:
            continue

        if level is None:
            level = "0"

        try:
            level = int(level)
        except ValueError:
            level = 0

        days.append({
            "date": date,
            "level": level
        })

    if not days:
        raise RuntimeError(
            "Could not find GitHub contribution data."
        )

    # Sort chronologically
    days.sort(
        key=lambda x: x["date"]
    )

    # --------------------------------------------------
    # Statistics
    # --------------------------------------------------

    total = sum(
        day["level"]
        for day in days
    )

    active_days = [
        day
        for day in days
        if day["level"] > 0
    ]

    # Current streak
    current_streak = 0

    for day in reversed(days):

        if day["level"] > 0:
            current_streak += 1
        else:
            break

    # Longest streak
    longest_streak = 0
    running = 0

    for day in days:

        if day["level"] > 0:
            running += 1
            longest_streak = max(
                longest_streak,
                running
            )
        else:
            running = 0

    best_day = None

    if active_days:
        best_day = max(
            active_days,
            key=lambda x: x["level"]
        )

    result = {
        "username": USERNAME,
        "source": URL,
        "days": days,
        "stats": {
            "total_activity": total,
            "active_days": len(active_days),
            "current_streak": current_streak,
            "longest_streak": longest_streak,
            "best_day": best_day
        }
    }

    OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    OUTPUT.write_text(
        json.dumps(
            result,
            indent=2
        ),
        encoding="utf-8"
    )

    print()
    print("========================================")
    print("SUCCESS")
    print("========================================")
    print(
        f"Saved: {OUTPUT.absolute()}"
    )
    print(
        f"Days: {len(days)}"
    )
    print(
        f"Active days: {len(active_days)}"
    )
    print(
        f"Current streak: {current_streak}"
    )
    print(
        f"Longest streak: {longest_streak}"
    )
    print()


if __name__ == "__main__":
    main()