# Sum up 25 November's world news in one image

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/slowwilly20/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/slowwilly20/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

make.fun bounty: **news-image-20261125** — $100, ends Fri 27 Nov 2026 07:00 WIB
(00:00 UTC). 50 best win rates share $100 (1st $20, 2nd $12, 3rd $6,
4th–10th $2, 11th–50th $1.20). An AI judge compares images two at a time
and picks the one that best sums up the day's world news.

## What it is

A one-page newspaper front page — **WORLD NEWS, Wednesday 25 November
2026** — built around a **world map**: the six biggest stories of the
day are pinned at their real locations (Gulf of Finland, Antalya,
Washington DC, New York, Ituri, Riyadh) and the story list below the
map is keyed to the pin numbers. The idea: the image is a map of the
day's world news, not just a list of it.

1. **Ukraine** — drone strikes on Russian ships (Baltic + Libya)
2. **Climate** — COP31 collapses with no deal
3. **Cyber** — CIA and spy chief's office hacked
4. **Tech** — Huawei guilty of stealing trade secrets
5. **Health** — WHO pulls Ebola staff out of Congo
6. **Middle East** — Houthis hit Riyadh's tallest tower

Sources are printed on the image: Reuters · CNN · AFP · WHO.
Per-story sources with URLs: see [NEWS.md](NEWS.md).

## Files

| File | What it is |
|---|---|
| `main.py` | The entry program (Python 3.13, stdlib only, no network). Writes `entry.png` to `/output/entry.png` and verifies its SHA-256. The brief allows the simplest program to copy an image the repository holds. |
| `entry.png` | The image itself — 1024×1024 PNG, 115,598 bytes (limit: 1 MiB, 1024×1024). |
| `news.json` | The day's news data (headlines, summaries, sources, pin locations) the image was built from. |
| `generate_image_v2.py` | Build-time renderer (PIL) that produced `entry.png` from `news.json` + `world.geo.json`. Kept in the repo so the image is fully reproducible. |
| `world.geo.json` | World country outlines (johan/world.geo.json) used to draw the map. |
| `generate_image.py` | v1 renderer (plain text grid, superseded by v2). Kept for provenance. |
| `LICENSE` | MIT (OSI-approved). |

## Run

```sh
python3 main.py
# wrote /output/entry.png (115598 bytes, sha256 a20d4d01...)
```

Deterministic: running it twice writes the exact same bytes (SHA-256 is
checked by the program itself). No network at run time; only the Python
standard library is used.

To re-render the image from the news data (build time only):

```sh
pip install pillow
python3 generate_image_v2.py news.json entry.png
```

## Submission checklist (before submitting)

- [ ] Create the public GitHub repo under the slowwilly20 account **after
      the competition opened** (25 Nov 2026 00:00 UTC) and push these files.
- [ ] Attach the AI coding-agent transcripts of the sessions that built it.
- [ ] Submit before Fri 27 Nov 2026 07:00 WIB; the last submission before
      the deadline is the final entry.
