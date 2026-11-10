# Border crossings

Read this when the trip crosses a border. A cross-border trip is usually three trips:
getting to the border, crossing it, and finding transport on the other side.

## Before searching

- Ask for the user's nationality (in the Step 1 question), because entry rules depend
  on it.
- Search in **both** sides' languages, plus the region's second language. Each side's
  sources often know little about the other side.
- Sources: official border and visa authorities, the user's own government's travel
  advice, recent crossing reports (for example Caravanistan for Central Asia and the
  Caucasus), local-language news for openings and closures.
- Every crossing has several names: the post on each side, the nearest town, an older
  name. Oybek (Uzbek post), Fotehobod or Fotekhobod (Tajik post), Buston and Chanak are
  one crossing. Search all of them.

## The border card (`border` in the JSON)

Keep it to what changes the plan:

```json
"border": {
  "name": "Oybek (Uzbekistan) – Fotehobod (Tajikistan)",
  "variants": ["Oybek-Buston", "Chanak", "Ойбек", "Фотеҳобод"],
  "through_or_change": "Change at the border; walk across. Cars do not usually cross.",
  "walking": "About 800 m between the posts with luggage; motor carts for a fee.",
  "open_to_foreigners": "Yes. Nearby crossings may be for locals only; use Oybek.",
  "hours": "24 hours",
  "transport_hours": "Shared taxis mostly run in daytime.",
  "each_side": "Money changers and SIM cards on the Uzbek side; little on the Tajik side. Yandex Go in Uzbekistan, Maxim in Tajikistan.",
  "before_crossing": "Change money, buy a SIM or eSIM that works on the far side, save offline maps.",
  "last_onward": "...",
  "entry_rules_url": "https://... (official)",
  "exit_rules": "Uzbek officers may check hotel registration slips; declare large amounts of cash.",
  "tips": "Waiting 30–90 min; longer on Friday afternoons and before holidays.",
  "confidence": "Likely", "confidence_reason": "...",
  "sources": ["https://..."]
}
```

- **Through or change:** whether the vehicle continues or you change, whether walking
  across is allowed (some crossings require being in a vehicle), and whether a through
  bus waits for everyone and what happens to luggage.
- **Open to foreigners and hours:** some crossings are for locals or the two
  neighbours' citizens only, and some borders are closed. Name the crossing foreigners
  must use.
- **The crossing's hours versus the transport's hours:** a 24-hour crossing does not
  mean 24-hour taxis.
- **Last onward departure on the far side.** If the plan arrives too late, warn and
  give a backup: another route or a place to stay overnight.
- **Entry rules:** link the official source for the user's nationality (visa, e-visa,
  visa on arrival at this crossing). Never state these rules from blog posts alone.
- **Exit rules** too: registration slips, currency declarations, exit stamps.
- **One tips line** for the rest: typical waiting times, time zone change, currency,
  SIM card and ride-hailing app changes, customs limits, and known scams reported in
  recent first-hand posts.

## Rating and freshness

- Border facts drop one confidence level faster than other facts.
- Claims about newly opened crossings from commercial sites need an official source.
- Always tell the user to check recent news about the crossing before going.
