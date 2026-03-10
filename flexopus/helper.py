from flexopus.client import FlexopusClient
from datetime import datetime

# Returns the first parking location for the given building id, or None if there is no parking location associated with the building
def getParkingLocation(client: FlexopusClient, building_id: int):
    locations = client.getLocations()["data"]
    bookable_stats = client.getLocationsBookableStats()["data"]
    for location in locations:
        if location["building_id"] != building_id:
            continue
        for stat in bookable_stats:
            if not stat["free_bookables"]["PARKING_SPACE"] > 0:
                continue
            if stat["id"] == location["id"]:
                return location
    return None

def getRandomParkingSpace(client: FlexopusClient, building_id: int, from_time: datetime, to_time: datetime):
    parking_location = getParkingLocation(client, building_id)
    parking_spaces = client.getLocationBookables(parking_location["id"], from_time, to_time)["data"]
    for space in parking_spaces:
        if space["type"] != "PARKING_SPACE":
            continue
        if space["status"] == "FREE" and len(space["actual_bookings"]) == 0:
            return space
    return None