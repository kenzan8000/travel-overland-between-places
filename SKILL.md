---
name: travel-overland-between-places
description: Find every realistic way to get from one place to another on a trip by ground or water (train, bus, marshrutka, minibus, shared taxi, jeepney and other hail-and-ride vehicles, private driver, ride-hailing, ferry or boat, including border crossings), sourced from official timetables and dated first-hand posts by locals and travellers, searched in the region's languages. Each option shows exactly where to board, times, duration, price, how to pay, comfort, a confidence label with how to check it, and a reliability note. Use when the user asks how to get from A to B between cities, towns, villages, a border or an island, during a trip or while planning one. Flights are out of scope. The places may come later; if they are not given, ask in the chat.
---

# Overland between places on a trip

Turn "how do I get from A to B?" into a short list, shown in the chat, of every
realistic way to make that trip by ground or water. Each option says exactly where to
board, when it leaves, how long it takes, what it costs, how to pay, how comfortable it
is, how sure you are, and how the user can check.

The hard cases are the point of this skill: a minibus that is on no website, three bus
stations in one town, a bus that runs only when enough people turn up, a border you
walk across. The answer often exists only in a local-language post, a station's
Telegram channel or a traveller's forum report.

**A missing fact is better than a wrong fact. A missing link is better than a guessed
link.** Never invent times, prices, stops, phone numbers or URLs. Transport information
goes stale fast, so every fact carries the date of its newest source.

These instructions are agent-neutral. "Search the web", "open the page" and "run the
command" mean whatever tools your environment provides. If you cannot run scripts,
follow the manual path in Step 9.

## Reference files: read only when they apply

| File | Read when |
| --- | --- |
| `references/confidence.md` | Always, before Step 7. Full rating rules, ways to check, false information on the spot. |
| `references/border-crossing.md` | The trip crosses a border. |
| `references/hail-and-ride.md` | An option uses a vehicle you flag down on the road (jeepney, songthaew, dolmuş, colectivo, matatu, minibus taxi...) or a "leaves when full" taxi rank. |
| `references/reliability.md` | An option has a change, a known punctuality problem, a `when_full` or boat leg, or a likely disruption (strike, track works, weather, season), or the user asks about delays. Always for boats and ferries (Coast Guard / gale warnings). |

Paths are relative to this skill's folder.

## Step 1: Confirm the places (ask only what is missing)

- If the message names both places, go to Step 2. Do not re-ask for what is already
  clear.
- If either place is missing, your whole reply is one short question in the chat, in
  the user's language, for example:

  > Where are you starting from and where do you want to go? Add the date if you know it.

- Ask as ordinary chat text, then stop and wait. Do not search or guess first.
- Ask only if a place is ambiguous (which Alexandria?) or has several names ("Kazbegi"
  is the town of Stepantsminda). Do not ask about budget, luggage or preferences; use
  them if the user gives them.
- If the trip crosses a border, read `references/border-crossing.md`. Ask for the
  user's nationality only when it is not already in the message; entry rules depend on
  it.
- Note the **user's language** (the language of their message). Write the answer in it.
- If no date is given, plan for the next few days and say so. Note the day of week and
  the season: timetables differ by both. For "today" or "now", note the time of day if
  the message gives it, and warn when same-day services (morning boats, last buses)
  may already be gone.

## Step 2: Choose the languages and the name variants

Decide the search languages for **this** trip, never from a fixed list, and state them
in the answer:

1. **The region's second languages.** English nearly everywhere, plus any other that is
   strong there: Russian in the former Soviet Union, French in West, Central and North
   Africa, Portuguese in Angola and Mozambique, Arabic in the Middle East and North
   Africa, Spanish in Latin America.
2. **The local language(s) at each end.** Two of them across a border. This search is
   **required**, and you report what it found, even "nothing".
3. **The languages of the country's largest visitor groups**, based on where visitors
   actually come from, not on neighbours. A quick search for the country's top tourist
   source markets settles it. Chinese and Korean for Japan; Polish and Russian for
   Georgia. Stop a visitor language after the first page of results if you find only
   machine translations of SEO or commercial pages; report "nothing first-hand".
4. **English, always**, if not already covered.
5. **The user's language**, for searching only when its speakers write a lot about the
   region (Japanese for Central Asia, for example).

Examples: Bulgaria is English and Bulgarian. Georgia is English, Russian, Georgian and
Polish. Tashkent to Khujand is Russian, English, Uzbek and Tajik (add Chinese only if a
quick visitor-market search shows China among the top sources and the first results are
not SEO copies). The Philippines is English, Filipino, and Cebuano in the Visayas and
Mindanao; add Hiligaynon when local Negros or Panay news is in it.

