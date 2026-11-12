"""Bulldog Bash tracker: a Streamlit app for Gonzaga Men's Club Volleyball's tournament.

Run from this folder with:  .venv/bin/streamlit run app.py --server.port 8502
"""

import base64
import html
from pathlib import Path

import pandas as pd
import streamlit as st

import tournament as tm

st.set_page_config(page_title="Bulldog Bash 2026", page_icon="🏐", layout="wide")

NAVY, RED = "#041E42", "#C8102E"
LOGO_DIR = Path(__file__).parent / "logos"

st.markdown(f"""<style>
.bb-hero {{background: linear-gradient(135deg, {NAVY} 0%, #0B2D5C 100%); color: #fff; padding: 1.3rem 1.6rem;
  border-radius: 14px; border-bottom: 6px solid {RED}; margin-bottom: 1rem;}}
.bb-hero h1 {{color: #fff; margin: .1rem 0 .2rem; padding: 0; font-size: 2.2rem;}}
.bb-kicker {{letter-spacing: .14em; font-size: .78rem; font-weight: 700; color: #C9D3E3;}}
.bb-sub {{color: #DCE3EE;}}
.bb-chip {{display: inline-flex; align-items: center; gap: .45rem; vertical-align: middle;}}
.bb-chip img {{flex: none;}}
.bb-tbd {{color: #8A94A6; font-style: italic;}}
.bb-table {{width: 100%; border-collapse: collapse; font-size: .92rem;}}
.bb-table th {{background: {NAVY}; color: #fff; padding: .45rem .5rem; text-align: center; font-weight: 600;}}
.bb-table th:nth-child(2) {{text-align: left;}}
.bb-table td {{padding: .4rem .5rem; border-bottom: 1px solid #E1E6EE; text-align: center;}}
.bb-table td:nth-child(2) {{text-align: left;}}
.bb-table tr.lead td {{background: #FDF1F3;}}
.bb-bracket {{display: flex; gap: 1.2rem; overflow-x: auto; padding: .5rem 0 1rem;}}
.bb-round {{display: flex; flex-direction: column; justify-content: space-around; min-width: 230px; flex: 1;}}
.bb-round-title {{font-weight: 700; color: {NAVY}; text-align: center; margin-bottom: .4rem;
  border-bottom: 3px solid {RED}; padding-bottom: .2rem;}}
.bb-match {{border: 1px solid #CFD7E3; border-left: 5px solid {NAVY}; border-radius: 10px; background: #fff;
  margin: .45rem 0; box-shadow: 0 1px 3px rgba(4,30,66,.08);}}
.bb-slot {{display: flex; align-items: center; gap: .4rem; padding: .35rem .55rem; min-height: 40px;}}
.bb-slot + .bb-slot {{border-top: 1px solid #E8ECF2;}}
.bb-slot .seed {{width: 1.2rem; color: #8A94A6; font-size: .8rem; text-align: right;}}
.bb-slot .score {{margin-left: auto; font-weight: 700; color: {NAVY};}}
.bb-slot.win {{background: #EAF0F8; font-weight: 700;}}
.bb-slot.lose {{opacity: .55;}}
.bb-champ {{text-align: center; border: 2px solid {RED}; border-radius: 14px; padding: 1rem; background: #FFF8F9;}}
.bb-card {{border: 1px solid #D6DDE8; border-top: 5px solid {RED}; border-radius: 12px; padding: .8rem 1rem; background: #fff;}}
.bb-pool {{border: 1px solid #D6DDE8; border-radius: 12px; padding: .6rem .8rem; background: #F7F9FC; margin-bottom: .6rem;}}
.bb-pool b {{color: {NAVY};}}
.bb-pool div {{margin: .3rem 0;}}
.bb-cal-wrap {{overflow-x: auto;}}
.bb-cal {{border-collapse: separate; border-spacing: 6px; width: 100%;}}
.bb-cal th {{background: {NAVY}; color: #fff; padding: .4rem; border-radius: 8px; font-weight: 600;}}
.bb-cal th.bb-cal-time {{background: #EEF2F7; color: {NAVY}; white-space: nowrap; width: 80px;}}
.bb-cal td {{vertical-align: top; min-width: 170px;}}
.bb-ev {{border-radius: 10px; padding: .45rem .55rem; border: 1px solid rgba(4,30,66,.15); font-size: .86rem; margin-bottom: 4px;}}
.bb-ev div {{margin: .12rem 0;}}
.bb-ev-label {{font-weight: 700; color: {NAVY}; font-size: .74rem; letter-spacing: .04em; text-transform: uppercase;}}
.bb-ev-ref {{color: #3A4A63; font-size: .8rem;}}
.bb-tl {{display: flex; gap: .8rem; align-items: center; border: 1px solid #D6DDE8; border-radius: 12px;
  padding: .55rem .8rem; margin: .4rem 0; background: #fff;}}
.bb-tl-time {{width: 82px; font-weight: 700; color: {NAVY}; line-height: 1.2;}}
.bb-role {{font-size: .72rem; font-weight: 800; letter-spacing: .06em; padding: .2rem .55rem; border-radius: 999px; color: #fff;}}
.bb-role.play {{background: {RED};}}
.bb-role.ref {{background: {NAVY};}}
.bb-vs {{color: #8A94A6; margin: 0 .3rem;}}
.bb-list div {{margin: .3rem 0;}}
.bb-list-title {{font-weight: 700; color: {NAVY}; border-bottom: 2px solid {RED}; margin-bottom: .3rem;}}
.bb-table tr.zero td {{background: #FFF6DB;}}
</style>""", unsafe_allow_html=True)

