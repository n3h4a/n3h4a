"""Build assets for the profile README: a "wrapped"-style card of the last 12 months on GitHub.

Reads public data through the GitHub GraphQL API and writes an SVG.
Usage: GITHUB_TOKEN=... python3 scripts/wrapped.py <login> <out.svg>
       python3 scripts/wrapped.py --from-json <response.json> <out.svg>   (offline preview)
"""

import datetime as dt
import json
import os
import sys
import urllib.request
from collections import defaultdict
from xml.sax.saxutils import escape

QUERY = """
query($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    login
    repositories(ownerAffiliations: OWNER, isFork: false, privacy: PUBLIC, first: 100) {
      totalCount
      nodes {
        name
        stargazerCount
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
          edges { size node { name color } }
        }
      }
    }
    contributionsCollection(from: $from, to: $to) {
      commitContributionsByRepository(maxRepositories: 10) {
        repository { name isPrivate }
        contributions { totalCount }
      }
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount weekday } }
      }
    }
  }
}
"""

# Markup, notebooks and build glue would drown out the code itself.
SKIP_LANGS = {"HTML", "CSS", "SCSS", "Jupyter Notebook", "Makefile", "Dockerfile",
              "Batchfile", "PowerShell", "Procfile", "Shell", "TeX"}
RENAME_LANGS = {"TSQL": "SQL", "PLpgSQL": "SQL", "PLSQL": "SQL"}
FALLBACK_COLORS = ["#ff8fab", "#a59cff", "#7ee8c7", "#ffd479", "#8fd3ff"]
WEEKDAYS = ["Sundays", "Mondays", "Tuesdays", "Wednesdays", "Thursdays", "Fridays", "Saturdays"]


def fetch(login: str, token: str) -> dict:
    now = dt.datetime.now(dt.timezone.utc)
    variables = {"login": login,
                 "from": (now - dt.timedelta(days=364)).strftime("%Y-%m-%dT00:00:00Z"),
                 "to": now.strftime("%Y-%m-%dT%H:%M:%SZ")}
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": variables}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json",
                 "User-Agent": "profile-wrapped"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        body = json.load(resp)
    if body.get("errors"):
        raise SystemExit(f"GraphQL errors: {body['errors']}")
    return body


def summarise(body: dict) -> dict:
    user = body["data"]["user"]
    cc = user["contributionsCollection"]
    days = [d for w in cc["contributionCalendar"]["weeks"] for d in w["contributionDays"]]
    days.sort(key=lambda d: d["date"])

    longest = run = 0
    for d in days:
        run = run + 1 if d["contributionCount"] > 0 else 0
        longest = max(longest, run)
    current = 0
    tail = days[:-1] if days and days[-1]["contributionCount"] == 0 else days  # today isn't over yet
    for d in reversed(tail):
        if d["contributionCount"] == 0:
            break
        current += 1

    by_weekday = defaultdict(int)
    for d in days:
        by_weekday[d["weekday"]] += d["contributionCount"]
    busiest = WEEKDAYS[max(by_weekday, key=by_weekday.get)] if any(by_weekday.values()) else "—"
    active_days = sum(1 for d in days if d["contributionCount"] > 0)

    lang_bytes = defaultdict(int)
    for repo in user["repositories"]["nodes"]:
        for e in repo["languages"]["edges"]:
            name = RENAME_LANGS.get(e["node"]["name"], e["node"]["name"])
            if name in SKIP_LANGS:
                continue
            lang_bytes[name] += e["size"]
    total = sum(lang_bytes.values()) or 1
    langs = sorted(lang_bytes.items(), key=lambda kv: -kv[1])[:5]
    langs = [(n, b / total * 100, FALLBACK_COLORS[i % 5]) for i, (n, b) in enumerate(langs)]

    repos = [(r["repository"]["name"], r["contributions"]["totalCount"])
             for r in cc["commitContributionsByRepository"]
             if not r["repository"]["isPrivate"] and r["repository"]["name"] != user["login"]]
    repos.sort(key=lambda kv: -kv[1])

    return {
        "total": cc["contributionCalendar"]["totalContributions"],
        "longest": longest, "current": current, "busiest": busiest, "active_days": active_days,
        "langs": langs, "repos": repos[:3],
        "stars": sum(r["stargazerCount"] for r in user["repositories"]["nodes"]),
        "public_repos": user["repositories"]["totalCount"],
    }


