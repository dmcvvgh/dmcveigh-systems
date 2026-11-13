"""Tournament facts and rules for the Bulldog Bash (Gonzaga Club Volleyball, men's and women's).

This file has the *facts* (teams, pools, Saturday schedule for each division) and the
*rules* (standings, seeding, single-elimination brackets). It has no Streamlit code,
so it can be tested on its own. Rules take a `Division` so the same code runs both sides.
"""

from __future__ import annotations

import json
import re
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

DAYS = {"Sat": "Saturday, Nov 14", "Sun": "Sunday, Nov 15"}
DAY_DATES = {"Sat": "20261114", "Sun": "20261115"}
# Estimated game lengths in minutes, used to tell when a team is busy.
POOL_MINUTES = {2: 60, 3: 90}   # by number of sets in a pool match
BRACKET_MINUTES = 75            # Sunday best-of-3

BYE = "BYE"  # an empty bracket slot: the other team advances automatically
BRACKETS = ["Gold", "Silver", "Bronze"]
STAT_FIELDS = ["Kills", "Aces", "Blocks", "Digs", "Assists", "Errors"]

# ---------- Facts: organizations, teams, pools, schedule ----------

# Colors for each school / rec program, used to draw its badge logo.
ORGS = {
    "GU":   {"name": "Gonzaga",        "abbr": "GU",   "bg": "#041E42", "ring": "#C8102E", "fg": "#FFFFFF"},
    "WHIT": {"name": "Whitworth",      "abbr": "WHIT", "bg": "#A6192E", "ring": "#111111", "fg": "#FFFFFF"},
    "UL":   {"name": "Upper Left",     "abbr": "UL",   "bg": "#0F4C5C", "ring": "#F28C28", "fg": "#FFFFFF"},
    "MCD":  {"name": "McDonald's",     "abbr": "McD",  "bg": "#DA291C", "ring": "#FFC72C", "fg": "#FFC72C"},
    "GRIZ": {"name": "Montana",        "abbr": "GRIZ", "bg": "#70263C", "ring": "#A7A9AC", "fg": "#FFFFFF"},
    "UI":   {"name": "Idaho",          "abbr": "UI",   "bg": "#111111", "ring": "#B3A369", "fg": "#E8D9A0"},
    "MSU":  {"name": "Montana State",  "abbr": "MSU",  "bg": "#00205B", "ring": "#B9975B", "fg": "#FFFFFF"},
    "UW":   {"name": "Washington",     "abbr": "UW",   "bg": "#4B2E83", "ring": "#B7A57A", "fg": "#FFFFFF"},
    "EWU":  {"name": "Eastern Washington", "abbr": "EWU", "bg": "#A10022", "ring": "#1A1A1A", "fg": "#FFFFFF"},
    "KOK":  {"name": "Kokua",          "abbr": "KOK",  "bg": "#1B7F5B", "ring": "#F4D35E", "fg": "#FFFFFF"},
    "WSU":  {"name": "Washington State", "abbr": "WSU", "bg": "#981E32", "ring": "#5E6A71", "fg": "#FFFFFF"},
    # Women's-only clubs. Colors are placeholders until we know the real ones.
    "MM":   {"name": "MM",             "abbr": "MM",   "bg": "#4A5568", "ring": "#A0AEC0", "fg": "#FFFFFF"},
    "BSQ":  {"name": "Butterset Squash", "abbr": "BSQ", "bg": "#C77D1A", "ring": "#2F855A", "fg": "#FFFFFF"},
}


@dataclass
class Division:
    """One side of the tournament (men's or women's): its own teams, pools, schedule and saved data."""
    key: str                    # "men" / "women": used in the page link and the database row id
    name: str                   # "Men's" / "Women's"
    teams: dict                 # team name -> (organization key, small label shown under the badge letters)
    pools: dict                 # pool letter -> team names
    sets_per_match: dict        # pool letter -> number of sets in a pool match
    schedule: list              # (pool, time, court, team 1, team 2, ref), copied from the tournament sheet
    bracket_sizes: dict         # starting number of teams in each Sunday bracket (changeable in the app)
    bracket_count: int = 3      # how many brackets: 1 = Gold, 2 = Gold + Silver, 3 = + Bronze (changeable)
    all_teams: list = field(init=False)
    matches: list = field(init=False)
    courts: list = field(init=False)

    def __post_init__(self):
        self.all_teams = sorted(self.teams)
        self.matches = _build_matches(self)
        self.courts = sorted({m["court"] for m in self.matches})
        _check(self)


