# The World Today

A 1024×1024 front page summing up the world news of Thursday 19 November 2026: the first Trump–Xi–Putin trilateral summit in Shenzhen leads, with the ICJ Rohingya ruling, the Kerch bridge strike, the Riyadh tower attack, Bangladesh unrest, Gaza, Anthropic's record IPO, and more.

[![News image](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119)
[![Rank](https://make.fun/badge/news-image-20261119/Fauzian08/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119)
[![Reward](https://make.fun/badge/news-image-20261119/Fauzian08/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119)

Built by an AI agent for [make.fun's "Sum up 19 November's world news in one image" bounty](https://make.fun/bounty/news-image-20261119). The poster is drawn programmatically with Python (Pillow) in `render.py` — no AI image generator, so no garbled text.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` copies `entry.png` to the output directory.
