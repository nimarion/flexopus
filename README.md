# flexopus

> Before doing a non get request to the api you have to do a get request which sets the csrf token cookie and header. Otherwise you will get an error from the server when issuing a non get request.

## Terminology

- **Building**: A building is a physical structure that can contain multiple rooms. It is identified by a unique id and has a list of locations associated with it.
- **Location**: A location is a specific area within a building, such as a floor or a parking lot. It is identified by a unique id and has a list of bookables associated with it.
- **Bookable**: A bookable is a resource that can be reserved, such as a desk, meeting room or parking space. It is identified by a unique id and has a list of **reservations** associated with it.
  - Status of a bookable: Does not represent if a bookable is currently reserved or not, but rather if it is available for reservation. A bookable can be unavailable for reservation if it is under maintenance or if it is restricted to certain users or groups.
- **Booking**: A booking is a reservation of a bookable for a specific time period. It is identified by a unique id and has a start time, end time and a reference to the bookable that is being reserved.

## Usage

- [Examples](examples/)

```python
from flexopus import FlexopusClient
import os

client = FlexopusClient(os.environ["FLEXOPUS_HOST"], os.environ["FLEXOPUS_TOKEN"])
```