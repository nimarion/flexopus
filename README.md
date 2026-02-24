# flexopus

## TODO

For all non GET requests. API servers returns html which says javscript needs to be enabled.
Following curl call works.
```bash
curl 'https://xyz.flexopus.com/internal-api/bookings/660983' \
  -X DELETE \
  -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:148.0) Gecko/20100101 Firefox/148.0' \
  -H 'Origin: https://xyz.flexopus.com' \
  -H 'Cookie: XSRF-TOKEN=fsdfsdfds0%3D; flexopus_session=sfsdfsd0%3D' \
  -H 'X-XSRF-TOKEN: fsdfds' 
```

- internal-api/v2/location/%spaceId%/bookables?from=2025-12-19T00:00:00.000%2B01:00&to=2025-12-19T23:59:00.000%2B01:00&include_past=true
- internal-api/favourites
- internal-api/bookables/1936/conflicts?from=2025-12-20T00:00:00.000%2B01:00&to=2025-12-20T23:59:00.000%2B01:00
- internal-api/bookings/conflicts?from=2025-12-20T00:00:00.000%2B01:00&to=2025-12-20T23:59:00.000%2B01:00&bookable_type=DESK&timezone=Europe%2FBerlin
- internal-api/location/39/bookables/1936/book POST
  - {"from_time":"2025-12-20T00:00:00.000+01:00","to_time":"2025-12-20T23:59:00.000+01:00","skip_weekends":false}
- internal-api/bookings/625879 DELETE
- internal-api/favourites POST
  - {"type":"bookable","id":1935}
- internal-api/favourites?type=bookable&id=1935 DELETE
- internal-api/bookings/625880 PATCH
  - {"fromTime":"2025-12-19T21:17:00.000+01:00","toTime":"2025-12-19T22:30:00.000+01:00"}