MEDALS = {"Gold": "🥇", "Silver": "🥈", "Bronze": "🥉"}
# Same colors as the pools on the tournament sheet, plus the Sunday brackets.
GROUP_COLORS = {"A": "#D9EAD3", "B": "#F4CCCC", "C": "#C9DAF8", "D": "#FCE5CD", "E": "#D9D2E9", "F": "#FFF2CC",
                "Gold": "#FBE6A2", "Silver": "#E3E7ED", "Bronze": "#F2D2B6"}
UNASSIGNED = "— Unassigned —"


# ---------- Logos ----------

def badge_svg(team: str) -> str:
    """An original circle badge in the team's school colors, e.g. 'GU' with a small 'A'."""
    org_key, label = tm.TEAMS[team]
    org = tm.ORGS[org_key]
    abbr = org["abbr"]
    font = {1: 40, 2: 38, 3: 30}.get(len(abbr), 24)
    text_y = 52 if label else 62
    sub = (f'<text x="50" y="78" text-anchor="middle" font-family="Arial, sans-serif" font-weight="700" '
           f'font-size="17" fill="{org["fg"]}">{html.escape(label)}</text>') if label else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">'
            f'<circle cx="50" cy="50" r="45" fill="{org["bg"]}" stroke="{org["ring"]}" stroke-width="7"/>'
            f'<text x="50" y="{text_y}" text-anchor="middle" font-family="Arial Black, Arial, sans-serif" '
            f'font-weight="900" font-size="{font}" fill="{org["fg"]}">{html.escape(abbr)}</text>{sub}</svg>')


def logo_uri(team: str) -> str:
    """Use a real logo from logos/<ORG>.png if one has been added, otherwise the drawn badge."""
    custom = LOGO_DIR / f"{tm.TEAMS[team][0]}.png"
    if custom.exists():
        return "data:image/png;base64," + base64.b64encode(custom.read_bytes()).decode()
    return "data:image/svg+xml;base64," + base64.b64encode(badge_svg(team).encode()).decode()


def chip(team: str | None, size: int = 30) -> str:
    """HTML for a logo + team name. Handles empty bracket slots too."""
    if team is None:
        return '<span class="bb-tbd">TBD</span>'
    if team == tm.BYE:
        return '<span class="bb-tbd">BYE</span>'
    return (f'<span class="bb-chip"><img src="{logo_uri(team)}" width="{size}" height="{size}" alt="">'
            f'{html.escape(team)}</span>')


def show_html(markup: str) -> None:
    st.markdown(markup, unsafe_allow_html=True)


# ---------- Score entry (shared by pool play and brackets) ----------

