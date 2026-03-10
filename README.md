# flexopus

An python client for the flexopus api which uses the internal api of the flexopus web application to interact with the flexopus backend. The client is designed to be used in a python application and provides a simple interface to interact with the flexopus api.

## Terminology

- **Building**: A building is a physical structure that can contain multiple rooms. It is identified by a unique id and has a list of locations associated with it.
- **Location**: A location is a specific area within a building, such as a floor or a parking lot. It is identified by a unique id and has a list of bookables associated with it.
- **Bookable**: A bookable is a resource that can be reserved, such as a desk, meeting room or parking space. It is identified by a unique id and has a list of **bookings** associated with it.
  - Status of a bookable: Does not represent if a bookable is currently reserved or not, but rather if it is available for reservation. A bookable can be unavailable for reservation if it is under maintenance or if it is restricted to certain users or groups.
- **Booking**: A booking is a reservation of a bookable for a specific time period. It is identified by a unique id and has a start time, end time and a reference to the bookable that is being reserved.

## Usage

- [Examples](examples/)

```bash
# requirements.txt
flexopus @ git+https://github.com/nimarion/flexopus
```

```bash
pip install -r requirements.txt
```

```python
import os
from flexopus import FlexopusClient

client = FlexopusClient(os.environ["FLEXOPUS_HOST"], os.environ["FLEXOPUS_TOKEN"])
client = FlexopusClient(os.environ["FLEXOPUS_HOST"], os.environ["FLEXOPUS_TOKEN"], "cookies.pkl")
```

## Authentication & XSRF Token

> Before doing a non get request to the api you have to do a get request which sets the csrf token cookie and header. Otherwise you will get an error from the server when issuing a non get request. If using the cookie_file option you can skip this step as the client will automatically load the session an csrf token from the cookie file and set it in the headers for you.

The api server returns a fresh session token and a csrf token in the cookies on every request. The session token is used for authentication and the csrf token is used to prevent cross-site request forgery attacks. During runtime the client will automatically update the session token and csrf token on every request. If you want to persist the session token and csrf token across multiple runs of your application, you can save them to disk and load them on startup using the `getLatestSessionToken` and `getXsrfToken` methods of the  `Flexopus` class.

# API Response Format

Most of the api endpoints return a response in the following format:

```json
{
  "data": {}, // The actual data returned by the api
  "links": {}, // pagination links, such as next, previous, first, last, etc.
  "meta" {} // metadata, such as pagination information, total count, etc.
}
```

locations/{id}/map returns a svg map of the location which is used in the web application to display the location map. The svg contains the layout of the location and the bookables associated with it.

```svg
<g id="bookables">
      <g id="DESK">
        <g id="TABLE_08">
          <path id="Vector_439" opacity="0.8" d="M873.929 164.09H857.972V208.09H873.929V164.09Z" fill="white"></path>
          <path id="Vector_440" opacity="0.8" d="M875.425 191.546C876.896 191.546 878.307 190.96 879.347 189.917C880.388 188.874 880.972 187.459 880.972 185.984C880.972 184.509 880.388 183.094 879.347 182.051C878.307 181.008 876.896 180.422 875.425 180.422V191.546Z" fill="white"></path>
        </g>
```

<p align="center">
  <img alt="Haha yes " width="250px" src="https://i.imgur.com/5bXJeZt.png">
  <br>
</p>