List **name variants** for both places and for every station, bazaar, stop and border
crossing you meet: local script, transliterations, old names and every script the
language uses. Skip a name that is already Latin-only and identical across sources.
Uzbek has Xo‘jand, Хўжанд and Toşkent-style spellings; Tajik writes Хуҷанд, Russian
Худжанд. Kuyluk, Qo'yliq, Kulyuk and Куйлюк are one bazaar. Searching the wrong
spelling finds nothing.

Collect the transport words in each language: bus station, timetable, minibus, shared
taxi, ferry (for example автогара and разписание in Bulgarian, маршрутка and автовокзал
in Russian, gare routière and taxi-brousse in French).

## Step 3: Search

Run the searches in every chosen language. Open and read the pages, not the search
snippets: snippets, cached copies and AI summaries regularly show other dates, merge
services or say "no direct train" when there is one. When a page tool times out, use a
search highlight only as a lead and mark the fact Uncertain until you can read the
page; never treat a snippet as Confirmed.

In rough order of trust:

1. **Official live sources for the exact date**: the railway's or operator's journey
   planner, queried for the travel date (not a cached page from another date); official
   booking sites. Use them to confirm trains and scheduled buses.
2. **Official daily departure lists**, often on a bus station's Telegram channel or
   website. A route missing from several days' lists is evidence it is not running.
3. **Operators' own sites and phone numbers.** Small operators are often linked only
   from forum posts.
4. **Recent first-hand posts**: blogs, the local subreddit (r/dumaguete beats
   r/phtravel), forums such as Caravanistan, Seat61, Tripadvisor and national forums.
   Non-English forums often hold the only off-season reports.
5. **Local channels**: Facebook, VK and Telegram groups.
6. **News and official notices**: launches, suspensions, fare changes, strikes, road
   closures, currency changes. News describes one moment; rate it by its date.
7. **Map apps**: Google Maps, 2GIS, Yandex Maps and local apps confirm stop locations;
   recent reviews and photos of timetable boards are often the freshest evidence.
   App-only services (such as the GG Shuttle in Armenia) show up in local-language posts
   and app store descriptions, rarely in English search.

Also search for the **season and day**: "winter", "December", local month names,
"Sunday". Summer timetables dominate results.

Rules for sources:

- **Keep** a source when it is official, or first-person with signs the author was
  there (specific details, dates, photos), with an identifiable author or publication.
- **Reject** SEO listicles, sites built around one search phrase, AI-generated pages,
  pages with no author or date that only rewrite others.
- **Leads only, never proof on their own:** aggregators (Rome2rio, 12Go, Busbud, Omio,
  obilet), commercial transfer sellers and their "checked on" dates, affiliate-linked
  guides, and summaries by search tools or other AIs, including ones the user pastes in.
  Find each fact on the cited page itself.
- **Copied pages count once.** The same timetable on many sites is one source.
- Log every source you opened with its date, language, kind, status (used or rejected)
  and a one-line reason.

If a page will not load through your page tool, try another way to fetch it (for
example `curl` with a browser user agent) or the data the page itself requests. If it
still fails, say the source could not be read.

## Step 4: Build the options

Consider every kind of ground and water transport, not only what booking sites list:

- train, including routes with changes;
- scheduled bus, and a bus that **runs only if enough passengers** turn up;
- bookable shared shuttle (fixed route and timetable, booked by phone or online);
- marshrutka or minibus that leaves when full; shared taxi;
- hail-and-ride vehicle with no fixed stops (read `references/hail-and-ride.md`);
- private driver marketplace (whole car, fixed price, stops allowed);
- ride-hailing app for the whole trip or to a border; door-to-door transfers;
- spare seats on empty return trips: no timetable, list as "possible, check current
  listings", never as a schedule;
- ferry or boat;
- routes through a hub town, and trips with several rides (for example bus, then
  jeepney, then tricycle).

For each service, build a **timeline** from the sources (launched, suspended, resumed,
stopped, timetable changes) and take the current status from the newest reliable
evidence, not from the newest-looking page.

**Never leave out the local option**, even when locals warn tourists off it. List it
with first-hand notes on safety, waiting time and price, and let the user decide. A
thin Uncertain card is enough when sources are old; do not invent detail to fill it.

**Ruling out is a result too:** "no train since 2020", "the direct bus is not in the
station's lists for 4 to 7 November".

## Step 5: Pin the boarding and arrival points

For every place where the user gets on or off:

- the local name in local script, the main name variants, and the station or stop when
  a town has several (each often serves different directions);
- what it is when it is not a station: a parking lot, petrol station, McDonald's,
  shopping centre, hostel, market or street corner;
- a landmark to recognize it, and the sign wording on the vehicle;
- distance and route from the centre (walk, city bus, taxi with a rough fare), and the
  same for the arrival point, which is often far from the centre;
- coordinates: take them from the operator, a map app or a forum post, and accept them
  only if two independent sources agree within about 150 m. Nominatim alone, or
  `check_points.py`'s single candidate, is one source; a second is another map app, the
  operator, or a dated post with a pin. Informal stops (highway drop, beach wharf) often
  have no pin: describe them with a landmark and leave coordinates out. Run
  `scripts/check_points.py` (Step 9) or check manually on OpenStreetMap.

## Step 6: Fill in the details

For each option, and for each ride in a several-ride option:

- departure times **for the travel date's day of week and season**, frequency, first
  and last departure; for "leaves when full", the usual window and cut-off;
- the **return leg and its last departure** when the user may come back the same day;
  for an assigned round-trip boat, separate the agreed return time from any published
  last public boat;
- scheduled and realistic duration; for several rides, a time breakdown that includes
  waiting (for example 1.5 h to the border, 30 min at the border, 40 min waiting for the
  next taxi to fill, 2 h 20 min onward);
- price in local currency with the date of the source; after a currency change or fare
  change (check the news), mark older prices as old and convert where an official rate
  exists;
- how to pay (window, driver, app, online; cash; small notes), booking rules (prepay,
  reconfirm 24 h before), phone and messenger contacts from the sources;
- comfort: vehicle type and size, air conditioning, luggage space and fees, toilet
  stops, road;
- tips from the sources and short local phrases with meanings;
- a **late-arrival warning only when a source gives a reason** (last onward departure,
  safety advice about night travel, mountain road, border closing), with that reason;
- a **one-line reliability note** and realistic duration. Read
  `references/reliability.md` when it applies.

## Step 7: Rate confidence

Read `references/confidence.md` first. In short:

- Rate each fact; an option is only as sure as the weakest fact the user relies on.
- **Confirmed**: an official source for the date or updated within about 6 months, or
  two independent first-hand reports under 6 months old that agree. **Likely**: one
  first-hand report under 12 months, or an older or undated official timetable.
  **Uncertain**: older sources, disagreement, or aggregators only. **Unknown**: nothing
  found.
- Minibuses, shared taxis and hail-and-ride vehicles drop a level without a report from
  the last 3 to 6 months.