def _check(div: Division) -> None:
    """Catch typos in the facts right away, instead of as wrong standings later."""
    for pool, teams in div.pools.items():
        for t in teams:
            assert t in div.teams, f"{div.name} pool {pool}: unknown team {t!r}"
    for pool, clock, court, t1, t2, ref in div.schedule:
        for t in (t1, t2):
            assert t in div.pools[pool], f"{div.name} {clock} court {court}: {t!r} isn't in pool {pool}"
        assert ref in div.teams, f"{div.name} {clock} court {court}: unknown ref {ref!r}"
    for org, _ in div.teams.values():
        assert org in ORGS, f"{div.name}: unknown organization {org!r}"


# ---------- Men's ----------

_MEN_TEAMS = {
    "GU A": ("GU", "A"), "GU B": ("GU", "B"),
    "Whitworth": ("WHIT", ""),
    "McDonald's": ("MCD", ""),
    "Griz VB": ("GRIZ", "VB"),
    "UI A": ("UI", "A"), "UI B": ("UI", "B"),
    "MSU A": ("MSU", "A"), "MSU B": ("MSU", "B"),
    "UW A": ("UW", "A"), "UW B": ("UW", "B"),
    "EWU": ("EWU", ""),
    "Kokua 18": ("KOK", "18"), "Kokua 16": ("KOK", "16"),
    "WSU A": ("WSU", "A"), "WSU B": ("WSU", "B"),
    "Upper Left A": ("UL", "A"), "Upper Left B": ("UL", "B"), "Upper Left C": ("UL", "C"),
    "Upper Left D": ("UL", "D"), "Upper Left E": ("UL", "E"), "Upper Left F": ("UL", "F"),
}

_MEN_POOLS = {
    "A": ["GU A", "Whitworth", "Upper Left E", "McDonald's"],
    "B": ["Upper Left A", "Griz VB", "UI A", "MSU B"],
    "C": ["UW A", "EWU", "Kokua 18", "Upper Left D"],
    "D": ["UW B", "WSU B", "Upper Left C", "UI B"],
    "E": ["MSU A", "GU B", "Upper Left F"],
    "F": ["WSU A", "Upper Left B", "Kokua 16"],
}
_MEN_SETS = {"A": 2, "B": 2, "C": 2, "D": 2, "E": 3, "F": 3}

# Saturday pool play, copied from the tournament sheet: (pool, time, court, team 1, team 2, ref)
_MEN_SCHEDULE = [
    ("A", "8:30", 1, "GU A", "Whitworth", "UW A"),
    ("A", "8:30", 2, "McDonald's", "Upper Left E", "Kokua 18"),
    ("A", "10:30", 1, "GU A", "Upper Left E", "Upper Left D"),
    ("A", "10:30", 2, "Whitworth", "McDonald's", "EWU"),
    ("A", "12:30", 1, "GU A", "McDonald's", "Kokua 18"),
    ("A", "12:30", 2, "Upper Left E", "Whitworth", "UW A"),
    ("B", "8:30", 3, "Upper Left A", "Griz VB", "UW B"),
    ("B", "8:30", 4, "UI A", "MSU B", "Upper Left C"),
    ("B", "10:30", 3, "Upper Left A", "MSU B", "UI B"),
    ("B", "10:30", 4, "Griz VB", "UI A", "WSU B"),
    ("B", "12:30", 3, "Upper Left A", "UI A", "Upper Left C"),
    ("B", "12:30", 4, "MSU B", "Griz VB", "UI B"),
    ("C", "9:30", 1, "UW A", "EWU", "Upper Left E"),
    ("C", "9:30", 2, "Kokua 18", "Upper Left D", "Whitworth"),
    ("C", "11:30", 1, "UW A", "Upper Left D", "GU A"),
    ("C", "11:30", 2, "Kokua 18", "EWU", "Upper Left E"),
    ("C", "1:30", 1, "UW A", "Kokua 18", "McDonald's"),
    ("C", "1:30", 2, "Upper Left D", "EWU", "Whitworth"),
    ("D", "9:30", 3, "UW B", "WSU B", "Upper Left A"),
    ("D", "9:30", 4, "Upper Left C", "UI B", "Griz VB"),
    ("D", "11:30", 3, "UW B", "UI B", "MSU B"),
    ("D", "11:30", 4, "WSU B", "Upper Left C", "UI A"),
    ("D", "1:30", 3, "UW B", "Upper Left C", "Griz VB"),
    ("D", "1:30", 4, "UI B", "WSU B", "MSU B"),
    ("E", "10:00", 5, "MSU A", "GU B", "Upper Left F"),
    ("E", "1:00", 5, "MSU A", "Upper Left F", "GU B"),
    ("E", "2:30", 4, "GU B", "Upper Left F", "MSU A"),
    ("F", "8:30", 5, "WSU A", "Upper Left B", "Kokua 16"),
    ("F", "11:30", 5, "WSU A", "Kokua 16", "Upper Left B"),
    ("F", "2:30", 5, "Upper Left B", "Kokua 16", "WSU A"),
]


