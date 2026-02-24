import requests
from typing import Optional, Dict, Any
from datetime import datetime

class FlexopusClient:
    def __init__(self, base_host: str, api_token: str, timeout: int = 30):
        self.base_url = f"https://{base_host}/internal-api"
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/json, image/svg+xml, */*",
            "Origin": f"https://{base_host}",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:148.0) Gecko/20100101 Firefox/148.0"
        })
        self.session.cookies.set(
            "flexopus_session",
            api_token,
            domain=base_host
        )
        self.timeout = timeout

    def _sync_csrf_header(self):
        """If XSRF-TOKEN cookie exists, send it as header."""
        xsrf_token = self.session.cookies.get("XSRF-TOKEN")
        if xsrf_token:
            self.session.headers.update({
                "X-XSRF-TOKEN": xsrf_token
            })

    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        self._sync_csrf_header()
        
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        response = self.session.request(
            method=method,
            url=url,
            params=params,
            json=json,
            timeout=self.timeout,
        )

        response.raise_for_status()

        content_type = response.headers.get("Content-Type", "").lower()
        if "image/svg+xml" in content_type:
            body = response.text
        elif "application/json" in content_type:
            body = response.json()
        else:
            body = response.content

        return body

    
    def getLocations(self):
        return self._request("GET", "v2/locations")
    
    def getLocationsBookableStats(self):
        return self._request("GET", f"v2/locations/bookable-stats")
    
    def getLocationBookables(self, id: int):
        return self._request("GET", "v2/location/{id}/bookables")
    
    def getLocationMap(self, id: int):
        return self._request("GET", f"locations/{id}/map")
    
    def getBuildings(self):
        return self._request("GET", "buildings")
    
    def getBuilding(self, id: int):
        return self._request("GET", f"buildings/{id}")
    
    def getEquipment(self):
        return self._request("GET", "search/data/equipments")
    
    def getBookableTypeImages(self):
        return self._request("GET", "bookable-type-images")
    
    # TODO: 422: Typ muss ausgefüllt werden
    def getFavourites(self):
        return self._request("GET", "favourites")
    
    def getSelfUser(self):
        return self._request("GET", "auth/user")
    
    """ 
    Possible parameters
        page=1,2,3,...
        bookable_type=DESK,MEETING_ROOM,PARKING_SPACE
        guest_bookings=false,true
        date_from=2025-02-01T00:00:00.000%2B01:00
        date_to=2026-12-31T23:59:59.999%2B01:00
        bookable_type=HOME_OFFICE,DESK
    """
    def getUser(self, id: int):
        return self._request("GET", f"users/{id}")
    
    def getUserBookings(self, id: int, params: Optional[Dict[str, any]] = None):
        return self._request("GET", f"bookings/user/{id}", params=params)
    
    """
    Required parameters
        name=max
        isActive=false,true
        isFavoured=false,true
    """
    def searchUsers(self, params: Optional[Dict[str, any]] = None):
        return self._request("GET", "search/users", params=params)
    
    """
    Required parameters
        type=DESK
        name=abc
        isActive=false
        isFavoured=false
    """
    def searchObjects(self, params: Optional[Dict[str, any]] = None):
        return self._request("GET", "search/objects", params=params)
    
    def getBooking(self, id: int):
        return self._request("GET", f"bookings/{id}")
    
    def deleteBooking(self, id: int):
        return self._request("DELETE", f"bookings/{id}")

    def updateBooking(self, id: int, from_time: datetime, to_time: datetime):
        payload = {
            "fromTime": from_time.isoformat(),
            "toTime": to_time.isoformat()
        }
        return self._request("PATCH", f"bookings/{id}", json=payload)
    
    def getSettings(self):
        return self._request("GET", "settings")

    def getBookable(self, id: int):
        return self._request("GET", f"bookables/{id}")

    def getCompanySettings(self):
        return self._request("GET", "company-settings")
    