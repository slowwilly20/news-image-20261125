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
2026** — with the six biggest stories of the day plus an "also today"
ticker:

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
| `entry.png` | The image itself — 1024×1024 PNG, 129,696 bytes (limit: 1 MiB, 1024×1024). |
| `news.json` | The day's news data (headlines, summaries, sources) the image was built from. |
| `generate_image.py` | Build-time renderer (PIL) that produced `entry.png` from `news.json`. Kept in the repo so the image is fully reproducible. |
| `LICENSE` | MIT (OSI-approved). |

## Run

```sh
python3 main.py
# wrote /output/entry.png (129696 bytes, sha256 09b7d977...)
```

Deterministic: running it twice writes the exact same bytes (SHA-256 is
checked by the program itself). No network at run time; only the Python
standard library is used.

To re-render the image from the news data (build time only):

```sh
pip install pillow
python3 generate_image.py news.json entry.png
```

## Submission checklist (before submitting)

- [ ] Create the public GitHub repo under the slowwilly20 account **after
      the competition opened** (25 Nov 2026 00:00 UTC) and push these files.
- [ ] Attach the AI coding-agent transcripts of the sessions that built it.
- [ ] Submit before Fri 27 Nov 2026 07:00 WIB; the last submission before
      the deadline is the final entry.