def render(s: dict) -> str:
    sans = '-apple-system, BlinkMacSystemFont, &quot;Segoe UI&quot;, Helvetica, Arial, sans-serif'
    mono = 'ui-monospace, SFMono-Regular, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace'
    out = []
    a = out.append

    a(f'''<svg xmlns="http://www.w3.org/2000/svg" width="840" height="490" viewBox="0 0 840 490" role="img" aria-labelledby="t d">
  <title id="t">n3h4a, wrapped: the last 12 months on GitHub</title>
  <desc id="d">{s["total"]:,} contributions, longest streak {s["longest"]} days, busiest on {s["busiest"]}. Top languages: {escape(", ".join(n for n, _, _ in s["langs"]))}.</desc>
  <style>
    .sans {{ font-family: {sans}; }}
    .mono {{ font-family: {mono}; }}
    .cap  {{ font-size: 11px; font-weight: 800; letter-spacing: 2px; fill: #b9b0d9; }}
    .big  {{ font-weight: 900; fill: #ffffff; }}
    .lbl  {{ font-size: 12.5px; fill: #cfc8e6; }}
  </style>
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#2a1640"/><stop offset="0.55" stop-color="#17142a"/><stop offset="1" stop-color="#0f1f24"/>
    </linearGradient>
    <filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="40"/></filter>
    <clipPath id="card"><rect x="0" y="0" width="840" height="490" rx="18"/></clipPath>
  </defs>
  <g clip-path="url(#card)">
    <rect width="840" height="490" fill="url(#bg)"/>
    <circle cx="90" cy="70" r="110" fill="#ff8fab" opacity="0.35" filter="url(#blur)">
      <animate attributeName="cx" values="90;140;90" dur="12s" repeatCount="indefinite"/>
    </circle>
    <circle cx="760" cy="420" r="130" fill="#7ee8c7" opacity="0.22" filter="url(#blur)">
      <animate attributeName="cy" values="420;370;420" dur="14s" repeatCount="indefinite"/>
    </circle>
    <circle cx="560" cy="60" r="90" fill="#a59cff" opacity="0.25" filter="url(#blur)"/>
  </g>
  <rect x="1" y="1" width="838" height="488" rx="18" fill="none" stroke="#2a2540" stroke-width="2"/>

  <g class="sans">
    <text x="32" y="46" class="cap" fill="#ff8fab" style="fill:#ff8fab">N3H4A · WRAPPED</text>
    <text x="32" y="66" class="lbl" style="fill:#8b84a8">the last 12 months on GitHub</text>
''')
    # equalizer
    bars = [(0, "14;5;11;7;14", "0.9s"), (7, "6;14;8;12;6", "0.8s"), (14, "10;6;14;4;10", "1s"), (21, "4;11;6;14;4", "1.1s")]
    for dx, vals, dur in bars:
        ys = ";".join(str(60 - int(v)) for v in vals.split(";"))
        a(f'    <rect x="{780 + dx}" y="46" width="4" height="14" rx="1.5" fill="#7ee8c7">'
          f'<animate attributeName="height" values="{vals}" dur="{dur}" repeatCount="indefinite"/>'
          f'<animate attributeName="y" values="{ys}" dur="{dur}" repeatCount="indefinite"/></rect>\n')

    # headline number
    a(f'''
    <text x="32" y="150" class="big" font-size="76" letter-spacing="-2">{s["total"]:,}</text>
    <text x="34" y="178" class="lbl" font-size="14">contributions · {s["active_days"]} days with at least one</text>
''')
    # mini stats
    tiles = [("LONGEST RUN", f'{s["longest"]} days'), ("CURRENT RUN", f'{s["current"]} days'),
             ("BUSIEST ON", s["busiest"])]
    for i, (cap, val) in enumerate(tiles):
        x = 32 + i * 130
        a(f'    <rect x="{x}" y="204" width="122" height="62" rx="12" fill="#ffffff" fill-opacity="0.06" stroke="#ffffff" stroke-opacity="0.08"/>\n')
        a(f'    <text x="{x + 14}" y="226" class="cap" font-size="9" style="letter-spacing:1px">{cap}</text>\n')
        a(f'    <text x="{x + 14}" y="252" class="big" font-size="19">{escape(val)}</text>\n')

    # top genres
    a('    <text x="460" y="104" class="cap">TOP GENRES</text>\n')
    for i, (name, pct, color) in enumerate(s["langs"]):
        y = 134 + i * 28
        w = max(4, pct / 100 * 170)
        a(f'    <text x="460" y="{y}" class="mono" font-size="13" fill="#6f6890">{i + 1:02d}</text>\n')
        a(f'    <text x="490" y="{y}" font-size="14.5" font-weight="700" fill="#ffffff">{escape(name)}</text>\n')
        a(f'    <rect x="610" y="{y - 10}" width="170" height="8" rx="4" fill="#ffffff" fill-opacity="0.08"/>\n')
        a(f'    <rect x="610" y="{y - 10}" width="0" height="8" rx="4" fill="{color}">'
          f'<animate attributeName="width" from="0" to="{w:.1f}" begin="{0.2 + i * 0.15:.2f}s" dur="1.2s" fill="freeze" '
          f'calcMode="spline" keyTimes="0;1" keySplines="0.2 0.7 0.3 1"/></rect>\n')
        a(f'    <text x="808" y="{y}" text-anchor="end" class="mono" font-size="12" fill="#cfc8e6">{pct:.0f}%</text>\n')

    # on repeat
    a('''
    <line x1="32" y1="298" x2="808" y2="298" stroke="#ffffff" stroke-opacity="0.08"/>
    <text x="32" y="328" class="cap">ON REPEAT</text>
    <text x="808" y="328" text-anchor="end" class="cap" style="fill:#6f6890">COMMITS</text>
''')
    top = s["repos"][0][1] if s["repos"] else 1
    for i, (name, n) in enumerate(s["repos"]):
        y = 362 + i * 34
        a(f'    <text x="32" y="{y}" class="mono" font-size="13" fill="#6f6890">{i + 1:02d}</text>\n')
        a(f'    <text x="62" y="{y}" font-size="16" font-weight="700" fill="#ffffff">{escape(name if len(name) <= 26 else name[:25] + "…")}</text>\n')
        # waveform scaled by commits
        for k in range(36):
            h = 3 + ((k * 7 + i * 5) % 11) * (n / top) * 1.3
            a(f'    <rect x="{330 + k * 9}" y="{y - 6 - h / 2:.1f}" width="4" height="{h:.1f}" rx="2" '
              f'fill="{["#ff8fab", "#a59cff", "#7ee8c7"][i % 3]}" opacity="0.75"/>\n')
        a(f'    <text x="808" y="{y}" text-anchor="end" class="mono" font-size="14" font-weight="700" fill="#ffffff">{n:,}</text>\n')
    if not s["repos"]:
        a('    <text x="62" y="362" class="lbl">nothing public yet. check back soon</text>\n')

    a(f'''
    <text x="32" y="474" class="mono" font-size="11" fill="#6f6890">{s["public_repos"]} public repos · ★ {s["stars"]} · rebuilt nightly by GitHub Actions</text>
  </g>
</svg>
''')
    return "".join(out)


def main() -> None:
    args = sys.argv[1:]
    if args and args[0] == "--from-json":
        body = json.load(open(args[1]))
        out_path = args[2]
    else:
        login, out_path = args
        body = fetch(login, os.environ["GITHUB_TOKEN"])
    svg = render(summarise(body))
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "w") as f:
        f.write(svg)
    print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
