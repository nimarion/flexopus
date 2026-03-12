import requests
import pickle
import os
from typing import Optional, Dict, Any
from datetime import datetime, timezone
from urllib.parse import unquote
from http.cookiejar import CookieJar
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def transformNowDatetime(dtime: datetime) -> datetime:
    now = datetime.now(timezone.utc)

    if dtime.tzinfo is None:
        dtime = dtime.replace(tzinfo=timezone.utc)

    return max(dtime, now)

def loadCookies(session: requests.Session, cookie_file: str):
    if not os.path.exists(cookie_file):
        with open(cookie_file, "wb") as f:
            logger.debug("Cookie file not found. Creating new cookie file at %s", cookie_file)
            pickle.dump(requests.cookies.RequestsCookieJar(), f)

    with open(cookie_file, "rb") as f:
        logger.debug("Loading cookies from file %s", cookie_file)
        cookies = pickle.load(f)

    if isinstance(cookies, CookieJar):
        session.cookies = cookies
        logger.debug("Cookies loaded successfully from %s", cookie_file)
    else:
        logger.warning("Loaded cookies are not of type CookieJar. Initializing empty cookie jar.")
        session.cookies = requests.cookies.RequestsCookieJar()

def saveCookies(session: requests.Session, cookie_file: str):
    with open(cookie_file, "wb") as f:
        pickle.dump(session.cookies, f)
        logger.debug("Cookies saved to file %s", cookie_file)

class FlexopusClient:

    _base_url: str
    _timeout: int
    session: requests.Session
    _cookie_file: Optional[str]

    def __init__(self, 
                 base_host: str, 
                 api_token: str,
                 timeout: int = 30, 
                 cookie_file: Optional[str] = None):
        self._base_url = f"https://{base_host}/internal-api"
        self._timeout = timeout
        self.session = requests.Session()
        self._cookie_file = cookie_file
        self.session.headers.update({
            "Accept": "application/json, image/svg+xml, */*",
            "Origin": f"https://{base_host}",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:148.0) Gecko/20100101 Firefox/148.0"
        })
        if cookie_file:
            loadCookies(self.session, cookie_file)
            
        if self.session.cookies.get("flexopus_session") is None and api_token is not None:
            self.session.cookies.set(
                "flexopus_session",
                api_token,
                domain=base_host
            )
        self.timeout = timeout
        logger.debug("Client initialized for host=%s", base_host)

    def _sync_csrf_header(self):
        """If XSRF-TOKEN cookie exists, send it as header."""
        xsrf_token = self.session.cookies.get("XSRF-TOKEN")
        if xsrf_token:
            self.session.headers.update({
                "X-XSRF-TOKEN": unquote(xsrf_token)
            })

    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        self._sync_csrf_header()
        
        url = f"{self._base_url}/{endpoint.lstrip('/')}"

        response = self.session.request(
            method=method,
            url=url,
            params=params,
            json=json,
            timeout=self.timeout,
        )

        response.raise_for_status()

        if self._cookie_file:
            saveCookies(self.session, self._cookie_file)

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
    
    def getLocationBookables(self, id: int, from_time: datetime, to_time: datetime):
        params = {
            "from": from_time.isoformat(),
            "to": to_time.isoformat(),
            "include_past": "true"
        }
        return self._request("GET", f"v2/location/{id}/bookables", params=params)
    
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
    
    # TODO: HTTP 422: Typ muss ausgefüllt werden
    def getFavourites(self):
        raise NotImplementedError()
        return self._request("GET", "favourites")
    
    def addFavourite(self):
        raise NotImplementedError()
    
    def deleteFavourite(self):
        raise NotImplementedError()
    
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
    
    def getBookingConflicts(self, from_time: datetime, to_time: datetime, bookable_type: str):
        params = {
            "from": from_time.isoformat(),
            "to": to_time.isoformat(),
            "bookable_type": bookable_type
        }
        return self._request("GET", "bookings/conflicts", params=params)
    
    def deleteBooking(self, id: int):
        return self._request("DELETE", f"bookings/{id}")

    def updateBooking(self, id: int, from_time: datetime, to_time: datetime):
        payload = {
            "fromTime": transformNowDatetime(from_time).isoformat(),
            "toTime": to_time.isoformat()
        }
        return self._request("PATCH", f"bookings/{id}", json=payload)
    
    def createBooking(self, location_id: int, bookable_id: int,  from_time: datetime, to_time: datetime, user_vehicle_id: Optional[int] = None):
        payload = {
            "from_time": transformNowDatetime(from_time).isoformat(),
            "to_time": to_time.isoformat(),
            "skip_weekends": False,
            "user_vehicle_id": user_vehicle_id
        }
        return self._request("POST", f"location/{location_id}/bookables/{bookable_id}/book", json=payload)

    def createGuestBooking(self, location_id: int, bookable_id: int,  from_time: datetime, to_time: datetime, guest_email: str, guest_name: str, booking_info: Optional[str] = ""):
        payload = {
            "from_time": transformNowDatetime(from_time).isoformat(),
            "to_time": to_time.isoformat(),
            "skip_weekends": False,
            "guest_email": guest_email,
            "guest_name": guest_name,
            "booking_info": booking_info 
        }
        return self._request("POST", f"location/{location_id}/bookables/{bookable_id}/guest-booking", json=payload)
    
    def getSettings(self):
        return self._request("GET", "settings")

    def getBookable(self, id: int):
        return self._request("GET", f"bookables/{id}")
    
    def getBookableConflicts(self, bookable_id: int, from_time: datetime, to_time: datetime):
        params = {
            "from": from_time.isoformat(),
            "to": to_time.isoformat(),
        }
        return self._request("GET", f"bookables/{bookable_id}/conflicts", params=params)

    def getCompanySettings(self):
        return self._request("GET", "company-settings")
    
    def authCheck(self):
        return self._request("GET", "auth/check")
    
    def getLatestSessionToken(self):
        return self.session.cookies.get("flexopus_session")

    def getXsrfToken(self):
        return self.session.cookies.get("XSRF-TOKEN")