
"""Manage warehouse assets and their maintenance schedules."""

import json
import tempfile
from datetime import datetime, timedelta
from pathlib import Path


# Global asset registry and default maintenance interval.
assets = {}
SERVICE_INTERVAL_DAYS = 90


def register_asset(asset_id, machine_type, logs=None):
    """Register an asset and record its ID in the current run's logs."""
    if not asset_id or not asset_id.strip():
        print("Could not register asset: asset ID cannot be empty.")
        return

    if logs is None:
        logs = []

    assets[asset_id] = {
        "type": machine_type,
        "last_service": datetime.now().strftime("%Y-%m-%d"),
    }
    logs.append(asset_id)
    print(
        "Registered", asset_id,
        "- total registrations this run:", len(logs)
    )


def update_service_date(asset_id, date):
    """Update an asset's service date after validating the input."""
    try:
        parsed_date = datetime.strptime(date, "%Y-%m-%d")
    except (ValueError, TypeError):
        print("Could not update", asset_id, "- invalid date")
        return

    if asset_id not in assets:
        print("Could not update", asset_id, "- asset not found")
        return

    assets[asset_id]["last_service"] = parsed_date.strftime("%Y-%m-%d")


def due_for_inspection(interval_days=SERVICE_INTERVAL_DAYS):
    """Return asset IDs whose last service exceeds the given interval."""
    due = []
    today = datetime.now()

    for asset_id, asset in assets.items():
        last_service = datetime.strptime(
            asset["last_service"], "%Y-%m-%d"
        )
        if today - last_service > timedelta(days=interval_days):
            due.append(asset_id)

    return due


def change_interval(days):
    """Validate and return a positive maintenance interval."""
    if not isinstance(days, int) or isinstance(days, bool) or days <= 0:
        raise ValueError("Service interval must be a positive integer.")
    return days


def export_service_report(file="maintenance.json"):
    """Write the asset registry to a UTF-8 JSON report."""
    with open(file, "w", encoding="utf-8") as report_file:
        json.dump(assets, report_file, indent=2)
    print("Report written to " + file)


def write_scratch_copy():
    """Create a securely named temporary JSON copy of the asset registry."""
    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        suffix=".json",
        delete=False,
    ) as scratch_file:
        json.dump(assets, scratch_file)
        path = Path(scratch_file.name)

    print("Scratch copy at", path)


def print_alerts(interval_days=SERVICE_INTERVAL_DAYS):
    """Print alerts for assets that are overdue for inspection."""
    for asset_id in due_for_inspection(interval_days):
        print(
            "ALERT: inspection overdue for",
            asset_id,
            assets[asset_id]["type"],
        )


def main():
    """Register sample assets and generate the maintenance report."""
    register_asset("FL-01", "Forklift")
    register_asset("CV-07", "Conveyor")
    register_asset("", "Pallet Jack")
    register_asset("FL-01", "Crane")

    update_service_date("FL-01", "2025-01-15")
    update_service_date("XX-99", "2025-02-01")

    try:
        interval_days = change_interval(90)
    except ValueError as error:
        print("Invalid service interval:", error)
        return

    date_input = input(
        "Last service date for CV-07 (YYYY-MM-DD, Enter to skip): "
    )
    if date_input:
        update_service_date("CV-07", date_input)

    if not assets:
        print("No assets registered.")
        return

    print_alerts(interval_days)
    export_service_report()
    write_scratch_copy()


if __name__ == "__main__":
    main()