# ---------- Women's (from screenshots/womens-schedule-sheet.png) ----------

_WOMEN_TEAMS = {
    "GU A": ("GU", "A"), "GU B": ("GU", "B"),
    "Griz VBC": ("GRIZ", "VBC"),
    "WSU A": ("WSU", "A"), "WSU B": ("WSU", "B"),
    "UI": ("UI", ""),
    "Upper Left": ("UL", ""),
    "MSU A": ("MSU", "A"), "MSU B": ("MSU", "B"),
    "Butterset Squash": ("BSQ", ""),
    "MM": ("MM", ""),
}

_WOMEN_POOLS = {
    "A": ["GU A", "Griz VBC", "WSU B", "UI"],
    "B": ["WSU A", "Upper Left", "MSU B", "Butterset Squash"],
    "C": ["MSU A", "MM", "GU B"],
}
_WOMEN_SETS = {"A": 2, "B": 2, "C": 3}

# The sheet's short names: "Griz" = Griz VBC, "Squash" = Butterset Squash, "UL" = Upper Left.
_WOMEN_SCHEDULE = [
    ("A", "8:30", 6, "GU A", "UI", "WSU A"),
    ("A", "8:30", 7, "Griz VBC", "WSU B", "MSU B"),
    ("A", "10:30", 6, "GU A", "Griz VBC", "Butterset Squash"),
    ("A", "10:30", 7, "UI", "WSU B", "Upper Left"),
    ("A", "12:30", 6, "GU A", "WSU B", "MSU B"),
    ("A", "12:30", 7, "Griz VBC", "UI", "WSU A"),
    ("B", "9:30", 6, "WSU A", "Butterset Squash", "UI"),
    ("B", "9:30", 7, "Upper Left", "MSU B", "GU A"),
    ("B", "11:30", 6, "WSU A", "MSU B", "Griz VBC"),
    ("B", "11:30", 7, "Upper Left", "Butterset Squash", "WSU B"),
    ("B", "1:30", 6, "WSU A", "Upper Left", "GU A"),
    ("B", "1:30", 7, "MSU B", "Butterset Squash", "UI"),
    ("C", "8:30", 8, "MSU A", "MM", "GU B"),
    ("C", "10:00", 8, "MSU A", "GU B", "MM"),
    ("C", "11:30", 8, "MM", "GU B", "MSU A"),
]


def clock_label(minutes: int) -> str:
    """Minutes after midnight -> '1:30 PM'."""
    hour, minute = divmod(minutes, 60)
    return f"{(hour - 1) % 12 + 1}:{minute:02d} {'AM' if hour < 12 else 'PM'}"


def _time_info(clock: str) -> tuple[int, str]:
    """'1:30' -> (810 minutes after midnight, '1:30 PM'). Hours before 7 are afternoon."""
    hour, minute = (int(x) for x in clock.split(":"))
    if hour < 7:
        hour += 12
    return hour * 60 + minute, clock_label(hour * 60 + minute)