def score_form(key: str, team1: str, team2: str, n_sets: int, current: list, on_save) -> None:
    """A small form: one row per set, two number boxes, Save and Clear buttons."""
    with st.form(key):
        head = st.columns([1, 2, 2])
        head[1].markdown(chip(team1, 34), unsafe_allow_html=True)
        head[2].markdown(chip(team2, 34), unsafe_allow_html=True)
        new_sets = []
        for i in range(n_sets):
            prev = current[i] if i < len(current) else [0, 0]
            row = st.columns([1, 2, 2])
            row[0].markdown(f"**Set {i + 1}**")
            # The saved value is part of the key, so the boxes refresh after Save or Clear.
            a = row[1].number_input(f"{team1} set {i + 1}", 0, 99, int(prev[0]), key=f"{key}_{i}a_{prev[0]}",
                                    label_visibility="collapsed")
            b = row[2].number_input(f"{team2} set {i + 1}", 0, 99, int(prev[1]), key=f"{key}_{i}b_{prev[1]}",
                                    label_visibility="collapsed")
            new_sets.append([int(a), int(b)])
        save_col, clear_col, _ = st.columns([1, 1, 3])
        saved = save_col.form_submit_button("💾 Save", type="primary")
        cleared = clear_col.form_submit_button("Clear")
    if saved:
        ties = [i + 1 for i, (a, b) in enumerate(new_sets) if a == b and a > 0]
        if ties:
            st.error(f"Set {ties[0]} is tied. A volleyball set can't end in a tie.")
        else:
            on_save(tm.played_sets(new_sets))
            st.rerun()
    if cleared:
        on_save([])
        st.rerun()


# ---------- Load data ----------

data = tm.load_data()
results = data["pool_results"]
events = tm.build_events(data)  # every game this weekend, shared by Overview, Calendar and Refs

show_html(f"""<div class="bb-hero"><div class="bb-kicker">GONZAGA MEN'S CLUB VOLLEYBALL</div>
<h1>🐾 Bulldog Bash 2026</h1>
<div class="bb-sub">Sat Nov 14 · Pool play &nbsp;|&nbsp; Sun Nov 15 · Gold, Silver &amp; Bronze brackets &nbsp;|&nbsp; Go Zags!</div></div>""")

tab_home, tab_cal, tab_pools, tab_bracket, tab_refs, tab_stats = st.tabs(
    ["🏠 Overview", "📅 Calendar", "🏐 Pool Play · Sat 11/14", "🏆 Sunday Bracket · 11/15", "🦓 Refs", "📊 Stats"])


# ---------- Overview ----------

with tab_home:
    done = sum(1 for m in tm.MATCHES if tm.played_sets(results.get(m["id"])))
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Teams", len(tm.TEAMS))
    c2.metric("Pools", len(tm.POOLS))
    c3.metric("Pool matches done", f"{done} / {len(tm.MATCHES)}")
    c4.metric("Courts", len({m["court"] for m in tm.MATCHES}))

    st.markdown("### 🐶 Zags spotlight")
    upcoming_events = [e for e in events if not e["done"]]

    def when(e):
        return f'{e["day"]} {tm.clock_label(e["start"])} · Court {e["court"]}'

    for team, col in zip(["GU A", "GU B"], st.columns(2)):
        pool = tm.pool_of(team)
        row = next(r for r in tm.pool_standings(pool, results) if r["Team"] == team)
        nxt = next((e for e in upcoming_events if team in e["teams"]), None)
        ref = next((e for e in upcoming_events if e["ref"] == team), None)
        opponent = next((t for t in nxt["teams"] if t != team), None) if nxt else None
        nxt_txt = f'{when(nxt)} vs {opponent or "TBD"}' if nxt else "Nothing scheduled"
        ref_txt = when(ref) if ref else "None scheduled"
        col.markdown(f"""<div class="bb-card">{chip(team, 46)}<br><br>
<b>Pool {pool}</b> · Place {row["Place"]} · Sets {row["Sets W"]}–{row["Sets L"]} · Diff {row["Diff"]:+d}<br>
<b>Next match:</b> {html.escape(nxt_txt)}<br><b>Next ref duty:</b> {html.escape(ref_txt)}</div>""",
                     unsafe_allow_html=True)

    st.markdown("### ⏱️ Up next")
    if upcoming_events:
        st.dataframe(pd.DataFrame([{"Day": e["day"], "Time": tm.clock_label(e["start"]), "Court": e["court"],
                                    "Game": e["label"],
                                    "Match": " vs ".join(t or "TBD" for t in e["teams"]),
                                    "Ref": e["ref"] or "needs ref"}
                                   for e in upcoming_events[:8]]), hide_index=True, width="stretch")
    else:
        st.success("Every scheduled game is finished. 🏆")

    st.markdown("### 🏐 The field")
    pool_cols = st.columns(3)
    for i, (pool, teams) in enumerate(tm.POOLS.items()):
        rows = "".join(f"<div>{chip(t, 28)}</div>" for t in teams)
        pool_cols[i % 3].markdown(f'<div class="bb-pool"><b>Pool {pool}</b> · {tm.SETS_PER_MATCH[pool]} sets to 25'
                                  f'{rows}</div>', unsafe_allow_html=True)


