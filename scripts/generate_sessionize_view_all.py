#!/usr/bin/env python3
"""
Generate a Sessionize-like `view/all` JSON from a small YAML description.

Input YAML shape (example):

timezone: Europe/Prague          # optional, only for ISO timestamps
speakers:
  - id: spk-novak                # optional; auto from name if omitted
    name: Jan Novak
    tagline: CTU in Prague
    bio: Short bio here.
sessions:
  - id: ses-keynote              # optional; auto from title if omitted
    title: Opening Keynote
    description: Welcome talk.
    speakers: [spk-novak]        # accepts a string or list; name also works
    type: keynote                # becomes a category "Session Type"
    track: instrumentation       # becomes a category "Track"
    room: Aula                   # any string; rooms are derived automatically
    start: 2026-09-10 09:00      # parsed with timezone if provided
    end: 2026-09-10 09:45

Usage:
    python scripts/generate_sessionize_view_all.py \
        --input data/program.yaml \
        --output themes/event/assets/test/sessionize-view-all.json

Notes:
- Requires PyYAML (`pip install pyyaml`).
- profilePicture is left empty to avoid remote fetches during Hugo build.
"""

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

import yaml


def slugify(text: str, prefix: str = "") -> str:
    cleaned = (
        text.strip()
        .lower()
        .encode("ascii", "ignore")
        .decode("ascii")
    )
    cleaned = re.sub(r"[^a-z0-9]+", "-", cleaned).strip("-")
    if not cleaned:
        cleaned = "item"
    return f"{prefix}{cleaned}"


def parse_time(value: str | None, tz: str | None) -> str | None:
    if not value:
        return None
    # Accept "YYYY-MM-DD HH:MM" or full ISO; attach timezone if provided.
    try:
        if "T" in value:
            parsed = dt.datetime.fromisoformat(value)
        else:
            parsed = dt.datetime.fromisoformat(value.replace(" ", "T"))
    except ValueError:
        raise ValueError(f"Invalid datetime format: {value!r}")

    if tz and parsed.tzinfo is None:
        try:
            import zoneinfo

            parsed = parsed.replace(tzinfo=zoneinfo.ZoneInfo(tz))
        except Exception:
            # Fall back to naive time if timezone is unavailable
            pass

    return parsed.isoformat()


def ensure_speaker(entry: dict, by_id: dict, name_lookup: dict) -> dict:
    name = entry.get("name") or entry.get("fullName")
    if not name:
        raise ValueError(f"Speaker entry is missing a name: {entry}")
    speaker_id = entry.get("id") or slugify(name, "spk-")
    if speaker_id in by_id:
        return by_id[speaker_id]

    parts = name.split()
    first = parts[0]
    last = " ".join(parts[1:]) if len(parts) > 1 else ""
    speaker = {
        "id": speaker_id,
        "firstName": first,
        "lastName": last,
        "fullName": name,
        "tagLine": entry.get("tagline", ""),
        "bio": entry.get("bio", ""),
        "isTopSpeaker": bool(entry.get("isTopSpeaker", False)),
        "profilePicture": entry.get("profilePicture", ""),
        "links": entry.get("links", []),
        "sessions": [],
        "questionAnswers": [],
    }
    by_id[speaker_id] = speaker
    name_lookup[name.lower()] = speaker_id
    return speaker