def _build_matches(div: Division) -> list[dict]:
    matches, counter = [], {}
    for pool, clock, court, t1, t2, ref in div.schedule:
        counter[pool] = counter.get(pool, 0) + 1
        minutes, label = _time_info(clock)
        matches.append({
            "id": f"{pool}{counter[pool]}", "pool": pool, "minutes": minutes, "time": label,
            "court": court, "team1": t1, "team2": t2, "ref": ref, "sets": div.sets_per_match[pool],
        })
    return sorted(matches, key=lambda m: (m["minutes"], m["court"]))


DIVISIONS = {
    "men": Division("men", "Men's", _MEN_TEAMS, _MEN_POOLS, _MEN_SETS, _MEN_SCHEDULE,
                    bracket_sizes={"Gold": 8, "Silver": 8, "Bronze": 8}),
    # 11 teams: three brackets of 4 (one BYE). Sizes can be changed in the app's Seeding panel.
    "women": Division("women", "Women's", _WOMEN_TEAMS, _WOMEN_POOLS, _WOMEN_SETS, _WOMEN_SCHEDULE,
                      bracket_sizes={"Gold": 4, "Silver": 4, "Bronze": 4}),
}
ALL_COURTS = sorted({c for d in DIVISIONS.values() for c in d.courts})


def pool_of(div: Division, team: str) -> str:
    return next(p for p, teams in div.pools.items() if team in teams)


# ---------- Storage: the JSON "database" ----------

def empty_data(div: Division) -> dict:
    return {
        "pool_results": {},  # match id -> [[team1 points, team2 points], ...] one pair per set
        "bracket_count": div.bracket_count,  # how many of Gold / Silver / Bronze are in use
        "brackets": {b: {"size": div.bracket_sizes[b], "seeds": None, "results": {}} for b in BRACKETS},
        "stats": [],         # list of stat rows (see STAT_FIELDS)
        "refs": {},          # game key -> ref team; overrides the sheet on Saturday (None = unassigned)
        "sunday_schedule": {},  # "Gold:R0M1" -> {"start": minutes after midnight, "court": n}
    }


# ---------- Storage: Supabase when connected, otherwise data.json ----------

# Each division is one row in the same table: "2026-men" and "2026-women".
DB_TABLE, YEAR = "bulldog_bash", "2026"
_db = None  # a Supabase client once use_supabase() is called; None means "use local files"


def use_supabase(client) -> None:
    """Save to Supabase (shared by every device) instead of local data-<division>.json files."""
    global _db
    _db = client


def _row_id(div: Division) -> str:
    return f"{YEAR}-{div.key}"


def _data_file(div: Division) -> Path:
    return Path(__file__).parent / f"data-{div.key}.json"


def storage_name(div: Division) -> str:
    return f"Supabase (shared), row {_row_id(div)}" if _db is not None else f"{_data_file(div).name} on this computer"


def _read_saved(div: Division) -> dict | None:
    if _db is not None:
        rows = _db.table(DB_TABLE).select("data").eq("id", _row_id(div)).execute().data
        return rows[0]["data"] if rows else None
    path = _data_file(div)
    if path.exists():
        try:
            return json.loads(path.read_text())
        except json.JSONDecodeError:
            return None
    return None


def load_data(div: Division) -> dict:
    data = empty_data(div)
    saved = _read_saved(div)
    if saved:
        data["pool_results"] = saved.get("pool_results", {})
        data["stats"] = saved.get("stats", [])
        data["refs"] = saved.get("refs", {})
        data["sunday_schedule"] = saved.get("sunday_schedule", {})
        data["bracket_count"] = saved.get("bracket_count", div.bracket_count)
        for b in BRACKETS:
            data["brackets"][b].update(saved.get("brackets", {}).get(b, {}))
    return data


def save_data(div: Division, data: dict) -> None:
    if _db is not None:
        _db.table(DB_TABLE).upsert({"id": _row_id(div), "data": data,
                                    "updated_at": datetime.now(timezone.utc).isoformat()}).execute()
    else:
        _data_file(div).write_text(json.dumps(data, indent=2))


