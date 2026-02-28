from flexopus import FlexopusClient
import os
from datetime import datetime, timezone, timedelta
from argparse import ArgumentParser
from collections import defaultdict

if __name__ == "__main__":
    client = FlexopusClient(os.environ["FLEXOPUS_HOST"], os.environ["FLEXOPUS_TOKEN"])
    argparser = ArgumentParser()
    argparser.add_argument("--locations", action="store_true")
    argparser.add_argument("--bookables", type=int, help="Location ID to list bookables for")
    argparser.add_argument("--buildings", action="store_true")
    argparser.add_argument("--equipment", action="store_true")
    argparser.add_argument("--self-user", action="store_true")
    argparser.add_argument("--settings", action="store_true")
    argparser.add_argument("--company-settings", action="store_true")
    argparser.parse_args()

    tz = timezone(timedelta(hours=1))  # adjust if needed

    now = datetime.now(tz)
    start_of_week = now - timedelta(days=now.weekday())
    start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)

    end_of_week = start_of_week + timedelta(days=6)
    end_of_week = end_of_week.replace(hour=23, minute=59, second=59, microsecond=999999)

    if argparser.parse_args().locations:
        locations = client.getLocations()["data"]

        grouped = defaultdict(list)

        for location in locations:
            building = location.get("building") or {}
            building_name = building.get("name", "Unknown Building")
            grouped[building_name].append(location)

        for building_name, items in grouped.items():
            print(f"=== {building_name} ===")
            for location in items:
                print(f"{location['id']}: {location['name']}")
            print()

    if argparser.parse_args().bookables:
        bookables = client.getLocationBookables(argparser.parse_args().bookables, 
                                                datetime.now(tz),
                                                datetime.now(tz) + timedelta(days=1))["data"]
        for bookable in bookables:
            actual_bookings = bookable.get("actual_bookings", [])
            print(f"{bookable['id']}: {bookable['name']} ({bookable['type']}) ({bookable['status']}), {len(actual_bookings)} bookings)")

    if argparser.parse_args().buildings:
        buildings = client.getBuildings()["data"]
        for building in buildings:
            print(f"{building['id']}: {building['name']}, {building['street']} {building['street_number']}, {building['zip']} {building['city']}")

    if argparser.parse_args().equipment:
        equipment = client.getEquipment()["data"]
        for eq in equipment:
            print(f"{eq['id']}: {eq['name']}")
    
    if argparser.parse_args().self_user:
        self_user = client.getSelfUser()["data"]
        print(f"{self_user['id']}: {self_user['name']} ({self_user['email']}) - {self_user['department']}")
        vehicles = self_user.get("vehicles", [])
        for vehicle in vehicles:
            print(f"  {vehicle['id']}: {vehicle['name']} {vehicle['license_plate']}")

    if argparser.parse_args().settings:
        settings = client.getSettings()["data"]
        for key, value in settings.items():
            if isinstance(value, dict):
                print(f"{key}:")
                for sub_key, sub_value in value.items():
                    print(f"  {sub_key}: {sub_value}")
            else:
                print(f"{key}: {value}")

    if argparser.parse_args().company_settings:
        company_settings = client.getCompanySettings()["data"]
        for key, value in company_settings.items():
            print(f"{key}: {value}")