- Show conflicts instead of choosing one silently.
- For anything below Confirmed, give concrete ways to check and a ready-made message in
  the local language (and the region's second language) for the hotel host or station.
- When the main option is Uncertain, always give a backup option.

## Step 8: Write the JSON

If you can run scripts, write the result to a temporary file such as
`/tmp/overland-<slug>.json`. Nothing needs to be kept after the chat. A complete
example is `examples/plovdiv-veliko-tarnovo.json`.

```json
{
  "trip": {"from": "Plovdiv, Bulgaria", "to": "Veliko Tarnovo, Bulgaria",
           "slug": "plovdiv-veliko-tarnovo", "date": "2026-11-12",
           "checked_on": "2026-11-10", "user_language": "en", "cross_border": false},
  "labels": {},
  "languages": [
    {"language": "Bulgarian", "role": "local",
     "found": "BDZ timetable for the date, operators' sites"}
  ],
  "recommendation": "One or two sentences.",
  "options": [
    {
      "id": "train-direct", "title": "Direct train", "mode": "train",
      "confidence": "Confirmed", "confidence_reason": "BDZ journey planner for 12 Nov",
      "last_confirmed": "2026-11-10", "reliability": "...",
      "summary": "16:05 → 20:36 · 4 h 31 min · €7.98",
      "rides": [
        {"mode": "train", "operator": "BDZ", "service": "fast train 4632",
         "pattern": "scheduled",
         "board": {"name": "Plovdiv Central Station", "local_name": "гара Пловдив",
                   "town": "Пловдив", "search_query": "Plovdiv Central Station",
                   "variants": [], "lat": 42.134422, "lon": 24.741373,
                   "landmark": "...", "from_centre": "..."},
         "alight": {"name": "...", "local_name": "...", "from_centre": "..."},
         "departures": "16:05", "duration": "4 h 31 min",
         "realistic_duration": "", "price": "€7.98 (2nd class)",
         "payment": "...", "comfort": "...", "sources": ["https://..."]}
      ],
      "time_breakdown": [],
      "booking": "...", "tips": [], "phrases": [],
      "facts": [{"fact": "...", "confidence": "Uncertain", "reason": "..."}],
      "how_to_check": [], "message": {"local": "...", "translation": "..."},
      "warnings": [], "sources": ["https://..."]
    }
  ],
  "border": null,
  "ruled_out": [{"what": "...", "reason": "...", "sources": ["https://..."]}],
  "sources": [
    {"url": "https://...", "title": "...", "author": "...", "date": "2026-11-10",
     "language": "bg", "kind": "official timetable", "status": "used", "reason": "..."},
    {"url": "https://...", "title": "...", "undated": true, "checked": "2026-11-10",
     "kind": "official operator page", "status": "used", "reason": "..."}
  ]
}
```

- `search_query`: the name that works on maps when the local name does not (Nominatim
  finds "Veliko Tarnovo railway station" but not "гара Велико Търново").
- `town`: the town the point is in, so geocoding searches the right place.
- `confidence_short`: a few words for the summary line (for example "BDZ planner");
  do not repeat the month already in `last_confirmed`.
- `undated`: the page shows no date; `checked` is when you read it. An undated official
  page supports Likely at most.
- `message.second`: optional second language of the ready-made message (for example
  Russian next to Uzbek). Omit `translation` when it would duplicate `second` and the
  user's language is already that language.
- Ride-level `sources` are enough; option-level `sources` need only URLs not already on
  a ride. Mixed trips (scheduled bus + `when_full` boat) use one pattern per ride.

- `pattern`: `scheduled`, `if_enough_passengers`, `when_full`, `hail_and_ride`,
  `on_demand` (private driver, app, charter) or `empty_leg`.
- Hail-and-ride rides use the fields in `references/hail-and-ride.md`; the border card
  uses the fields in `references/border-crossing.md`.
- Leave out anything you could not confirm. Do not fill a field with a guess.
- `labels`: when the user's language is not English, translate the headings. The keys
  and English defaults are in `scripts/render_options.py` (`DEFAULT_LABELS`).

## Step 9: Check points and render

### With the scripts (preferred)

Both use only the Python 3 standard library.

```bash
python3 scripts/check_points.py /tmp/overland-<slug>.json
python3 scripts/render_options.py /tmp/overland-<slug>.json
```

`check_points.py` geocodes each boarding and arrival point by name (Google Places when
`GOOGLE_MAPS_API_KEY` is set in the environment or in `.env` here, OpenStreetMap
otherwise) and reports how far that is from your coordinates. Fix or remove
coordinates that are off by more than about 150 m in a town, or that nothing confirms.
For a point with no coordinates it prints one map candidate; that is a single source,
and often the wrong place (a goods siding instead of the passenger station), so add it
only when a second source agrees. Give points a `town` so the lookup searches the right
place.
If no lookup can be reached, the environment has no internet; check on OpenStreetMap
with your browsing tool instead.

`render_options.py` prints Markdown to stdout and warnings to stderr. Read every
warning: facts without a source, sources without a date, ratings the rules do not
allow, a missing backup or border card. Fix the JSON and rerun.

### Without the scripts (manual path)

Check each point's coordinates against OpenStreetMap and a second source. Write the
Markdown in the layout of Step 10. Map links are
`https://www.google.com/maps/search/?api=1&query=<lat>,<lon>`, built only from
coordinates you accepted. Escape `(`, `)` and spaces in URLs as `%28`, `%29` and `%20`.

## Step 10: Show the result in the chat

Post the Markdown as your reply, in the user's language, with one short sentence
before it. Do not only point to a file. It is laid out for a phone, with no tables:

1. A line with the date checked and the travel date, then the languages searched and
   what the local-language search found.
2. The recommendation in one or two sentences.
3. One summary line per option: name, times, duration, price, confidence and its
   reason, for example
   `1. **Direct train** · 16:05 → 20:36 · 4 h 31 min · €7.98 · Confirmed (BDZ, 10 Nov 2026)`.
4. One card per option: confidence and reliability first, then each ride (board, look
   for, departs, duration, price and payment, get off, comfort), the time breakdown,
   booking, tips, local phrases, weaker facts, how to check, the ready-made message,
   warnings, and numbered source links.
5. The border card, when the trip crosses a border.
6. What was ruled out and why.
7. Sources: used ones numbered with date, language and kind; then rejected ones with
   reasons.

If nothing reliable turned up, say so plainly and suggest the hotel host, the tourist
office or the station itself, with the ready-made message.
