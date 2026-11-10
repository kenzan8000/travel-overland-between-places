# Confidence: rating facts, showing conflicts, ways to check

Confidence answers one question: **is this information correct now?** Whether the
service runs on time is a different question, handled in `reliability.md`.

## Rate each fact, then the option

Facts go stale at different speeds:

- **Slow:** where a station is, which station serves which direction.
- **Medium:** prices, booking rules, operators.
- **Fast:** minibus and shared-taxi times and routes, "leaves when full" windows,
  border rules, seasonal timetables, anything after a fare or currency change.

An option is only as confident as the weakest fact the user relies on to take the trip
(boarding point, that it runs, the day). Weaker side facts (exact fare after a currency
change, which stop the driver prefers) go in `facts` with their own label and reason;
the option may stay Likely while those stay Uncertain.

## Labels

Ages are counted from `trip.checked_on`.

| Label | Rule |
| --- | --- |
| **Confirmed** | An official source queried for the travel date or updated within about 6 months, **or** two independent first-hand reports under 6 months old that agree. |
| **Likely** | One first-hand report under 12 months old, **or** an official timetable that is older or has no date. |
| **Uncertain** | Sources older than 12 to 24 months, sources that disagree, or only aggregator, commercial or AI-summary data. |
| **Unknown** | Nothing found. Say so instead of filling the gap. |

Downgrade one level:

- for non-bookable minibuses, shared taxis and hail-and-ride vehicles, unless a report
  from the last **6 months** exists;
- again where routes are being redrawn (for example the Philippines' Public Transport
  Modernization Program), but only when local news or posts show **this corridor** is
  affected;
- for off-season travel, holidays, road works or border changes found in recent news;
- for any border fact, one level faster than other facts.

Hard limits:

- Shared taxis, hail-and-ride vehicles and other services with **no official source**
  cannot be **Confirmed**; two agreeing first-hand reports under 6 months support
  Likely at most.
- A published timetable that recent first-hand reports contradict is **at most
  Uncertain** (bus 251 to Oybek was listed as hourly; travellers waited hours or could
  not find it).
- A route missing from an official daily departure list for several days counts as
  evidence that it is **not running**.
- Copied pages count as one source. "Two sources agree" means two independent ones.
- Aggregators, commercial transfer sellers (and their "checked on" dates, which a
  seller can set to anything), affiliate guides and AI summaries never lift a fact
  above Uncertain on their own. Community timetables that are not from the operator
  are leads only.
- Visa and entry rules are never rated from blog posts; they need an official source.

## Timelines

Before deciding what is current, line up every dated source for the service: launched,
suspended, resumed, timetable changed, stopped. Example, Tashkent to Khujand bus:
launched 2018 with 3 buses a day; stopped 2020; resumed 2021 at 09:00 and 18:00; a
ministry page with prices dated November 2022 lists 16:00; a 2025 forum says the Tajik
operator stopped; missing from the station's daily lists for 4 to 7 November 2026. The
current status comes from the newest reliable evidence, not the newest-looking page.

## Conflicts

- Show both values with their sources and dates, and rate the fact Uncertain. Do not
  pick one silently.
- Official sources conflict too: one operator with two websites can list R400 and
  R500, or 14:00 and 14:45.
- Make the ready-made message ask about exactly the conflicting fact ("Is the fare to
  Durban R400 or R500?").
- Separate an official fare matrix from what travellers actually paid; show both, with
  the date the matrix took effect.

## How the user can check (for anything below Confirmed)

Order by effort, and give the concrete link, channel or number:

1. The operator's or station's live planner, booking site or official app for the date.
2. The newest Google Maps or 2GIS reviews and photos of the station; photos of the
   timetable board are often recent.
3. The operator's or station's Facebook page, Telegram channel or Viber group.
4. A **ready-made message** for the hotel or guesthouse host, or the station's phone
   or WhatsApp. Write it in the local language and add the region's second language or
   English, plus a translation for the user. Keep it short and specific, for example:
   "Hello! Does the minibus to Dilijan still leave from the Northern bus station? What
   time is the first one on Saturday, and how much is it?"
5. Asking at the station the day before, with a local phrase and the destination
   written in local script to show.
6. A recent forum or Facebook group thread.

Always give a **backup option** when the main one is Uncertain: a hub-town route, a
bookable alternative or a private driver.

## False information on the spot

At busy stations and tourist hubs, the people who approach you first are often touts
paid to steer you elsewhere, for example around New Delhi railway station or in Cairo.
Most locals are honest; the problem is concentrated at hubs.

- "Ask at the station" means official ticket counters, uniformed staff, the information
  desk or the hotel host, never someone who approaches the user first.
- Give the official live source where one exists, so the user can check a claim in
  seconds: NTES and IRCTC in India, the Egyptian National Railways site in Egypt, the
  railway's own app elsewhere.
- Typical claims to check against an official source before acting: "your train is
  cancelled", "it's full", "the office has moved", "it's closed today", "that bus
  doesn't go there anymore", "your hotel is closed", "foreigners can't take this train".
- Agree the full price before getting in: per seat or for the whole car, and in which
  currency. One traveller agreed 50,000 som for a shared taxi in Tashkent and the
  driver demanded $100 at arrival; another was asked for 25,000 AMD cash midway on a
  Yerevan app ride.
- Put a scam warning on a card only when recent first-hand posts report a specific scam
  at that station or on that route. Never paint a whole country as dishonest.
