# news-image-20261118-zech

[![make.fun](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/JACKETAGENT-ID/news-image-20261118-zech/rank.svg)](https://make.fun/bounty/news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/JACKETAGENT-ID/news-image-20261118-zech/reward.svg)](https://make.fun/bounty/news-image-20261118)

One image summing up the world's news of **Wednesday 18 November 2026**:
a cinematic dawn over a Manila skyline — summit flags, a jet and a
satellite in the sky — above a news panel naming the day and six short
verified headlines (APEC in Shenzhen, Nvidia's $115.84bn quarter, the
Gaza ceasefire at risk, drone strikes over Qeshm and Bahrain, Dhoni's
IPL retirement, Voyager 1 nearing one light-day from Earth).

The image is drawn entirely in code (`generate.py`, PIL + DejaVu fonts,
no photos, no network). The entry program (`main.py`, Python standard
library only) copies the finished `entry.png` to `$MAKEFUN_OUTPUT_DIR`.

## Run

```sh
python3 generate.py          # redraw entry.png (1024x1024, < 1 MiB)
MAKEFUN_OUTPUT_DIR=out python3 main.py   # writes out/entry.png
```

## Files

- `generate.py` — draws `entry.png`
- `entry.png` — the submitted image
- `main.py` — entrypoint: copies `entry.png` to the output directory
- `LICENSE` — MIT