# ---------- Rules: scoring and standings ----------

def played_sets(sets: list) -> list:
    """Only sets where someone scored count as played (0-0 means not entered)."""
    return [s for s in sets or [] if s[0] or s[1]]


def sets_won(sets: list) -> tuple[int, int]:
    sets = played_sets(sets)
    return sum(a > b for a, b in sets), sum(b > a for a, b in sets)


def match_winner(team1: str, team2: str, sets: list) -> str | None:
    w1, w2 = sets_won(sets)
    if w1 > w2:
        return team1
    if w2 > w1:
        return team2
    return None  # not played yet, or a split (e.g. 1-1 in a 2-set pool match)


def result_summary(team1: str, team2: str, sets: list) -> str:
    sets = played_sets(sets)
    if not sets:
        return ""
    scores = ", ".join(f"{a}–{b}" for a, b in sets)
    w1, w2 = sets_won(sets)
    winner = match_winner(team1, team2, sets)
    if winner:
        return f"{winner} {max(w1, w2)}–{min(w1, w2)} ({scores})"
    return f"Split {w1}–{w2} ({scores})"


def pool_standings(div: Division, pool: str, pool_results: dict) -> list[dict]:
    """Rank a pool by sets won, then point differential, then points scored."""
    rows = {t: {"Team": t, "Played": 0, "Sets W": 0, "Sets L": 0, "Pts For": 0, "Pts Against": 0}
            for t in div.pools[pool]}
    for m in div.matches:
        if m["pool"] != pool:
            continue
        sets = played_sets(pool_results.get(m["id"], []))
        if not sets:
            continue
        a, b = rows[m["team1"]], rows[m["team2"]]
        a["Played"] += 1
        b["Played"] += 1
        for p1, p2 in sets:
            a["Pts For"] += p1
            a["Pts Against"] += p2
            b["Pts For"] += p2
            b["Pts Against"] += p1
            if p1 > p2:
                a["Sets W"] += 1
                b["Sets L"] += 1
            elif p2 > p1:
                b["Sets W"] += 1
                a["Sets L"] += 1
    for r in rows.values():
        r["Diff"] = r["Pts For"] - r["Pts Against"]
    ordered = sorted(rows.values(), key=lambda r: (-r["Sets W"], -r["Diff"], -r["Pts For"], r["Team"]))
    for place, r in enumerate(ordered, start=1):
        r["Place"] = place
    return ordered


def overall_ranking(div: Division, pool_results: dict) -> list[str]:
    """Rank every team across pools: pool finish first, then set win %, then point diff per set.
    Percentages and per-set numbers make 3-team and 4-team pools comparable."""
    entries = []
    for pool in div.pools:
        for r in pool_standings(div, pool, pool_results):
            total_sets = r["Sets W"] + r["Sets L"]
            pct = r["Sets W"] / total_sets if total_sets else 0
            per_set = r["Diff"] / total_sets if total_sets else 0
            entries.append((r["Place"], -pct, -per_set, r["Team"]))
    return [team for *_, team in sorted(entries)]


# ---------- Rules: Sunday brackets ----------

def active_brackets(data: dict) -> list[str]:
    """The brackets in use for this division: Gold, then Silver, then Bronze."""
    return BRACKETS[:data.get("bracket_count", len(BRACKETS))]


def bracket_spots(teams: int) -> int:
    """A single-elimination bracket needs 2, 4, 8 or 16 spots. 6 teams -> 8 spots (2 BYEs)."""
    spots = 2
    while spots < teams:
        spots *= 2
    return spots


def project_seeds(ranking: list[str], sizes: dict[str, int]) -> dict[str, list[str]]:
    """Fill each bracket in order (Gold first) with its number of teams, in ranking order.
    Leftover spots become BYEs; they land on the top seeds, who skip the first round."""
    seeds, i = {}, 0
    for b, teams in sizes.items():
        chunk = ranking[i:i + teams]
        seeds[b] = chunk + [BYE] * (bracket_spots(teams) - len(chunk))
        i += teams
    return seeds


