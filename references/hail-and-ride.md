# Hail-and-ride vehicles and taxi ranks

Read this when an option uses a vehicle you flag down on the road or that leaves a rank
when full: jeepney (Philippines), songthaew (Thailand), angkot or bemo (Indonesia),
dolmuş (Turkey), colectivo (Latin America), matatu (Kenya), dala dala (Tanzania),
trotro (Ghana), minibus taxi (South Africa), and similar.

These have no timetable and often no fixed stops, so the usual card fields do not fit.
The questions become: where do I stand, how do I recognize the right one, how do I pay,
and how do I get off.

## Which pattern and which fields

| Pattern | Use for | Required fields |
| --- | --- | --- |
| `hail_and_ride` | Flag down on the road | `wait` (with direction of travel), `recognize`, and usually `stop` |
| `when_full` | Shared-taxi or minibus rank that leaves when full | `board` with a landmark is enough; add usual fill-up wait |
| `scheduled` | Numbered bus that uses a terminal or fixed stop | `board` / `alight`; optional `recognize` for the signboard |

A full-size bus that drops you on a highway is `scheduled`, not hail-and-ride. A boat
that waits for enough passengers is `when_full` (or `if_enough_passengers`).

## Ride fields (`hail_and_ride`)

```json
{
  "mode": "jeepney", "pattern": "hail_and_ride",
  "wait": "Terminal on [road], or the national highway, [direction] lane (towards [town])",
  "recognize": "Destination on the windshield board; ask before boarding if some only go part-way",
  "service_hours": "... (with the date of the source)",
  "price": "... reported on [date]; check whether a fare matrix rose after that",
  "payment": "Local custom (pass fare forward, pay at the window, passenger list…)",
  "stop": "Local stop phrase, or knock on the roof",
  "get_off": "Landmark, then what comes next",
  "sources": ["https://..."]
}
```

Fill every field from dated sources for **this** trip. The shape above is a template;
do not copy numbers or hours from it.

- **Where to wait:** the road or junction, and the **direction of travel** ("southbound
  lane, towards Zamboanguita"), not left or right, which depends on the country's
  traffic side.
- **How to recognize it:** colour or livery, and the exact sign wording. Jeepneys show
  place names on the side and a windshield board ("Cubao – Quiapo"), not a route number.
- **How often and when:** how often one passes, first and last service. For ranks, the
  usual fill-up wait and the time of day it is shortest.
- **Paying:** official fare matrix where one exists (for example the LTFRB matrix in the
  Philippines), with the date it took effect, next to what travellers actually paid.
  Check the news for fare changes after the latest first-hand post. Local customs differ:
  passing the fare forward, paying the driver at the window when getting off, or writing
  your name and an emergency number on a passenger list and paying up front (long South
  African minibus taxi trips).
- **Stopping:** the local phrase, and any gesture or roof knock.
- **Getting off:** the landmark, and what comes next.
- **Luggage:** whether a big bag fits or costs extra.

## Taxi ranks (minibus taxis, shared taxis, marshrutkas that leave when full)

- Cities often have several ranks, each serving different directions. Name the right
  one and how to reach it.
- Ask locals at the rank which vehicle goes to the destination; confirm with the driver
  or conductor before loading bags.
- It leaves when full: give the usual wait (one traveller waited 5 hours for a
  Durban–Underberg minibus taxi after arriving at 08:00) and when to arrive.
- Drivers may speak little of the region's second language; give the destination in
  local script and a short phrase.
- Some taxis follow fixed routes with no published maps; regional route sources help
  (Sakay.ph for Metro Manila jeepneys; Taximap.co.za for South African minibus taxis,
  not yet checked). Outside big cities, routes appear mostly in locals' posts and
  Facebook groups.

## Several rides in a row

Trips like bus to a town, jeepney, tricycle, then a boat get one short ride entry each,
in order, plus a `time_breakdown` that includes waiting. Note the last connection of the
day on each ride in `tips` or `warnings` (there is no separate schema field), and for
boats the authority that suspends trips in bad weather (for example the Philippine
Coast Guard), cash needs, and the last boat back. Separate an agreed round-trip boat
return from any published last public boat.

## Confidence

These vehicles drop one level unless a report from the last **6 months** exists, and
one more where routes are being redrawn (for example the Philippines' Public Transport
Modernization Program — check local news or posts for whether **this corridor** is
affected; do not assume a national programme changes every route). Shared taxis with no
official source cannot be Confirmed; see `confidence.md`.