# ---------- Pool play ----------

def save_pool_result(match_id: str):
    def _save(sets):
        if sets:
            data["pool_results"][match_id] = sets
        else:
            data["pool_results"].pop(match_id, None)
        tm.save_data(data)
    return _save


with tab_pools:
    for pool, ptab in zip(tm.POOLS, st.tabs([f"Pool {p}" for p in tm.POOLS])):
        with ptab:
            left, right = st.columns([5, 6], gap="large")
            with left:
                st.markdown(f"#### Pool {pool} standings")
                body = "".join(
                    f'<tr class="{"lead" if r["Place"] == 1 and r["Played"] else ""}"><td>{r["Place"]}</td>'
                    f'<td>{chip(r["Team"], 28)}</td><td>{r["Played"]}</td><td>{r["Sets W"]}–{r["Sets L"]}</td>'
                    f'<td>{r["Pts For"]}–{r["Pts Against"]}</td><td>{r["Diff"]:+d}</td></tr>'
                    for r in tm.pool_standings(pool, results))
                show_html('<table class="bb-table"><tr><th>#</th><th>Team</th><th>MP</th><th>Sets</th>'
                          f'<th>Points</th><th>Diff</th></tr>{body}</table>')
                st.caption("Ranked by sets won, then point differential, then points scored.")
            with right:
                st.markdown(f"#### Matches · {tm.SETS_PER_MATCH[pool]} sets to 25")
                for m in [m for m in tm.MATCHES if m["pool"] == pool]:
                    sets = results.get(m["id"], [])
                    summary = tm.result_summary(m["team1"], m["team2"], sets)
                    icon = "✅" if summary else "⏳"
                    label = f'{icon} {m["time"]} · Ct {m["court"]} — {m["team1"]} vs {m["team2"]}'
                    with st.expander(label + (f"  ·  {summary}" if summary else "")):
                        st.caption(f'Ref: {m["ref"]}')
                        score_form(f'pool_{m["id"]}', m["team1"], m["team2"], m["sets"], sets,
                                   save_pool_result(m["id"]))


# ---------- Sunday brackets ----------

def bracket_html(rounds: list, champion: str | None, seed_of: dict, medal: str) -> str:
    cols = []
    for matches in rounds:
        cards = []
        for m in matches:
            w1, w2 = tm.sets_won(m["sets"])
            slots = []
            for team, won in zip(m["teams"], (w1, w2)):
                state = ""
                if m["winner"] and team not in (None, tm.BYE):
                    state = "win" if m["winner"] == team else "lose"
                seed = seed_of.get(team, "")
                score = won if m["sets"] else ""
                slots.append(f'<div class="bb-slot {state}"><span class="seed">{seed}</span>'
                             f'{chip(team, 26)}<span class="score">{score}</span></div>')
            cards.append(f'<div class="bb-match">{"".join(slots)}</div>')
        title = tm.round_name(len(matches) * 2)
        cols.append(f'<div class="bb-round"><div class="bb-round-title">{title}</div>{"".join(cards)}</div>')
    champ = (f'<div style="font-size:2.4rem">{medal}</div>{chip(champion, 56)}' if champion
             else '<div style="font-size:2.4rem">🏆</div><span class="bb-tbd">To be decided</span>')
    cols.append(f'<div class="bb-round"><div class="bb-round-title">Champion</div>'
                f'<div class="bb-champ">{champ}</div></div>')
    return f'<div class="bb-bracket">{"".join(cols)}</div>'


def save_bracket_result(bracket: dict, match: dict):
    def _save(sets):
        if sets:
            bracket["results"][match["id"]] = {"teams": match["teams"], "sets": sets}
        else:
            bracket["results"].pop(match["id"], None)
        tm.save_data(data)
    return _save


