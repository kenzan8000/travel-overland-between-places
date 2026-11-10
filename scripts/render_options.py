#!/usr/bin/env python3
"""Render overland transport options from JSON to Markdown for the chat.

Checks the JSON against the skill's rules (every option has dated sources, ratings the
rules allow, a backup when the main option is uncertain, a border card for cross-border
trips, a reported local-language search) and prints warnings to stderr. Prints Markdown
laid out for a phone, with no tables, to stdout.

Usage:
    python3 scripts/render_options.py trip.json
    python3 scripts/render_options.py trip.json -o trip.md
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys

LEVELS = ["Unknown", "Uncertain", "Likely", "Confirmed"]
PATTERNS = {"scheduled", "if_enough_passengers", "when_full", "hail_and_ride", "on_demand", "empty_leg"}
VOLATILE_PATTERNS = {"when_full", "hail_and_ride", "if_enough_passengers", "empty_leg"}
VOLATILE_MODES = {
    "marshrutka", "minibus", "minibus taxi", "shared taxi", "jeepney", "songthaew", "angkot",
    "bemo", "dolmus", "dolmuş", "colectivo", "matatu", "dala dala", "trotro", "van",
}
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

DEFAULT_LABELS = {
    "checked": "Checked",
    "for_travel": "for travel on",
    "languages": "Searched in",
    "recommendation": "Recommendation",
    "options": "Options",
    "confidence": "Confidence",
    "last_confirmed": "last confirmed",
    "reliability": "Reliability",
    "ride": "Ride",
    "of": "of",
    "board": "Board",
    "wait": "Wait",
    "look_for": "Look for",
    "also_called": "also called",
    "from_centre": "From the centre",
    "map": "map",
    "departs": "Departs",
    "frequency": "How often",
    "service_hours": "Service hours",
    "duration": "Duration",
    "realistic": "often",
    "price": "Price",
    "pay": "Pay",
    "stop": "To stop",
    "get_off": "Get off",
    "comfort": "Comfort",
    "time_breakdown": "Time breakdown",
    "booking": "Booking",
    "tips": "From the sources",
    "phrases": "Local phrases",
    "weaker_facts": "Weaker facts",
    "how_to_check": "How to check",
    "message": "Message to send",
    "warnings": "Warnings",
    "item_sources": "Sources",
    "border": "Border crossing",
    "through_or_change": "Through or change",
    "walking": "On foot",
    "open_to_foreigners": "Open to foreigners",
    "hours": "Crossing hours",
    "transport_hours": "Transport hours",
    "each_side": "On each side",
    "before_crossing": "Before crossing",
    "last_onward": "Last onward departure",
    "entry_rules": "Entry rules (official)",
    "exit_rules": "Exit rules",
    "ruled_out": "Ruled out",
    "sources": "Sources",
    "rejected_sources": "Rejected sources",
    "no_options": "Nothing reliable was found for this trip.",
}

PATTERN_NAMES = {
    "scheduled": "scheduled",
    "if_enough_passengers": "scheduled, runs only if enough passengers",
    "when_full": "leaves when full",
    "hail_and_ride": "flag it down on the road",
    "on_demand": "on demand",
    "empty_leg": "possible, check current listings",
}

warnings_count = 0


def warn(message: str) -> None:
    global warnings_count
    warnings_count += 1
    print(f"warning: {message}", file=sys.stderr)


def md_url(url: str) -> str:
    return url.replace(" ", "%20").replace("(", "%28").replace(")", "%29")


def parse_date(value: object) -> dt.date | None:
    if not isinstance(value, str) or not value.strip():
        return None
    m = re.match(r"^(\d{4})(?:-(\d{1,2}))?(?:-(\d{1,2}))?", value.strip())
    if not m:
        return None
    year = int(m.group(1))
    month = int(m.group(2) or 6)
    day = int(m.group(3) or (15 if m.group(2) else 30))
    try:
        return dt.date(year, month, day)
    except ValueError:
        return None


def fmt_date(value: object) -> str:
    if not isinstance(value, str) or not value.strip():
        return ""
    parts = value.strip().split("-")
    try:
        if len(parts) >= 3:
            return f"{int(parts[2])} {MONTHS[int(parts[1]) - 1]} {parts[0]}"
        if len(parts) == 2:
            return f"{MONTHS[int(parts[1]) - 1]} {parts[0]}"
    except (ValueError, IndexError):
        pass
    return value.strip()


def as_list(value: object) -> list:
    if value is None or value == "":
        return []
    return value if isinstance(value, list) else [value]


def text(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        return "; ".join(text(v) for v in value if text(v))
    return str(value).strip()


def map_link(point: dict) -> str:
    lat, lon = point.get("lat"), point.get("lon")
    if isinstance(lat, (int, float)) and isinstance(lon, (int, float)):
        return f"https://www.google.com/maps/search/?api=1&query={lat:.6f},{lon:.6f}"
    return ""


class Renderer:
    def __init__(self, data: dict):
        self.data = data
        self.trip = data.get("trip") or {}
        self.labels = {**DEFAULT_LABELS, **(data.get("labels") or {})}
        self.today = parse_date(self.trip.get("checked_on")) or dt.date.today()
        self.sources = [s for s in as_list(data.get("sources")) if isinstance(s, dict)]
        self.used = [s for s in self.sources if s.get("status", "used") == "used" and s.get("url")]
        self.rejected = [s for s in self.sources if s.get("status") == "rejected"]
        self.number = {s["url"]: i + 1 for i, s in enumerate(self.used)}
        self.referenced: set[str] = set()

    def L(self, key: str) -> str:
        return self.labels.get(key, key)

    # ---------- checks ----------

    def source_refs(self, urls: list, where: str) -> str:
        links = []
        for url in as_list(urls):
            if not isinstance(url, str):
                continue
            self.referenced.add(url)
            n = self.number.get(url)
            if n is None:
                warn(f"{where}: source {url} is not in the used sources list")
                continue
            links.append(f"[{n}]({md_url(url)})")
        return " ".join(links)

    def newest_age_days(self, urls: list) -> tuple[int | None, bool]:
        ages, official = [], False
        by_url = {s.get("url"): s for s in self.used}
        for url in as_list(urls):
            src = by_url.get(url)
            if not src:
                continue
            if "official" in text(src.get("kind")).lower():
                official = True
            d = parse_date(src.get("date"))
            if d:
                ages.append((self.today - d).days)
        return (min(ages) if ages else None), official

    def check_option(self, idx: int, opt: dict) -> None:
        name = opt.get("title") or opt.get("id") or f"option {idx}"
        conf = opt.get("confidence")
        if conf not in LEVELS:
            warn(f"{name}: confidence must be one of {', '.join(LEVELS)}")
        if not opt.get("confidence_reason"):
            warn(f"{name}: confidence has no reason")
        urls = list(as_list(opt.get("sources")))
        for ride in as_list(opt.get("rides")):
            if isinstance(ride, dict):
                urls += as_list(ride.get("sources"))
        if not urls and conf != "Unknown":
            warn(f"{name}: no sources; every option needs at least one used source")
        age, official = self.newest_age_days(urls)
        volatile = any(
            isinstance(r, dict)
            and (r.get("pattern") in VOLATILE_PATTERNS or text(r.get("mode")).lower() in VOLATILE_MODES)
            for r in as_list(opt.get("rides"))
        )
        if urls and age is None:
            if official and conf == "Confirmed":
                warn(f"{name}: Confirmed, but its only official sources have no date (allowed: Likely)")
            elif not official and conf in ("Confirmed", "Likely"):
                warn(f"{name}: rated {conf} without any dated or official source (allowed: Uncertain)")
        if age is not None:
            if conf == "Confirmed" and age > 183 and not official:
                warn(f"{name}: Confirmed, but the newest source is {age} days old and none is official")
            if conf == "Confirmed" and volatile and age > 183:
                warn(f"{name}: Confirmed for a minibus, shared taxi or hail-and-ride vehicle with no report in the last 6 months")
            if conf == "Likely" and age > 365 and not official:
                warn(f"{name}: Likely, but the newest source is {age} days old")
        if conf in ("Uncertain", "Unknown", "Likely") and not as_list(opt.get("how_to_check")):
            warn(f"{name}: rated {conf} but has no how_to_check")
        for ride in as_list(opt.get("rides")):
            if not isinstance(ride, dict):
                continue
            pattern = ride.get("pattern")
            if pattern and pattern not in PATTERNS:
                warn(f"{name}: unknown pattern '{pattern}'")
            if pattern == "hail_and_ride" and not (ride.get("wait") and ride.get("recognize")):
                warn(f"{name}: hail-and-ride ride needs 'wait' and 'recognize'")
            for key in ("board", "alight"):
                point = ride.get(key)
                if isinstance(point, dict):
                    lat, lon = point.get("lat"), point.get("lon")
                    if (lat is None) != (lon is None):
                        warn(f"{name}: {key} has only one of lat/lon")
                    if isinstance(lat, (int, float)) and not -90 <= lat <= 90:
                        warn(f"{name}: {key} latitude out of range")
                    if isinstance(lon, (int, float)) and not -180 <= lon <= 180:
                        warn(f"{name}: {key} longitude out of range")

    def check(self) -> None:
        options = [o for o in as_list(self.data.get("options")) if isinstance(o, dict)]
        if not self.trip.get("checked_on"):
            warn("trip.checked_on is missing; source ages are counted from today")
        langs = [l for l in as_list(self.data.get("languages")) if isinstance(l, dict)]
        if not any(l.get("role") == "local" and l.get("found") for l in langs):
            warn("no local-language search reported in 'languages' (role 'local' with 'found')")
        for i, opt in enumerate(options, 1):
            self.check_option(i, opt)
        if options and options[0].get("confidence") in ("Uncertain", "Unknown") and len(options) < 2:
            warn("the main option is not certain and there is no backup option")
        if self.trip.get("cross_border"):
            border = self.data.get("border")
            if not isinstance(border, dict):
                warn("trip.cross_border is true but there is no border card")
            else:
                for key in ("through_or_change", "open_to_foreigners", "hours", "last_onward"):
                    if not border.get(key):
                        warn(f"border card: '{key}' is empty")
                if not border.get("entry_rules_url"):
                    warn("border card: no official entry rules link")
        for src in self.rejected:
            if not src.get("reason"):
                warn(f"rejected source {src.get('url')} has no reason")
        for src in self.used:
            if not src.get("date") and not src.get("undated"):
                warn(f"used source {src.get('url')} has no date (set \"undated\": true if the page has none)")

    # ---------- rendering ----------

    def bullet(self, label: str, value: object) -> str:
        value = text(value)
        return f"- **{label}:** {value}" if value else ""

    def point_line(self, label_key: str, point: object) -> str:
        if not isinstance(point, dict):
            return self.bullet(self.L(label_key), point)
        name = text(point.get("name"))
        local = text(point.get("local_name"))
        head = f"{name} ({local})" if local and local != name else (name or local)
        bits = [head] if head else []
        if point.get("variants"):
            bits.append(f"{self.L('also_called')} {', '.join(as_list(point['variants']))}")
        if point.get("landmark"):
            bits.append(text(point["landmark"]))
        link = map_link(point)
        if link:
            bits.append(f"[{self.L('map')}]({link})")
        line = f"- **{self.L(label_key)}:** " + " · ".join(bits)
        if point.get("from_centre"):
            line += f"\n  - {self.L('from_centre')}: {text(point['from_centre'])}"
        return line

    def ride_block(self, ride: dict, n: int, total: int, where: str, seen: set[str] | None = None) -> list[str]:
        out = []
        head_bits = [text(ride.get("mode")).capitalize(), text(ride.get("operator")), text(ride.get("service"))]
        pattern = PATTERN_NAMES.get(ride.get("pattern", ""), "")
        if pattern and ride.get("pattern") != "scheduled":
            head_bits.append(pattern)
        head = " · ".join(b for b in head_bits if b)
        out.append(f"**{self.L('ride')} {n} {self.L('of')} {total}: {head}**" if total > 1 else f"**{head}**")
        out.append("")
        lines = []
        if ride.get("wait"):
            lines.append(self.bullet(self.L("wait"), ride.get("wait")))
        if ride.get("board"):
            lines.append(self.point_line("board", ride.get("board")))
        lines.append(self.bullet(self.L("look_for"), ride.get("recognize")))
        lines.append(self.bullet(self.L("departs"), ride.get("departures")))
        lines.append(self.bullet(self.L("frequency"), ride.get("frequency")))
        lines.append(self.bullet(self.L("service_hours"), ride.get("service_hours")))
        duration = text(ride.get("duration"))
        if ride.get("realistic_duration"):
            duration = f"{duration}, {self.L('realistic')} {text(ride['realistic_duration'])}" if duration else text(ride["realistic_duration"])
        lines.append(self.bullet(self.L("duration"), duration))
        lines.append(self.bullet(self.L("price"), ride.get("price")))
        lines.append(self.bullet(self.L("pay"), ride.get("payment")))
        lines.append(self.bullet(self.L("stop"), ride.get("stop")))
        if ride.get("alight"):
            lines.append(self.point_line("get_off", ride.get("alight")))
        lines.append(self.bullet(self.L("get_off"), ride.get("get_off")))
        lines.append(self.bullet(self.L("comfort"), ride.get("comfort")))
        urls = [u for u in as_list(ride.get("sources")) if isinstance(u, str)]
        if seen is not None:
            urls = [u for u in urls if u not in seen]
            seen.update(u for u in as_list(ride.get("sources")) if isinstance(u, str))
        refs = self.source_refs(urls, where)
        if refs:
            lines.append(f"- **{self.L('item_sources')}:** {refs}")
        out += [l for l in lines if l]
        out.append("")
        return out

    def summary_line(self, i: int, opt: dict) -> str:
        title = text(opt.get("title")) or f"Option {i}"
        conf = text(opt.get("confidence"))
        note = text(opt.get("confidence_short"))
        when = fmt_date(opt.get("last_confirmed"))
        bits = []
        if note:
            bits.append(note)
        if when and (not note or when.lower() not in note.lower()):
            bits.append(when)
        detail = ", ".join(bits)
        conf_part = f"{conf} ({detail})" if detail else conf
        parts = [f"**{title}**", text(opt.get("summary")), conf_part]
        return f"{i}. " + " · ".join(p for p in parts if p)

    def option_card(self, i: int, opt: dict) -> list[str]:
        where = text(opt.get("title")) or f"option {i}"
        out = [f"### {i}. {text(opt.get('title'))}", ""]
        conf = text(opt.get("confidence"))
        reason = text(opt.get("confidence_reason"))
        when = fmt_date(opt.get("last_confirmed"))
        conf_line = conf + (f": {reason}" if reason else "")
        if when:
            conf_line += f" ({self.L('last_confirmed')} {when})"
        out.append(self.bullet(self.L("confidence"), conf_line))
        rel = self.bullet(self.L("reliability"), opt.get("reliability"))
        if rel:
            out.append(rel)
        out.append("")
        rides = [r for r in as_list(opt.get("rides")) if isinstance(r, dict)]
        cited_in_rides: set[str] = set()
        for n, ride in enumerate(rides, 1):
            out += self.ride_block(ride, n, len(rides), where, cited_in_rides)
        lines = []
        breakdown = as_list(opt.get("time_breakdown"))
        if breakdown:
            lines.append(f"- **{self.L('time_breakdown')}:** " + " → ".join(text(b) for b in breakdown))
        if opt.get("booking"):
            lines.append(self.bullet(self.L("booking"), opt.get("booking")))
        tips = as_list(opt.get("tips"))
        if tips:
            lines.append(f"- **{self.L('tips')}:**")
            lines += [f"  - {text(t)}" for t in tips]
        phrases = []
        for p in as_list(opt.get("phrases")):
            if isinstance(p, dict) and p.get("phrase"):
                s = f"*{p['phrase']}*"
                if p.get("meaning"):
                    s += f" = {p['meaning']}"
                if p.get("pronunciation"):
                    s += f" ({p['pronunciation']})"
                phrases.append(s)
        if phrases:
            lines.append(f"- **{self.L('phrases')}:** " + "; ".join(phrases))
        facts = [f for f in as_list(opt.get("facts")) if isinstance(f, dict)]
        if facts:
            lines.append(f"- **{self.L('weaker_facts')}:**")
            for f in facts:
                lines.append(f"  - {text(f.get('fact'))}: {text(f.get('confidence'))}" + (f", {text(f.get('reason'))}" if f.get("reason") else ""))
        checks = as_list(opt.get("how_to_check"))
        if checks:
            lines.append(f"- **{self.L('how_to_check')}:**")
            lines += [f"  - {text(c)}" for c in checks]
        msg = opt.get("message")
        if isinstance(msg, dict) and msg.get("local"):
            lines.append(f"- **{self.L('message')}:**")
            lines.append("")
            lines.append(f"  > {text(msg['local'])}")
            second = text(msg.get("second"))
            translation = text(msg.get("translation"))
            if second:
                lines.append("  >")
                lines.append(f"  > {second}")
            if translation and translation != second:
                lines.append("")
                lines.append(f"  *{translation}*")
        warns = as_list(opt.get("warnings"))
        if warns:
            lines.append(f"- **{self.L('warnings')}:** " + "; ".join(text(w) for w in warns))
        extra = [u for u in as_list(opt.get("sources")) if u not in cited_in_rides]
        refs = self.source_refs(extra, where)
        if refs:
            lines.append(f"- **{self.L('item_sources')}:** {refs}")
        out += lines
        out.append("")
        return out

    def border_card(self) -> list[str]:
        border = self.data.get("border")
        if not isinstance(border, dict):
            return []
        out = [f"## {self.L('border')}: {text(border.get('name'))}", ""]
        if border.get("variants"):
            out.append(f"*{self.L('also_called')} {', '.join(as_list(border['variants']))}*")
            out.append("")
        conf = text(border.get("confidence"))
        if conf:
            out.append(self.bullet(self.L("confidence"), conf + (f": {text(border.get('confidence_reason'))}" if border.get("confidence_reason") else "")))
        for key in ("through_or_change", "walking", "open_to_foreigners", "hours", "transport_hours",
                    "each_side", "before_crossing", "last_onward", "exit_rules"):
            line = self.bullet(self.L(key), border.get(key))
            if line:
                out.append(line)
        if border.get("entry_rules_url"):
            out.append(f"- **{self.L('entry_rules')}:** {md_url(text(border['entry_rules_url']))}")
        if border.get("tips"):
            out.append(self.bullet(self.L("tips"), border.get("tips")))
        refs = self.source_refs(border.get("sources"), "border card")
        if refs:
            out.append(f"- **{self.L('item_sources')}:** {refs}")
        out.append("")
        return out

    def render(self) -> str:
        t = self.trip
        out = [f"## {text(t.get('from'))} → {text(t.get('to'))}", ""]
        meta = f"*{self.L('checked')} {fmt_date(t.get('checked_on'))}"
        if t.get("date"):
            meta += f" · {self.L('for_travel')} {fmt_date(t.get('date'))}"
        out += [meta + "*", ""]
        langs = []
        for l in as_list(self.data.get("languages")):
            if isinstance(l, dict) and l.get("language"):
                s = text(l["language"])
                if l.get("found"):
                    s += f" ({text(l['found'])})"
                langs.append(s)
        if langs:
            out += [f"**{self.L('languages')}:** " + "; ".join(langs), ""]
        if self.data.get("recommendation"):
            out += [f"**{self.L('recommendation')}:** {text(self.data['recommendation'])}", ""]
        options = [o for o in as_list(self.data.get("options")) if isinstance(o, dict)]
        if not options:
            out += [self.L("no_options"), ""]
        else:
            out += [f"## {self.L('options')}", ""]
            out += [self.summary_line(i, o) for i, o in enumerate(options, 1)]
            out.append("")
            for i, o in enumerate(options, 1):
                out += self.option_card(i, o)
        out += self.border_card()
        ruled = [r for r in as_list(self.data.get("ruled_out")) if isinstance(r, dict)]
        if ruled:
            out += [f"## {self.L('ruled_out')}", ""]
            for r in ruled:
                refs = self.source_refs(r.get("sources"), "ruled out")
                line = f"- **{text(r.get('what'))}:** {text(r.get('reason'))}"
                out.append(line + (f" {refs}" if refs else ""))
            out.append("")
        if self.used:
            out += [f"## {self.L('sources')}", ""]
            for s in self.used:
                when = fmt_date(s.get("date")) or ("undated" if s.get("undated") else "")
                if s.get("checked") and not s.get("date"):
                    when += f", read {fmt_date(s['checked'])}"
                bits = [text(s.get("author")), when, text(s.get("language")), text(s.get("kind"))]
                meta = " · ".join(b for b in bits if b)
                title = text(s.get("title")) or s["url"]
                out.append(f"{self.number[s['url']]}. [{title}]({md_url(s['url'])})" + (f" · {meta}" if meta else ""))
            out.append("")
        if self.rejected:
            out += [f"**{self.L('rejected_sources')}**", ""]
            for s in self.rejected:
                title = text(s.get("title")) or text(s.get("url"))
                url = text(s.get("url"))
                link = f"[{title}]({md_url(url)})" if url else title
                out.append(f"- {link}: {text(s.get('reason'))}")
            out.append("")
        for s in self.used:
            if s["url"] not in self.referenced:
                warn(f"used source {s['url']} is not cited by any option, ride, border card or ruled-out item")
        return "\n".join(out).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("json_file")
    parser.add_argument("-o", "--output", help="write Markdown to this file instead of stdout")
    args = parser.parse_args()
    try:
        with open(args.json_file, encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"error: cannot read {args.json_file}: {exc}", file=sys.stderr)
        return 2
    renderer = Renderer(data)
    renderer.check()
    markdown = renderer.render()
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(markdown)
    else:
        sys.stdout.write(markdown)
    if warnings_count:
        print(f"{warnings_count} warning(s)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
