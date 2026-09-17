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

def getFreeParkingSpace(client: FlexopusClient, building_id: int, from_time: datetime, to_time: datetime):
    return getPreferedFreeParkingSpace(client, building_id, from_time, to_time, [])

def getPreferedFreeParkingSpace(client: FlexopusClient, building_id: int, from_time: datetime, to_time: datetime, prefered_parking_spaces: list[str]):
    locations = client.getLocations()["data"]
    building_locations = [loc for loc in locations if loc["building_id"] == building_id]
    
    free_spaces = []
    for loc in building_locations:
        try:
            parking_spaces = client.getLocationBookables(loc["id"], from_time, to_time)["data"]
            loc_free_spaces = [space for space in parking_spaces if space["type"] == "PARKING_SPACE" and space["status"] == "FREE" and len(space["actual_bookings"]) == 0]
            free_spaces.extend(loc_free_spaces)
        except Exception:
            pass
            
    if not free_spaces:
        return None
        
    if len(prefered_parking_spaces) > 0:
        for pref_name in prefered_parking_spaces:
            clean_pref = pref_name.strip().lower()
            for space in free_spaces:
                if space["name"].strip().lower() == clean_pref:
                    return space
                    
    return free_spaces[0]