with tab_bracket:
    st.markdown("### Sunday, Nov 15 · Single elimination")
    st.caption("Seeds come from Saturday pool play: pool finish first, then set win %, then point "
               "differential per set. Gold takes the top seeds, then Silver, then Bronze. "
               "Bracket matches are best of 3.")
    sizes = {b: data["brackets"][b]["size"] for b in tm.BRACKETS}
    projected = tm.project_seeds(tm.overall_ranking(results), sizes)
    medals = MEDALS

    for name, btab in zip(tm.BRACKETS, st.tabs([f"{medals[b]} {b}" for b in tm.BRACKETS])):
        with btab:
            bracket = data["brackets"][name]
            locked = bracket["seeds"] is not None
            seeds = bracket["seeds"] if locked else projected[name]
            if not locked:
                st.info("**Projected bracket.** It updates live as pool scores come in. When pool play "
                        "is final, open **⚙️ Seeding** below and click **Lock in seeds** to start "
                        "entering Sunday scores.")
            rounds, champion = tm.resolve_bracket(seeds, bracket["results"])
            seed_of = {t: i + 1 for i, t in enumerate(seeds) if t != tm.BYE}
            show_html(bracket_html(rounds, champion, seed_of, medals[name]))

            if locked:
                st.markdown("#### Enter bracket scores")
                playable = 0
                for matches in rounds:
                    for m in matches:
                        a, b = m["teams"]
                        if a in (None, tm.BYE) or b in (None, tm.BYE):
                            continue
                        playable += 1
                        summary = tm.result_summary(a, b, m["sets"])
                        title = f'{"✅" if m["winner"] else "⏳"} {tm.round_name(len(matches) * 2)} — {a} vs {b}'
                        with st.expander(title + (f"  ·  {summary}" if summary else "")):
                            score_form(f'{name}_{m["id"]}_{a}_{b}', a, b, 3, m["sets"],
                                       save_bracket_result(bracket, m))
                if not playable:
                    st.caption("No matchups are ready yet.")

            with st.expander("⚙️ Seeding"):
                size = st.radio("Bracket size", [4, 8], index=[4, 8].index(bracket["size"]),
                                horizontal=True, key=f"size_{name}")
                if size != bracket["size"]:
                    bracket["size"] = size
                    if locked:
                        bracket["seeds"] = (bracket["seeds"] + [tm.BYE] * size)[:size]
                    tm.save_data(data)
                    st.rerun()
                options = [tm.BYE] + tm.ALL_TEAMS
                with st.form(f"seeds_{name}"):
                    st.caption("Change any seed by hand, then lock them in. Empty slots should be BYE.")
                    grid = st.columns(2)
                    new_seeds = []
                    for i, current in enumerate(seeds):
                        new_seeds.append(grid[i % 2].selectbox(
                            f"Seed {i + 1}", options, index=options.index(current), key=f"seed_{name}_{i}_{current}"))
                    lock = st.form_submit_button("🔒 Lock in seeds", type="primary")
                if lock:
                    real = [t for t in new_seeds if t != tm.BYE]
                    elsewhere = {t for b in tm.BRACKETS if b != name and data["brackets"][b]["seeds"]
                                 for t in data["brackets"][b]["seeds"] if t != tm.BYE}
                    dupes = sorted({t for t in real if real.count(t) > 1} | (set(real) & elsewhere))
                    if dupes:
                        st.error(f"These teams are seeded twice: {', '.join(dupes)}")
                    else:
                        bracket["seeds"] = new_seeds
                        tm.save_data(data)
                        st.rerun()
                if locked and st.button("↩️ Unlock and go back to projected seeds", key=f"unlock_{name}"):
                    bracket["seeds"] = None
                    tm.save_data(data)
                    st.rerun()


# ---------- Calendar ----------

def event_card(e: dict) -> str:
    a, b = e["teams"]
    ref = html.escape(e["ref"]) if e["ref"] else '<span class="bb-tbd">needs ref</span>'
    return (f'<div class="bb-ev" style="background:{GROUP_COLORS[e["group"]]}">'
            f'<div class="bb-ev-label">{e["label"]}{" ✅" if e["done"] else ""}</div>'
            f'<div>{chip(a, 22)}</div><div>{chip(b, 22)}</div><div class="bb-ev-ref">🦓 Ref: {ref}</div></div>')


def calendar_grid(day_events: list) -> str:
    """Times down the side, courts across the top."""
    courts = sorted({e["court"] for e in day_events})
    times = sorted({e["start"] for e in day_events})
    head = "".join(f"<th>Court {c}</th>" for c in courts)
    body = ""
    for t in times:
        cells = "".join("<td>" + "".join(event_card(e) for e in day_events
                                         if e["start"] == t and e["court"] == c) + "</td>" for c in courts)
        body += f'<tr><th class="bb-cal-time">{tm.clock_label(t)}</th>{cells}</tr>'
    return f'<div class="bb-cal-wrap"><table class="bb-cal"><tr><th></th>{head}</tr>{body}</table></div>'


