#!/usr/bin/env python3
"""Check the boarding and arrival points of an overland trip JSON against a map.

For every ride's `board` and `alight` point with coordinates, looks the point up by
name and reports how far the result is from your coordinates. Uses Google Places
(Text Search, new API) when GOOGLE_MAPS_API_KEY is set in the environment or in a
`.env` file in the skill folder, and OpenStreetMap Nominatim otherwise. Points without
coordinates are listed so you can add or leave them out. Nothing is written back.

Usage:
    python3 scripts/check_points.py trip.json
    python3 scripts/check_points.py trip.json --tolerance-m 250 --mode osm
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
PLACES_SEARCH_URL = "https://places.googleapis.com/v1/places:searchText"
PLACES_FIELDS = "places.displayName,places.formattedAddress,places.location,places.googleMapsUri"
USER_AGENT = "travel-overland-between-places/1.0 (travel skill; python-urllib)"


def load_env() -> None:
    path = SKILL_DIR / ".env"
    if not path.is_file():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        name, value = line.split("=", 1)
        name = name.strip().removeprefix("export ").strip()
        value = value.strip().strip('"').strip("'")
        if name and value and not os.environ.get(name):
            os.environ[name] = value


def haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r = 6371000.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp, dl = math.radians(lat2 - lat1), math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def http_json(url: str, body: dict | None = None, headers: dict | None = None, timeout: float = 15) -> object:
    req_headers = {"User-Agent": USER_AGENT, "Accept": "application/json"}
    data = None
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        req_headers["Content-Type"] = "application/json"
    req_headers.update(headers or {})
    req = urllib.request.Request(url, data=data, headers=req_headers)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


_last_nominatim = 0.0


def nominatim(query: str, lat: float | None, lon: float | None, language: str) -> list[tuple[str, float, float]]:
    global _last_nominatim
    wait = 1.1 - (time.monotonic() - _last_nominatim)
    if wait > 0:
        time.sleep(wait)
    params = {"q": query, "format": "jsonv2", "limit": "5", "accept-language": language}
    if lat is not None and lon is not None:
        d = 0.5
        params["viewbox"] = f"{lon - d},{lat + d},{lon + d},{lat - d}"
    _last_nominatim = time.monotonic()
    results = http_json(f"{NOMINATIM_URL}?{urllib.parse.urlencode(params)}")
    return [(r.get("display_name", ""), float(r["lat"]), float(r["lon"])) for r in results or []]


def google(query: str, lat: float | None, lon: float | None, key: str, language: str) -> list[tuple[str, float, float]]:
    body = {"textQuery": query, "languageCode": language, "pageSize": 5}
    if lat is not None and lon is not None:
        body["locationBias"] = {"circle": {"center": {"latitude": lat, "longitude": lon}, "radius": 20000.0}}
    headers = {"X-Goog-Api-Key": key, "X-Goog-FieldMask": PLACES_FIELDS}
    data = http_json(PLACES_SEARCH_URL, body=body, headers=headers)
    out = []
    for p in (data or {}).get("places", []):
        loc = p.get("location") or {}
        if "latitude" in loc and "longitude" in loc:
            name = (p.get("displayName") or {}).get("text", "")
            label = f"{name}, {p.get('formattedAddress', '')}".strip(", ")
            if p.get("googleMapsUri"):
                label += f" <{p['googleMapsUri']}>"
            out.append((label, float(loc["latitude"]), float(loc["longitude"])))
    return out


def points(data: dict):
    for opt in data.get("options") or []:
        if not isinstance(opt, dict):
            continue
        for n, ride in enumerate(opt.get("rides") or [], 1):
            if not isinstance(ride, dict):
                continue
            for key in ("board", "alight"):
                point = ride.get(key)
                if isinstance(point, dict):
                    yield f"{opt.get('id') or opt.get('title')} ride {n} {key}", point


def queries(point: dict, town: str) -> list[str]:
    out = []
    if point.get("search_query"):
        out.append(point["search_query"])
    for name in (point.get("local_name"), point.get("name")):
        if name:
            q = f"{name}, {town}" if town and town.lower() not in name.lower() else name
            if q not in out:
                out.append(q)
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("json_file")
    parser.add_argument("--mode", choices=["auto", "google", "osm"], default="auto")
    parser.add_argument("--tolerance-m", type=float, default=150, help="largest accepted distance (default 150)")
    args = parser.parse_args()

    load_env()
    with open(args.json_file, encoding="utf-8") as f:
        data = json.load(f)
    trip = data.get("trip") or {}
    language = trip.get("user_language") or "en"
    name_to_code = {
        "bulgarian": "bg", "russian": "ru", "uzbek": "uz", "tajik": "tg",
        "georgian": "ka", "polish": "pl", "filipino": "fil", "tagalog": "tl",
        "cebuano": "ceb", "hiligaynon": "hil", "japanese": "ja", "korean": "ko",
        "chinese": "zh", "french": "fr", "spanish": "es", "portuguese": "pt",
        "arabic": "ar", "german": "de", "english": "en",
    }
    for lang in data.get("languages") or []:
        if isinstance(lang, dict) and lang.get("role") == "local" and lang.get("language"):
            code = name_to_code.get(str(lang["language"]).split(",")[0].strip().lower())
            if code:
                language = f"{code},{language}" if code != language else code
            break
    key = os.environ.get("GOOGLE_MAPS_API_KEY", "").strip()
    mode = args.mode if args.mode != "auto" else ("google" if key else "osm")
    if mode == "google" and not key:
        print("error: --mode google needs GOOGLE_MAPS_API_KEY", file=sys.stderr)
        return 2
    print(f"mode: {'Google Places' if mode == 'google' else 'OpenStreetMap Nominatim'}")

    problems = 0
    unreachable = 0
    with_coords = 0
    without_coords = 0
    for where, point in points(data):
        lat, lon = point.get("lat"), point.get("lon")
        label = point.get("local_name") or point.get("name") or "?"
        town = point.get("town") or ""
        if not isinstance(lat, (int, float)) or not isinstance(lon, (int, float)):
            without_coords += 1
            found = []
            for q in queries(point, town):
                try:
                    found = google(q, None, None, key, language) if mode == "google" else nominatim(q, None, None, language)
                except (urllib.error.URLError, TimeoutError, OSError, ValueError) as exc:
                    unreachable += 1
                    print(f"- {where}: {label}: no coordinates; lookup failed ({exc})")
                    break
                if found:
                    break
            if found:
                name, rlat, rlon = found[0]
                print(f"- {where}: {label}: no coordinates; one candidate {rlat:.6f}, {rlon:.6f} '{name}' "
                      "(one source only: add it only if a second source agrees)")
            elif not unreachable:
                print(f"- {where}: {label}: no coordinates and no map match; describe it with a landmark")
            continue
        with_coords += 1
        best = None
        for q in queries(point, town):
            try:
                results = google(q, lat, lon, key, language) if mode == "google" else nominatim(q, lat, lon, language)
            except (urllib.error.URLError, TimeoutError, OSError, ValueError) as exc:
                unreachable += 1
                print(f"- {where}: {label}: lookup failed ({exc})")
                break
            for name, rlat, rlon in results:
                dist = haversine_m(lat, lon, rlat, rlon)
                if best is None or dist < best[0]:
                    best = (dist, name, q)
            if best and best[0] <= args.tolerance_m:
                break
        if best is None:
            problems += 1
            print(f"- {where}: {label}: NOT FOUND by name; confirm the coordinates another way or remove them")
        elif best[0] <= args.tolerance_m:
            print(f"- {where}: {label}: ok, {best[0]:.0f} m from '{best[1]}'")
        else:
            problems += 1
            print(f"- {where}: {label}: CHECK, nearest match is {best[0]:.0f} m away: '{best[1]}' (query '{best[2]}')")
    if unreachable:
        print("Some lookups failed. If none could be reached, this environment has no internet; "
              "check the points on openstreetmap.org with your browsing tool.", file=sys.stderr)
    if without_coords and not with_coords:
        print(f"note: {without_coords} point(s) have no coordinates; nothing was distance-checked "
              "(that is fine when pins are unavailable — describe them with a landmark)", file=sys.stderr)
    print(f"{problems} point(s) to check")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
