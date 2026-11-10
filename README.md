# Travel overland between places

An agent skill for trips. Tell it where you are and where you want to go, and it lists
every realistic way to get there by ground or water: trains, buses, marshrutkas and
minibuses, shared taxis, jeepneys and other vehicles you flag down on the road, private
drivers, taxi apps, ferries and boats. Flights are out of scope.

It is built for the trips booking sites do not cover: a minibus that is on no website,
three bus stations in one town, a bus that runs only when enough people turn up, a
border you walk across. The agent searches in the languages that actually hold the
information (the region's second language such as English, Russian or French, the local
language at each end, and the languages of the country's main visitor groups), reads
official timetables, station channels and first-hand posts by locals and travellers,
and shows the result in the chat.

The output is laid out for a phone, with no tables. It starts with a one-line summary
per option, then a card for each:

| Field | Content |
| --- | --- |
| Confidence | Confirmed, Likely, Uncertain or Unknown, with the reason and the date it was last confirmed |
| Reliability | Whether it tends to run on time, and a realistic duration |
| Board and get off | The station or stop in local script, other spellings, a landmark, a map link, and how far it is from the centre |
| Departs, duration, price, pay | Times for your date and season, the fare with its date, how to pay |
| Comfort | Vehicle, air conditioning, luggage |
| Rides | One block per ride when the trip needs several, with a time breakdown including waiting |
| How to check | Concrete ways to confirm anything below Confirmed, and a ready-made message in the local language for your host or the station |
| Sources | Numbered links with dates; rejected sources with reasons |

Cross-border trips also get a border card: whether you change or walk across, opening
hours versus transport hours, what you can only get on one side, the last onward
departure, and a link to the official entry rules for your nationality.

## What's in here

```
travel-overland-between-places/
  SKILL.md                          the skill: workflow and rules for the agent
  references/confidence.md          rating rules, conflicts, ways to check, touts
  references/reliability.md         delays, connections, strikes, weather, ticket rights
  references/border-crossing.md     the border card
  references/hail-and-ride.md       jeepney-style vehicles, taxi ranks, several rides
  scripts/render_options.py         checks the JSON against the rules, prints Markdown
  scripts/check_points.py           checks boarding and arrival points on a map
  examples/plovdiv-veliko-tarnovo.json   sample input
  .env.example                      optional API keys
```

The scripts need only Python 3.9 or newer, with no extra packages. Agents that cannot
run scripts follow the manual path in `SKILL.md`.

## Install

`SKILL.md` uses the open Agent Skills format (a folder with a `SKILL.md` file and
`name`/`description` frontmatter). Copy or symlink the whole folder:

| Agent | Where |
| --- | --- |
| Claude Code | `~/.claude/skills/travel-overland-between-places/` |
| Claude apps (phone, web, desktop) | Zip the folder and upload it in the Skills section of Settings |
| Cursor | `~/.cursor/skills/travel-overland-between-places/` |
| Cursor Cloud Agents (phone, web) | Keep the folder in a repo the agent opens, under `.cursor/skills/` |
| Codex CLI | `~/.codex/skills/travel-overland-between-places/` |
| Anything else | Paste `SKILL.md` and the `references/` files into the chat or the agent's custom instructions |

Then ask something like "How do I get from Plovdiv to Veliko Tarnovo on Thursday?" or
"Tashkent to Khujand overland?" The agent needs web search and page reading.

## Optional API keys

Everything works without keys, through web search and OpenStreetMap. Keys only make
some checks faster or more certain. Copy `.env.example` to `.env` in this folder and
fill in what you have; `.env` is ignored by git. Never paste a key into the chat.

- `GOOGLE_MAPS_API_KEY`: `check_points.py` then checks stations and stops with Google
  Places (Text Search, new API) and prints a Google Maps link for each match. Enable
  "Places API (New)" in the [Google Cloud console](https://console.cloud.google.com/).
  The same key works for the `my-maps-spots` skill.
- `TRANSITLAND_API_KEY`: lets the agent query official GTFS timetables published by
  operators in many countries through [Transitland](https://www.transit.land/), for
  example `https://transit.land/api/v2/rest/stops?lat=..&lon=..&radius=500&api_key=..`.
  It helps confirm trains and scheduled buses; it rarely covers minibuses.

Regional map services (2GIS, Naver, Kakao, Amap, Mapy.com) are worth a key only if you
travel there often; their public pages are usually enough. No key solves minibus
schedules: those still come from first-hand posts and local channels.

## Running the scripts yourself

```bash
python3 scripts/check_points.py examples/plovdiv-veliko-tarnovo.json
python3 scripts/render_options.py examples/plovdiv-veliko-tarnovo.json
```

`render_options.py` options: `-o trip.md` writes the Markdown to a file. Warnings go to
stderr.

`check_points.py` options: `--mode google|osm` forces a lookup service, and
`--tolerance-m 250` changes the accepted distance (default 150 m).

The sample's facts come from a real check on 10 November 2026 and will go stale; real
runs use the sources current at the time.