def team_timeline(team: str, team_events: list) -> str:
    rows = []
    for e in team_events:
        role = "play" if team in e["teams"] else "ref"
        a, b = e["teams"]
        extra = f' · Ref: {html.escape(e["ref"] or "needs ref")}' if role == "play" else ""
        rows.append(f'<div class="bb-tl"><div class="bb-tl-time">{tm.clock_label(e["start"])}<br>'
                    f'<small>Court {e["court"]}</small></div><span class="bb-role {role}">{role.upper()}</span>'
                    f'<div>{chip(a, 24)}<span class="bb-vs">vs</span>{chip(b, 24)}<br>'
                    f'<small>{e["label"]}{extra}{" · ✅ final" if e["done"] else ""}</small></div></div>')
    return "".join(rows)


def court_clashes(day_events: list) -> list[str]:
    clashes = []
    for i, a in enumerate(day_events):
        for b in day_events[i + 1:]:
            if a["court"] == b["court"] and tm.overlaps(a, b):
                clashes.append(f'Court {a["court"]}: {a["label"]} ({tm.clock_label(a["start"])}) overlaps '
                               f'{b["label"]} ({tm.clock_label(b["start"])})')
    return clashes


def sunday_time_editor() -> None:
    seeds = tm.bracket_seeds(data)
    time_options = [None] + list(range(8 * 60, 18 * 60 + 1, 15))  # 8:00 AM to 6:00 PM, every 15 min
    st.caption("Give each Sunday game a start time and court. Team names fill in as the bracket plays out. "
               f"Games are blocked out for about {tm.BRACKET_MINUTES} minutes.")
    for b in tm.BRACKETS:
        rounds, _ = tm.resolve_bracket(seeds[b], data["brackets"][b]["results"])
        games = [(f"{b}:{m['id']}", tm.round_name(len(ms) * 2), m)
                 for ms in rounds for m in ms if tm.BYE not in m["teams"]]
        with st.form(f"sunday_times_{b}"):
            st.markdown(f"**{MEDALS[b]} {b}**")
            picks = {}
            for key, round_label, m in games:
                current = data["sunday_schedule"].get(key, {})
                start, court = current.get("start"), current.get("court", 1)
                c1, c2, c3 = st.columns([4, 2, 1])
                c1.markdown(f'{round_label}: {" vs ".join(t or "TBD" for t in m["teams"])}')
                new_start = c2.selectbox("Start", time_options, index=time_options.index(start) if start in time_options else 0,
                                         format_func=lambda x: "— not set —" if x is None else tm.clock_label(x),
                                         key=f"start_{key}_{start}", label_visibility="collapsed")
                new_court = c3.selectbox("Court", [1, 2, 3, 4, 5], index=court - 1, key=f"court_{key}_{court}",
                                         label_visibility="collapsed")
                picks[key] = (new_start, new_court)
            if st.form_submit_button(f"💾 Save {b} times"):
                for key, (new_start, new_court) in picks.items():
                    if new_start is None:
                        data["sunday_schedule"].pop(key, None)
                    else:
                        data["sunday_schedule"][key] = {"start": new_start, "court": new_court}
                tm.save_data(data)
                st.rerun()


with tab_cal:
    view = st.radio("Show", ["Whole tournament", "One team"], horizontal=True, key="cal_view")
    if view == "One team":
        team = st.selectbox("Team", tm.ALL_TEAMS, index=tm.ALL_TEAMS.index("GU A"), key="cal_team")
        mine = [e for e in events if team in e["teams"] or e["ref"] == team]
        for day, day_name in tm.DAYS.items():
            st.markdown(f"#### {day_name}")
            day_events = [e for e in mine if e["day"] == day]
            if day_events:
                show_html(team_timeline(team, day_events))
            else:
                st.caption("Nothing scheduled yet." + (" Sunday games show up once they have a time "
                                                       "(see 🗓️ Sunday game times)." if day == "Sun" else ""))
        st.download_button("📲 Add to my calendar (.ics)", tm.team_ics(team, events),
                           file_name=f"bulldog-bash-{team.lower().replace(' ', '-').replace(chr(39), '')}.ics",
                           mime="text/calendar")
        st.caption("Opens in Apple Calendar, Google Calendar or Outlook. Download again if times or refs change.")
    else:
        day = st.radio("Day", list(tm.DAYS), format_func=tm.DAYS.get, horizontal=True, key="cal_day")
        day_events = [e for e in events if e["day"] == day]
        for clash in court_clashes(day_events):
            st.warning(clash, icon="⚠️")
        if day_events:
            show_html(calendar_grid(day_events))
        else:
            st.info("No Sunday games have times yet. Set them in **🗓️ Sunday game times** below.")
    with st.expander("🗓️ Sunday game times"):
        sunday_time_editor()


