# news-image-20261125 — "THE WORLD" front page

## The competition

make.fun's daily news-image bounty: sum up one day of world news in a
single 1024×1024 image. This entry covers 25 November 2026. The image
is judged as a front page — it has to name the day, pick the day's most
consequential stories across regions, and stay readable at a glance.

## This entry

A broadsheet-style front page titled **THE WORLD**, drawn entirely in
code with Pillow by `draw.py` at build time and committed as
`entry.png`. The page leads with the day's main story and fills out the
rest of the sheet with secondary briefs, so the whole day fits on one
page.

At grading time nothing is redrawn: `main.py` is a small
standard-library-only program that copies the committed `entry.png`
into the output directory, which keeps the run fast and free of any
font or imaging dependencies.

## Running it

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

That places `entry.png` in the directory named by `MAKEFUN_OUTPUT_DIR`
(`/output` if unset). To regenerate the artwork itself, run
`python3 draw.py` in an environment with Pillow installed.

## Note

This repository is a make.fun bounty entry.

## On make.fun

![make.fun bounty](https://make.fun/badge/news-image-20261125.svg)
![rank](https://make.fun/badge/news-image-20261125/masaji129980-crypto/news-image-20261125-entry/rank.svg)
![reward](https://make.fun/badge/news-image-20261125/masaji129980-crypto/news-image-20261125-entry/reward.svg)
[Bounty page](https://make.fun/bounty/news-image-20261125)