def normalize_speakers(data: dict) -> dict:
    by_id: dict[str, dict] = {}
    name_lookup: dict[str, str] = {}
    for entry in data.get("speakers", []):
        ensure_speaker(entry, by_id, name_lookup)
    return {"by_id": by_id, "name_lookup": name_lookup}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Convert a minimal YAML schedule into Sessionize view/all JSON."
    )
    parser.add_argument(
        "--input",
        default="data/program.yaml",
        help="Path to YAML input (default: data/program.yaml)",
    )
    parser.add_argument(
        "--output",
        default="themes/event/assets/test/sessionize-view-all.json",
        help="Path to write JSON output (default: themes/event/assets/test/sessionize-view-all.json)",
    )
    parser.add_argument(
        "--track-title",
        default="Track",
        help="Title for the track category (default: Track)",
    )
    parser.add_argument(
        "--type-title",
        default="Session Type",
        help="Title for the session type category (default: Session Type)",
    )
    args = parser.parse_args(argv)

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Input file not found: {input_path}", file=sys.stderr)
        return 1

    raw = yaml.safe_load(input_path.read_text(encoding="utf-8")) or {}
    timezone = raw.get("timezone")
    speaker_data = normalize_speakers(raw)
    speakers_by_id = speaker_data["by_id"]
    speaker_name_lookup = speaker_data["name_lookup"]

    rooms = {}
    tracks_declared = raw.get("tracks") or []
    track_items = []
    if isinstance(tracks_declared, list):
        for idx, item in enumerate(tracks_declared):
            if isinstance(item, str):
                track_items.append(
                    {"id": slugify(item, "track-"), "name": item, "sort": idx}
                )
            elif isinstance(item, dict):
                name = item.get("name")
                if not name:
                    raise ValueError(f"Track entry missing 'name': {item}")
                track_items.append(
                    {
                        "id": item.get("id") or slugify(name, "track-"),
                        "name": name,
                        "sort": item.get("sort", idx),
                    }
                )
    track_map = {t["name"].lower(): t for t in track_items}

    types = set()
    sessions = []

    for idx, sess in enumerate(raw.get("sessions", []), 1):
        title = sess.get("title") or f"Session {idx}"
        session_id = sess.get("id") or slugify(title, "ses-")
        track = sess.get("track") or "general"
        track_lower = str(track).lower()
        if track_lower in track_map:
            track_id = track_map[track_lower]["id"]
            track_name = track_map[track_lower]["name"]
        else:
            track_id = slugify(track, "track-")
            track_name = track
            track_items.append(
                {"id": track_id, "name": track_name, "sort": len(track_items)}
            )
            track_map[track_lower] = track_items[-1]

        session_type = sess.get("type") or "session"
        type_id = slugify(session_type, "type-")
        types.add((type_id, session_type))

        room_name = sess.get("room") or "Main Hall"
        room_id = rooms.get(room_name, {}).get("id") or slugify(room_name, "room-")
        rooms[room_name] = {"id": room_id, "name": room_name}

        speaker_refs = sess.get("speakers") or sess.get("speaker") or []
        if isinstance(speaker_refs, str):
            speaker_refs = [speaker_refs]
        speaker_ids = []
        for ref in speaker_refs:
            spk = speakers_by_id.get(ref) or speakers_by_id.get(speaker_name_lookup.get(str(ref).lower(), ""))
            if not spk:
                spk = ensure_speaker({"name": ref}, speakers_by_id, speaker_name_lookup)
            speaker_ids.append(spk["id"])
            spk["sessions"].append(session_id)

        starts_at = parse_time(sess.get("start"), timezone)
        ends_at = parse_time(sess.get("end"), timezone)

        sessions.append(
            {
                "id": session_id,
                "title": title,
                "description": sess.get("description", ""),
                "startsAt": starts_at,
                "endsAt": ends_at,
                "roomId": room_id,
                "isServiceSession": bool(sess.get("isServiceSession", False)),
                "isPlenumSession": False,
                "speakers": speaker_ids,
                "categoryItems": [track_id, type_id],
            }
        )

        categories = []
    if track_items:
        categories.append(
            {
                "id": "cat-track",
                "title": args.track_title,
                "items": [
                    {"id": item["id"], "name": item["name"], "sort": item["sort"]}
                    for item in sorted(track_items, key=lambda t: t["sort"])
                ],
            }
        )
    if types:
        categories.append(
            {
                "id": "cat-type",
                "title": args.type_title,
                "items": [
                    {"id": tid, "name": name, "sort": i}
                    for i, (tid, name) in enumerate(sorted(types, key=lambda x: x[1]))
                ],
            }
        )

    data = {
        "sessions": sessions,
        "speakers": list(speakers_by_id.values()),
        "questions": [],
        "categories": categories,
        "rooms": list(rooms.values()),
    }

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {output_path} ({len(sessions)} sessions, {len(speakers_by_id)} speakers)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