# ---------- Refs ----------

def set_ref(event_key: str, sheet_ref: str | None, widget_key: str) -> None:
    """Runs when a ref dropdown changes. Saturday keeps the sheet's ref unless overridden."""
    choice = st.session_state[widget_key]
    saved = tm.load_data()
    if choice == UNASSIGNED:
        if sheet_ref:
            saved["refs"][event_key] = None      # remember that the sheet's ref was removed
        else:
            saved["refs"].pop(event_key, None)
    elif choice == sheet_ref:
        saved["refs"].pop(event_key, None)       # back to the original sheet assignment
    else:
        saved["refs"][event_key] = choice
    tm.save_data(saved)


with tab_refs:
    day = st.radio("Day", list(tm.DAYS), format_func=tm.DAYS.get, horizontal=True, key="ref_day")
    day_events = [e for e in events if e["day"] == day]
    counts = tm.ref_counts(events)
    board, side = st.columns([3, 2], gap="large")

    with side:
        st.markdown("### 👀 Who's off?")
        if not day_events:
            st.caption("No games scheduled for this day yet.")
        else:
            slot = st.selectbox("Pick a time", sorted({e["start"] for e in day_events}),
                                format_func=tm.clock_label, key=f"off_time_{day}")
            probe = {"key": "_probe", "day": day, "start": slot, "end": slot + 1}
            now = [e for e in day_events if tm.overlaps(e, probe)]
            playing = sorted({t for e in now for t in e["teams"] if t})
            reffing = sorted({e["ref"] for e in now if e["ref"]})
            off = sorted((t for t in tm.ALL_TEAMS if t not in playing and t not in reffing),
                         key=lambda t: (counts[t], t))
            c1, c2, c3 = st.columns(3)
            for col, title, teams in [(c1, "🏐 Playing", playing), (c2, "🦓 Reffing", reffing), (c3, "😴 Off", off)]:
                items = "".join(f"<div>{chip(t, 22)}" + (f" <small>({counts[t]})</small>" if col is c3 else "")
                                + "</div>" for t in teams) or '<div class="bb-tbd">nobody</div>'
                col.markdown(f'<div class="bb-list"><div class="bb-list-title">{title}</div>{items}</div>',
                             unsafe_allow_html=True)
            st.caption("Off teams are listed fewest ref duties first; the number is their weekend total.")

        st.markdown("### 📋 Ref duty count")
        sat, sun = tm.ref_counts(events, "Sat"), tm.ref_counts(events, "Sun")
        body = "".join(
            f'<tr class="{"zero" if not counts[t] else ""}"><td>{counts[t]}</td><td>{chip(t, 24)}</td>'
            f'<td>{sat[t]}</td><td>{sun[t]}</td></tr>'
            for t in sorted(tm.ALL_TEAMS, key=lambda t: (counts[t], t)))
        show_html(f'<table class="bb-table"><tr><th>Total</th><th>Team</th><th>Sat</th><th>Sun</th></tr>{body}</table>')
        st.caption("Highlighted teams haven't reffed yet.")

    with board:
        st.markdown("### 🦓 Ref board")
        if day == "Sat":
            st.caption("Saturday refs come from the tournament sheet. Change one if a team can't make it; "
                       "the list only shows teams that are off at that time. ⭐ = fewest ref duties so far.")
            if any(e["key"] in data["refs"] for e in day_events) and st.button("↩️ Reset Saturday to the sheet"):
                for e in day_events:
                    data["refs"].pop(e["key"], None)
                tm.save_data(data)
                st.rerun()
        else:
            st.caption("⭐ = a team that's off, has reffed the least, and is in the same bracket when possible.")
            if st.button("✨ Auto-assign Sunday refs", type="primary",
                         disabled=not any(not e["ref"] for e in day_events)):
                n = tm.auto_assign_refs(data, "Sun")
                tm.save_data(data)
                st.toast(f"Assigned {n} ref{'s' if n != 1 else ''}")
                st.rerun()
        if not day_events:
            st.info("No Sunday games have times yet. Set them in **📅 Calendar → 🗓️ Sunday game times**.")
        for e in day_events:
            current = e["ref"]
            ranked = tm.suggest_refs(e, events, tm.preferred_refs(e, data))
            best = ranked[0] if ranked else None
            options = [UNASSIGNED] + ([current] if current and current not in ranked else []) + ranked

            def label(t, current=current, best=best, sheet=e["sheet_ref"]):
                if t == UNASSIGNED:
                    return t
                n = counts[t] - (1 if t == current else 0)
                return (f'{"⭐ " if t == best else ""}{t} · {n} other ref{"s" if n != 1 else ""}'
                        f'{" (sheet)" if t == sheet else ""}')

            c1, c2, c3 = st.columns([2, 3, 4])
            c1.markdown(f'**{tm.clock_label(e["start"])}** · Ct {e["court"]}<br><small>{e["label"]}</small>',
                        unsafe_allow_html=True)
            c2.markdown(f'{chip(e["teams"][0], 22)}<br>{chip(e["teams"][1], 22)}', unsafe_allow_html=True)
            widget_key = f'ref_{e["key"]}_{current}'
            c3.selectbox("Ref", options, index=options.index(current) if current else 0, format_func=label,
                         key=widget_key, label_visibility="collapsed",
                         on_change=set_ref, args=(e["key"], e["sheet_ref"], widget_key))
            problem = tm.ref_problem(e, events)
            if problem:
                c3.warning(problem, icon="⚠️")
            elif not current:
                c3.caption(f"Needs a ref · suggested: {best}" if best else "Needs a ref · nobody is free then")
            st.divider()