def bracket_order(size: int) -> list[int]:
    """Standard seeding order so 1 and 2 can only meet in the final. 8 -> [1,8,4,5,2,7,3,6]."""
    order = [1]
    while len(order) < size:
        n = len(order) * 2
        order = [x for s in order for x in (s, n + 1 - s)]
    return order


def round_name(teams_in_round: int) -> str:
    return {2: "Final", 4: "Semifinals", 8: "Quarterfinals"}.get(teams_in_round, f"Round of {teams_in_round}")


def resolve_bracket(seeds: list[str], results: dict) -> tuple[list[list[dict]], str | None]:
    """Work out every match in the bracket from the seeds and the scores entered so far.

    Returns (rounds, champion). Each match has its two teams (a name, BYE, or None for
    'winner not decided yet'), its set scores, and its winner. Results are stored with the
    team names, so a score only counts if it belongs to the same two teams.
    """
    current = [seeds[s - 1] for s in bracket_order(len(seeds))]
    rounds, r = [], 0
    while len(current) > 1:
        matches, next_round = [], []
        for i in range(0, len(current), 2):
            a, b = current[i], current[i + 1]
            match_id = f"R{r}M{i // 2}"
            saved = results.get(match_id)
            sets = saved["sets"] if saved and saved.get("teams") == [a, b] else []
            if a is None or b is None:
                winner = None                      # waiting on an earlier match
            elif a == BYE or b == BYE:
                winner = b if a == BYE else a      # a bye: the other slot advances (BYE vs BYE -> BYE)
            else:
                winner = match_winner(a, b, sets)
            matches.append({"id": match_id, "teams": [a, b], "sets": sets, "winner": winner})
            next_round.append(winner)
        rounds.append(matches)
        current, r = next_round, r + 1
    champion = current[0] if current and current[0] not in (None, BYE) else None
    return rounds, champion


def pool_complete(div: Division, pool: str, pool_results: dict) -> bool:
    """True once every match in the pool has a score."""
    return all(played_sets(pool_results.get(m["id"])) for m in div.matches if m["pool"] == pool)


def projected_seeds(div: Division, pool_results: dict, sizes: dict[str, int]) -> dict[str, list]:
    """The live projection from pool play. A team stays None (shown as TBD) until every match
    in its pool has a score; its exact seed can still move until all pools are finished."""
    finished = {t for p in div.pools if pool_complete(div, p, pool_results) for t in div.pools[p]}
    seeds = project_seeds(overall_ranking(div, pool_results), sizes)
    return {b: [t if t == BYE or t in finished else None for t in s] for b, s in seeds.items()}


def bracket_seeds(div: Division, data: dict) -> dict[str, list]:
    """Locked seeds where they exist, otherwise the live projection from pool play."""
    sizes = {b: data["brackets"][b]["size"] for b in active_brackets(data)}
    projected = projected_seeds(div, data["pool_results"], sizes)
    return {b: data["brackets"][b]["seeds"] or projected[b] for b in sizes}


# ---------- Calendar: every game on one timeline ----------

def build_events(div: Division, data: dict) -> list[dict]:
    """One list of every game this weekend: Saturday pool games, plus Sunday bracket games
    that have been given a time. The calendar, refs and overview all read from this."""
    refs = data["refs"]
    events = []
    for m in div.matches:
        events.append({
            "key": m["id"], "day": "Sat", "start": m["minutes"], "end": m["minutes"] + POOL_MINUTES[m["sets"]],
            "court": m["court"], "teams": [m["team1"], m["team2"]], "label": f"Pool {m['pool']}",
            "group": m["pool"], "ref": refs.get(m["id"], m["ref"]), "sheet_ref": m["ref"],
            "done": bool(played_sets(data["pool_results"].get(m["id"]))),
        })
    seeds = bracket_seeds(div, data)
    for b in active_brackets(data):
        rounds, _ = resolve_bracket(seeds[b], data["brackets"][b]["results"])
        for matches in rounds:
            for m in matches:
                slot = data["sunday_schedule"].get(f"{b}:{m['id']}")
                if not slot or BYE in m["teams"]:
                    continue
                events.append({
                    "key": f"{b}:{m['id']}", "day": "Sun", "start": slot["start"],
                    "end": slot["start"] + BRACKET_MINUTES, "court": slot["court"], "teams": m["teams"],
                    "label": f"{b} {round_name(len(matches) * 2)}", "group": b,
                    "ref": refs.get(f"{b}:{m['id']}"), "sheet_ref": None, "done": m["winner"] is not None,
                })
    return sorted(events, key=lambda e: (e["day"] != "Sat", e["start"], e["court"]))


