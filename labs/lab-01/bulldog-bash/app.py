"""Bulldog Bash tracker: a Streamlit app for Gonzaga Club Volleyball's tournament (men's and women's).

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


# ---------- Storage ----------
# With SUPABASE_URL and SUPABASE_KEY in Streamlit secrets, every device shares one copy of the scores.
# Without them (e.g. on a laptop with no secrets.toml), the app falls back to data.json.

@st.cache_resource
def supabase_client(url: str, key: str):
    from supabase import create_client
    return create_client(url, key)


try:
    _url, _key = st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"]
except Exception:  # no secrets file, or the keys aren't in it
    _url = _key = None
if _url and _key:
    tm.use_supabase(supabase_client(_url, _key))

st.markdown(f"""<style>
.bb-hero {{background: linear-gradient(135deg, {NAVY} 0%, #0B2D5C 100%); color: #fff; padding: 1.3rem 1.6rem;
  border-radius: 14px; border-bottom: 6px solid {RED}; margin-bottom: 1rem;}}
.bb-hero h1 {{color: #fff; margin: .1rem 0 .2rem; padding: 0; font-size: 2.2rem;}}
.bb-kicker {{letter-spacing: .14em; font-size: .78rem; font-weight: 700; color: #C9D3E3;}}
.bb-sub {{color: #DCE3EE;}}
.bb-chip {{display: inline-flex; align-items: center; gap: .45rem; vertical-align: middle;}}
.bb-chip img {{flex: none; object-fit: contain;}}
.bb-hero-logo {{height: 1.15em; width: auto; vertical-align: -.15em; margin-right: .2em;}}
.bb-icon {{height: 1.2em; width: auto; vertical-align: -.25em;}}
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
/* Score forms: keep each set on one line on phones (Streamlit normally stacks columns under 640px). */
[data-testid="stForm"] [data-testid="stHorizontalBlock"] {{flex-wrap: nowrap !important; gap: .5rem;}}
[data-testid="stForm"] [data-testid="stColumn"] {{min-width: 0 !important; width: auto !important;}}
[data-testid="stForm"] [data-testid="stColumn"]:first-child {{flex: 1 1 0 !important;}}
[data-testid="stForm"] [data-testid="stColumn"]:not(:first-child) {{flex: 2 1 0 !important;}}
[data-testid="stForm"] [data-testid="stHorizontalBlock"]:last-child [data-testid="stColumn"] {{flex: 1 1 0 !important;}}
[data-testid="stForm"] input[type="number"] {{font-size: 16px;}}  /* 16px stops iPhones zooming in on tap */
@media (max-width: 640px) {{
  .bb-hero {{padding: 1rem;}}
  .bb-hero h1 {{font-size: 1.6rem;}}
  [data-testid="stForm"] .bb-chip {{flex-direction: column; align-items: flex-start; gap: .15rem;
    font-size: .9rem; line-height: 1.2; word-break: normal; overflow-wrap: normal;}}
  [data-testid="stForm"] button[data-testid="stNumberInputStepDown"],
  [data-testid="stForm"] button[data-testid="stNumberInputStepUp"] {{display: none;}}
}}
</style>""", unsafe_allow_html=True)

MEDALS = {"Gold": "🥇", "Silver": "🥈", "Bronze": "🥉"}
# Same colors as the pools on the tournament sheet, plus the Sunday brackets.
GROUP_COLORS = {"A": "#D9EAD3", "B": "#F4CCCC", "C": "#C9DAF8", "D": "#FCE5CD", "E": "#D9D2E9", "F": "#FFF2CC",
                "Gold": "#FBE6A2", "Silver": "#E3E7ED", "Bronze": "#F2D2B6"}
UNASSIGNED = "— Unassigned —"


# ---------- Logos ----------

def badge_svg(team: str) -> str:
    """An original circle badge in the team's school colors, e.g. 'GU' with a small 'A'."""
    org_key, label = div.teams[team]
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


def image_uri(path: Path) -> str:
    """A PNG file turned into text the browser can show inline (a 'data URI')."""
    return "data:image/png;base64," + base64.b64encode(path.read_bytes()).decode()


def logo_uri(team: str) -> str:
    """Use a real logo from logos/<ORG>.png if one has been added, otherwise the drawn badge."""
    custom = LOGO_DIR / f"{div.teams[team][0]}.png"
    if custom.exists():
        return image_uri(custom)
    return "data:image/svg+xml;base64," + base64.b64encode(badge_svg(team).encode()).decode()


REF_ICON = f'<img class="bb-icon" src="{image_uri(LOGO_DIR / "ref-shirt.png")}" alt="Ref">'


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
    """A small form: one row per set, two number boxes, Save and Clear buttons.

    2-set pool matches also get an optional Set 3 row; left at 0-0 it doesn't count.
    """
    rows = max(n_sets, 3)
    with st.form(key):
        head = st.columns([1, 2, 2], vertical_alignment="center")
        head[1].markdown(chip(team1, 28), unsafe_allow_html=True)
        head[2].markdown(chip(team2, 28), unsafe_allow_html=True)
        new_sets = []
        for i in range(rows):
            prev = current[i] if i < len(current) else [0, 0]
            row = st.columns([1, 2, 2], vertical_alignment="center")
            optional = i >= n_sets
            row[0].markdown(f"**Set {i + 1}**" + ('<br><small>if played</small>' if optional else ""),
                            unsafe_allow_html=True)
            # The saved value is part of the key, so the boxes refresh after Save or Clear.
            a = row[1].number_input(f"{team1} set {i + 1}", 0, 99, int(prev[0]), key=f"{key}_{i}a_{prev[0]}",
                                    label_visibility="collapsed")
            b = row[2].number_input(f"{team2} set {i + 1}", 0, 99, int(prev[1]), key=f"{key}_{i}b_{prev[1]}",
                                    label_visibility="collapsed")
            new_sets.append([int(a), int(b)])
        save_col, clear_col, _ = st.columns([1, 1, 1])
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

# ---------- Division toggle (upper left) ----------
# Each viewer picks a side. The choice lives in their own session (so it never changes anyone
# else's screen) and in the page link, e.g. ?division=women, so a bookmark opens the right side.

def keep_division() -> None:
    """Clicking the already-selected option would clear it; put the last choice back."""
    if st.session_state.division is None:
        st.session_state.division = st.session_state.get("last_division", "men")


if "division" not in st.session_state:
    wanted = st.query_params.get("division", "men")
    st.session_state.division = wanted if wanted in tm.DIVISIONS else "men"
toggle_col, _ = st.columns([1, 3])
toggle_col.segmented_control("Division", list(tm.DIVISIONS), format_func=lambda k: tm.DIVISIONS[k].name,
                             key="division", on_change=keep_division, label_visibility="collapsed")
div = tm.DIVISIONS[st.session_state.division or st.session_state.get("last_division", "men")]
st.session_state.last_division = div.key
st.query_params["division"] = div.key

data = tm.load_data(div)
results = data["pool_results"]
events = tm.build_events(div, data)  # every game this weekend, shared by Overview, Calendar and Refs

active = tm.active_brackets(data)
bracket_words = (active[0] if len(active) == 1 else ", ".join(active[:-1]) + " &amp; " + active[-1]) + \
    (" bracket" if len(active) == 1 else " brackets")
show_html(f"""<div class="bb-hero"><div class="bb-kicker">GONZAGA {div.name.upper()} CLUB VOLLEYBALL</div>
<h1><img class="bb-hero-logo" src="{image_uri(LOGO_DIR / "GU.png")}" alt="Gonzaga"> Bulldog Bash 2026</h1>
<div class="bb-sub">Sat Nov 14 · Pool play &nbsp;|&nbsp; Sun Nov 15 · {bracket_words} &nbsp;|&nbsp; Go Zags!</div></div>""")

# Tab labels can only be text, so CSS draws the ref shirt in front of the 5th top-level tab ("Refs").
# ":not(stTabPanel *)" skips the tab rows nested inside a tab (like Pool A-F), where Pool E is also 5th.
show_html(f"""<style>
[data-testid="stTab"]:nth-of-type(5):not([data-testid="stTabPanel"] *) p::before {{
  content: ""; display: inline-block; width: 1.25em; height: 1.25em; margin-right: .35em;
  vertical-align: -.25em; background: url("{image_uri(LOGO_DIR / "ref-shirt.png")}") center / contain no-repeat;}}
</style>""")

tab_home, tab_cal, tab_pools, tab_bracket, tab_refs, tab_stats = st.tabs(
    ["🏠 Overview", "📅 Calendar", "🏐 Pool Play · Sat 11/14", "🏆 Sunday Bracket · 11/15", "Refs", "📊 Stats"])


# ---------- Overview ----------

with tab_home:
    done = sum(1 for m in div.matches if tm.played_sets(results.get(m["id"])))
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Teams", len(div.teams))
    c2.metric("Pools", len(div.pools))
    c3.metric("Pool matches done", f"{done} / {len(div.matches)}")
    c4.metric("Courts", len({m["court"] for m in div.matches}))

    upcoming_events = [e for e in events if not e["done"]]
    st.caption(f"Scores are saved to: **{tm.storage_name(div)}**")

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
    for i, (pool, teams) in enumerate(div.pools.items()):
        rows = "".join(f"<div>{chip(t, 28)}</div>" for t in teams)
        pool_cols[i % 3].markdown(f'<div class="bb-pool"><b>Pool {pool}</b> · {div.sets_per_match[pool]} sets to 25'
                                  f'{rows}</div>', unsafe_allow_html=True)


# ---------- Pool play ----------

def save_pool_result(match_id: str):
    def _save(sets):
        if sets:
            data["pool_results"][match_id] = sets
        else:
            data["pool_results"].pop(match_id, None)
        tm.save_data(div, data)
    return _save


with tab_pools:
    for pool, ptab in zip(div.pools, st.tabs([f"Pool {p}" for p in div.pools])):
        with ptab:
            left, right = st.columns([5, 6], gap="large")
            with left:
                st.markdown(f"#### Pool {pool} standings")
                body = "".join(
                    f'<tr class="{"lead" if r["Place"] == 1 and r["Played"] else ""}"><td>{r["Place"]}</td>'
                    f'<td>{chip(r["Team"], 28)}</td><td>{r["Played"]}</td><td>{r["Sets W"]}–{r["Sets L"]}</td>'
                    f'<td>{r["Pts For"]}–{r["Pts Against"]}</td><td>{r["Diff"]:+d}</td></tr>'
                    for r in tm.pool_standings(div, pool, results))
                show_html('<table class="bb-table"><tr><th>#</th><th>Team</th><th>MP</th><th>Sets</th>'
                          f'<th>Points</th><th>Diff</th></tr>{body}</table>')
                st.caption("Ranked by sets won, then point differential, then points scored.")
            with right:
                st.markdown(f"#### Matches · {div.sets_per_match[pool]} sets to 25")
                for m in [m for m in div.matches if m["pool"] == pool]:
                    sets = results.get(m["id"], [])
                    summary = tm.result_summary(m["team1"], m["team2"], sets)
                    icon = "✅" if summary else "⏳"
                    label = f'{icon} {m["time"]} · Ct {m["court"]} — {m["team1"]} vs {m["team2"]}'
                    with st.expander(label + (f"  ·  {summary}" if summary else "")):
                        st.caption(f'Ref: {m["ref"]}')
                        score_form(f'{div.key}_pool_{m["id"]}', m["team1"], m["team2"], m["sets"], sets,
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
        tm.save_data(div, data)
    return _save


with tab_bracket:
    st.markdown("### Sunday, Nov 15 · Single elimination")
    st.caption("Seeds come from Saturday pool play: pool finish first, then set win %, then point "
               "differential per set. Gold takes the top seeds, then Silver, then Bronze. "
               "Bracket matches are best of 3.")
    medals = MEDALS

    with st.expander(f"🛠️ Bracket setup · {div.name}"):
        count_labels = {1: "1 (Gold)", 2: "2 (Gold, Silver)", 3: "3 (Gold, Silver, Bronze)"}
        count = st.radio("Number of brackets", [1, 2, 3], index=data["bracket_count"] - 1, horizontal=True,
                         format_func=count_labels.get, key=f'{div.key}_bracket_count_{data["bracket_count"]}')
        if count != data["bracket_count"]:
            data["bracket_count"] = count
            tm.save_data(div, data)
            st.rerun()
        with st.form(f"{div.key}_bracket_sizes"):
            st.caption("Teams in each bracket, filled from the top of the rankings (Gold first). Uneven numbers "
                       "are fine: the top seeds get BYEs, e.g. 6 teams → seeds 1 and 2 skip the first round.")
            size_cols = st.columns(len(tm.active_brackets(data)))
            new_sizes = {}
            for col, b in zip(size_cols, tm.active_brackets(data)):
                is_locked = data["brackets"][b]["seeds"] is not None
                new_sizes[b] = col.number_input(
                    f"{medals[b]} {b} teams", 2, 16, data["brackets"][b]["size"], disabled=is_locked,
                    key=f'{div.key}_teams_{b}_{data["brackets"][b]["size"]}',
                    help="Unlock this bracket's seeds to change its size." if is_locked else None)
            if st.form_submit_button("💾 Save bracket sizes"):
                for b, n in new_sizes.items():
                    data["brackets"][b]["size"] = int(n)
                tm.save_data(div, data)
                st.rerun()
        placed = sum(data["brackets"][b]["size"] for b in tm.active_brackets(data))
        total = len(div.all_teams)
        if placed < total:
            st.warning(f"{div.name} has {total} teams but the brackets hold {placed}: "
                       f"the {total - placed} lowest-ranked team{'s' if total - placed != 1 else ''} won't play Sunday.")
        elif placed > total:
            st.warning(f"The brackets hold {placed} teams but {div.name} only has {total}: "
                       f"the last bracket will have {placed - total} empty spot{'s' if placed - total != 1 else ''}.")
        else:
            st.success(f"All {total} {div.name.lower()} teams have a spot in a Sunday bracket.")

    sizes = {b: data["brackets"][b]["size"] for b in tm.active_brackets(data)}
    projected = tm.projected_seeds(div, results, sizes)

    for name, btab in zip(sizes, st.tabs([f"{medals[b]} {b}" for b in sizes])):
        with btab:
            bracket = data["brackets"][name]
            locked = bracket["seeds"] is not None
            seeds = bracket["seeds"] if locked else projected[name]
            if not locked:
                st.info("**Projected bracket.** Teams show as TBD until every match in their pool has a "
                        "score. Seeds can still shift until all pools are finished. When pool play is "
                        "final, open **⚙️ Seeding** below and click **Lock in seeds** to start entering "
                        "Sunday scores.")
            rounds, champion = tm.resolve_bracket(seeds, bracket["results"])
            seed_of = {t: i + 1 for i, t in enumerate(seeds) if t not in (None, tm.BYE)}
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
                            score_form(f'{div.key}_{name}_{m["id"]}_{a}_{b}', a, b, 3, m["sets"],
                                       save_bracket_result(bracket, m))
                if not playable:
                    st.caption("No matchups are ready yet.")

            with st.expander("⚙️ Seeding"):
                options = [None, tm.BYE] + div.all_teams  # None = TBD (its pool isn't finished yet)
                with st.form(f"{div.key}_seeds_{name}"):
                    st.caption("Change any seed by hand, then lock them in. Empty slots should be BYE.")
                    grid = st.columns(2)
                    new_seeds = []
                    for i, current in enumerate(seeds):
                        new_seeds.append(grid[i % 2].selectbox(
                            f"Seed {i + 1}", options, index=options.index(current), key=f"{div.key}_seed_{name}_{i}_{current}",
                            format_func=lambda t: "TBD" if t is None else t))
                    lock = st.form_submit_button("🔒 Lock in seeds", type="primary")
                if lock and None in new_seeds:
                    st.error("Some seeds are still TBD. Pick a team or BYE for every seed before locking.")
                elif lock:
                    real = [t for t in new_seeds if t != tm.BYE]
                    elsewhere = {t for b in tm.active_brackets(data) if b != name and data["brackets"][b]["seeds"]
                                 for t in data["brackets"][b]["seeds"] if t != tm.BYE}
                    dupes = sorted({t for t in real if real.count(t) > 1} | (set(real) & elsewhere))
                    if dupes:
                        st.error(f"These teams are seeded twice: {', '.join(dupes)}")
                    else:
                        bracket["seeds"] = new_seeds
                        tm.save_data(div, data)
                        st.rerun()
                if locked and st.button("↩️ Unlock and go back to projected seeds", key=f"{div.key}_unlock_{name}"):
                    bracket["seeds"] = None
                    tm.save_data(div, data)
                    st.rerun()


# ---------- Calendar ----------

def event_card(e: dict) -> str:
    a, b = e["teams"]
    ref = html.escape(e["ref"]) if e["ref"] else '<span class="bb-tbd">needs ref</span>'
    return (f'<div class="bb-ev" style="background:{GROUP_COLORS[e["group"]]}">'
            f'<div class="bb-ev-label">{e["label"]}{" ✅" if e["done"] else ""}</div>'
            f'<div>{chip(a, 22)}</div><div>{chip(b, 22)}</div><div class="bb-ev-ref">{REF_ICON} Ref: {ref}</div></div>')


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
    seeds = tm.bracket_seeds(div, data)
    time_options = [None] + list(range(8 * 60, 18 * 60 + 1, 15))  # 8:00 AM to 6:00 PM, every 15 min
    st.caption("Give each Sunday game a start time and court. Team names fill in as the bracket plays out. "
               f"Games are blocked out for about {tm.BRACKET_MINUTES} minutes.")
    for b in tm.active_brackets(data):
        rounds, _ = tm.resolve_bracket(seeds[b], data["brackets"][b]["results"])
        games = [(f"{b}:{m['id']}", tm.round_name(len(ms) * 2), m)
                 for ms in rounds for m in ms if tm.BYE not in m["teams"]]
        with st.form(f"{div.key}_sunday_times_{b}"):
            st.markdown(f"**{MEDALS[b]} {b}**")
            picks = {}
            for key, round_label, m in games:
                current = data["sunday_schedule"].get(key, {})
                start, court = current.get("start"), current.get("court", div.courts[0])
                c1, c2, c3 = st.columns([4, 2, 1])
                c1.markdown(f'{round_label}: {" vs ".join(t or "TBD" for t in m["teams"])}')
                new_start = c2.selectbox("Start", time_options, index=time_options.index(start) if start in time_options else 0,
                                         format_func=lambda x: "— not set —" if x is None else tm.clock_label(x),
                                         key=f"{div.key}_start_{key}_{start}", label_visibility="collapsed")
                new_court = c3.selectbox("Court", tm.ALL_COURTS, index=tm.ALL_COURTS.index(court) if court in tm.ALL_COURTS else 0,
                                         key=f"{div.key}_court_{key}_{court}",
                                         label_visibility="collapsed")
                picks[key] = (new_start, new_court)
            if st.form_submit_button(f"💾 Save {b} times"):
                for key, (new_start, new_court) in picks.items():
                    if new_start is None:
                        data["sunday_schedule"].pop(key, None)
                    else:
                        data["sunday_schedule"][key] = {"start": new_start, "court": new_court}
                tm.save_data(div, data)
                st.rerun()


with tab_cal:
    view = st.radio("Show", ["Whole tournament", "One team"], horizontal=True, key="cal_view")
    if view == "One team":
        team = st.selectbox("Team", div.all_teams, index=div.all_teams.index("GU A"), key=f"{div.key}_cal_team")
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

def set_ref(div_key: str, event_key: str, sheet_ref: str | None, widget_key: str) -> None:
    """Runs when a ref dropdown changes. Saturday keeps the sheet's ref unless overridden."""
    choice = st.session_state[widget_key]
    div = tm.DIVISIONS[div_key]
    saved = tm.load_data(div)
    if choice == UNASSIGNED:
        if sheet_ref:
            saved["refs"][event_key] = None      # remember that the sheet's ref was removed
        else:
            saved["refs"].pop(event_key, None)
    elif choice == sheet_ref:
        saved["refs"].pop(event_key, None)       # back to the original sheet assignment
    else:
        saved["refs"][event_key] = choice
    tm.save_data(div, saved)


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
                                format_func=tm.clock_label, key=f"{div.key}_off_time_{day}")
            probe = {"key": "_probe", "day": day, "start": slot, "end": slot + 1}
            now = [e for e in day_events if tm.overlaps(e, probe)]
            playing = sorted({t for e in now for t in e["teams"] if t})
            reffing = sorted({e["ref"] for e in now if e["ref"]})
            off = sorted((t for t in div.all_teams if t not in playing and t not in reffing),
                         key=lambda t: (counts[t], t))
            c1, c2, c3 = st.columns(3)
            for col, title, teams in [(c1, "🏐 Playing", playing), (c2, f"{REF_ICON} Reffing", reffing), (c3, "😴 Off", off)]:
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
            for t in sorted(div.all_teams, key=lambda t: (counts[t], t)))
        show_html(f'<table class="bb-table"><tr><th>Total</th><th>Team</th><th>Sat</th><th>Sun</th></tr>{body}</table>')
        st.caption("Highlighted teams haven't reffed yet.")

    with board:
        st.markdown(f"### {REF_ICON} Ref board", unsafe_allow_html=True)
        if day == "Sat":
            st.caption("Saturday refs come from the tournament sheet. Change one if a team can't make it; "
                       "the list only shows teams that are off at that time. ⭐ = fewest ref duties so far.")
            if any(e["key"] in data["refs"] for e in day_events) and st.button("↩️ Reset Saturday to the sheet"):
                for e in day_events:
                    data["refs"].pop(e["key"], None)
                tm.save_data(div, data)
                st.rerun()
        else:
            st.caption("⭐ = a team that's off, has reffed the least, and is in the same bracket when possible.")
            if st.button("✨ Auto-assign Sunday refs", type="primary",
                         disabled=not any(not e["ref"] for e in day_events)):
                n = tm.auto_assign_refs(div, data, "Sun")
                tm.save_data(div, data)
                st.toast(f"Assigned {n} ref{'s' if n != 1 else ''}")
                st.rerun()
        if not day_events:
            st.info("No Sunday games have times yet. Set them in **📅 Calendar → 🗓️ Sunday game times**.")
        for e in day_events:
            current = e["ref"]
            ranked = tm.suggest_refs(div, e, events, tm.preferred_refs(div, e, data))
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
            widget_key = f'{div.key}_ref_{e["key"]}_{current}'
            c3.selectbox("Ref", options, index=options.index(current) if current else 0, format_func=label,
                         key=widget_key, label_visibility="collapsed",
                         on_change=set_ref, args=(div.key, e["key"], e["sheet_ref"], widget_key))
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
        key=f"{div.key}_stats_editor_{st.session_state.stats_version}",
        column_config={
            "Team": st.column_config.SelectboxColumn("Team", options=div.all_teams, required=True),
            "Opponent": st.column_config.SelectboxColumn("Opponent", options=div.all_teams),
            **{f: st.column_config.NumberColumn(f, min_value=0, step=1, default=0) for f in tm.STAT_FIELDS},
        })
    if st.button("💾 Save stats", type="primary"):
        clean = edited.dropna(subset=["Team"]).copy()
        clean[tm.STAT_FIELDS] = clean[tm.STAT_FIELDS].fillna(0).astype(int)
        clean[["Player", "Opponent"]] = clean[["Player", "Opponent"]].fillna("")
        data["stats"] = clean.to_dict("records")
        tm.save_data(div, data)
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