# ---------- Stats ----------

with tab_stats:
    st.markdown("### 📊 Stats")
    st.caption("Type into the table like a spreadsheet. Add a row with ➕ at the bottom, pick the team, "
               "then click **Save stats**. Player is optional if you only track team totals.")
    columns = ["Team", "Player", "Opponent"] + tm.STAT_FIELDS
    if data["stats"]:
        df = pd.DataFrame(data["stats"], columns=columns)
    else:
        df = pd.DataFrame({c: pd.Series(dtype="str") for c in columns[:3]}
                          | {c: pd.Series(dtype="int") for c in tm.STAT_FIELDS})
    st.session_state.setdefault("stats_version", 0)
    edited = st.data_editor(
        df, num_rows="dynamic", hide_index=True, width="stretch",
        key=f"stats_editor_{st.session_state.stats_version}",
        column_config={
            "Team": st.column_config.SelectboxColumn("Team", options=tm.ALL_TEAMS, required=True),
            "Opponent": st.column_config.SelectboxColumn("Opponent", options=tm.ALL_TEAMS),
            **{f: st.column_config.NumberColumn(f, min_value=0, step=1, default=0) for f in tm.STAT_FIELDS},
        })
    if st.button("💾 Save stats", type="primary"):
        clean = edited.dropna(subset=["Team"]).copy()
        clean[tm.STAT_FIELDS] = clean[tm.STAT_FIELDS].fillna(0).astype(int)
        clean[["Player", "Opponent"]] = clean[["Player", "Opponent"]].fillna("")
        data["stats"] = clean.to_dict("records")
        tm.save_data(data)
        st.session_state.stats_version += 1
        st.rerun()

    if data["stats"]:
        stats = pd.DataFrame(data["stats"])
        st.markdown("#### Team totals")
        totals = stats.groupby("Team")[tm.STAT_FIELDS].sum().sort_values("Kills", ascending=False)
        st.dataframe(totals, width="stretch")
        players = stats[stats["Player"].astype(str).str.strip() != ""]
        if not players.empty:
            st.markdown("#### Player leaders")
            by_player = players.groupby(["Player", "Team"])[tm.STAT_FIELDS].sum().reset_index()
            for field, col in zip(["Kills", "Aces", "Blocks", "Digs"], st.columns(4)):
                col.markdown(f"**{field}**")
                col.dataframe(by_player.nlargest(5, field)[["Player", "Team", field]],
                              hide_index=True, width="stretch")