def overlaps(a: dict, b: dict) -> bool:
    """Two games overlap if they're on the same day and each starts before the other ends."""
    return a["day"] == b["day"] and a["start"] < b["end"] and b["start"] < a["end"]


def busy_teams(event: dict, events: list[dict]) -> set[str]:
    """Teams that can't ref this game: its two teams, plus anyone playing or reffing
    another game at an overlapping time."""
    busy = {t for t in event["teams"] if t}
    for other in events:
        if other["key"] != event["key"] and overlaps(other, event):
            busy.update(t for t in other["teams"] if t)
            if other["ref"]:
                busy.add(other["ref"])
    return busy


def ref_counts(events: list[dict], day: str | None = None) -> Counter:
    return Counter(e["ref"] for e in events if e["ref"] and (day is None or e["day"] == day))


def preferred_refs(div: Division, event: dict, data: dict) -> set[str]:
    """On Sunday, teams from the same bracket ('in the pool') are suggested first."""
    if event["day"] == "Sun":
        return {t for t in bracket_seeds(div, data)[event["group"]] if t not in (None, BYE)}
    return set()


def suggest_refs(div: Division, event: dict, events: list[dict], preferred: set[str] = frozenset()) -> list[str]:
    """Teams that are off during this game, best first: fewest ref duties so far,
    then teams from the same bracket, then alphabetical."""
    busy = busy_teams(event, events)
    counts = ref_counts(events)
    if event["ref"]:
        counts[event["ref"]] -= 1  # don't count this game against its own current ref
    free = [t for t in div.all_teams if t not in busy]
    return sorted(free, key=lambda t: (counts[t], t not in preferred, t))


def ref_problem(event: dict, events: list[dict]) -> str | None:
    ref = event["ref"]
    if not ref:
        return None
    if ref in event["teams"]:
        return f"{ref} is playing in this game"
    if ref in busy_teams(event, events):
        return f"{ref} is playing or reffing at an overlapping time"
    return None


def auto_assign_refs(div: Division, data: dict, day: str = "Sun") -> int:
    """Give every unassigned game on this day the top suggested ref, in time order.
    Counts are recalculated after each pick so duty spreads out evenly."""
    assigned = 0
    while True:
        events = build_events(div, data)
        todo = [e for e in events if e["day"] == day and not e["ref"]]
        for e in todo:
            options = suggest_refs(div, e, events, preferred_refs(div, e, data))
            if options:
                data["refs"][e["key"]] = options[0]
                assigned += 1
                break
        else:
            return assigned  # nothing left that can be filled


def team_ics(team: str, events: list[dict]) -> str:
    """A calendar file (.ics) with every game this team plays or refs."""
    def stamp(day, minutes):
        return f"{DAY_DATES[day]}T{minutes // 60:02d}{minutes % 60:02d}00"
    lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Bulldog Bash//Tracker//EN", "CALSCALE:GREGORIAN"]
    for e in events:
        role = "Play" if team in e["teams"] else "Ref" if e["ref"] == team else None
        if not role:
            continue
        a, b = (t or "TBD" for t in e["teams"])
        uid = re.sub(r"[^A-Za-z0-9]", "-", f"{e['key']}-{team}")
        lines += ["BEGIN:VEVENT", f"UID:{uid}@bulldog-bash", "DTSTAMP:20261112T000000Z",
                  f"DTSTART;TZID=America/Los_Angeles:{stamp(e['day'], e['start'])}",
                  f"DTEND;TZID=America/Los_Angeles:{stamp(e['day'], e['end'])}",
                  f"SUMMARY:Bulldog Bash {role}: {a} vs {b}",
                  f"LOCATION:Court {e['court']}", f"DESCRIPTION:{e['label']}", "END:VEVENT"]
    lines.append("END:VCALENDAR")
    return "\r\n".join(lines) + "\r\n"
