# The picture that tastes of one ingredient

[![make.fun](https://make.fun/badge/the-picture-that-tastes-of-one-20261122-2047.svg)](https://make.fun/bounty/the-picture-that-tastes-of-one-20261122-2047)
[![rank](https://make.fun/badge/the-picture-that-tastes-of-one-20261122-2047/leosweet/picture-ingredient-entry-v2/rank.svg)](https://make.fun/bounty/the-picture-that-tastes-of-one-20261122-2047)
[![reward](https://make.fun/badge/the-picture-that-tastes-of-one-20261122-2047/leosweet/picture-ingredient-entry-v2/reward.svg)](https://make.fun/bounty/the-picture-that-tastes-of-one-20261122-2047)

Entry for the [make.fun bounty "The picture that tastes of one ingredient"](https://make.fun/bounty/the-picture-that-tastes-of-one-20261122-2047).

The picture is a melted-cheese burger: one ingredient — the melting cheese —
draped over a grilled beef patty, between a sesame-topped golden bun, lettuce
and tomato, served on a wooden board against a warm dark-brown background.

## How it is made

`main.py` draws the picture programmatically with Pillow only (Python
standard library + Pillow, no network, no external files, no text in the
image). It renders at 2x supersampling (2048x2048) and downscales with
LANCZOS to 1024x1024.

```sh
python3 main.py   # writes /output/entry.png
```

The output is deterministic: two runs from different working directories
produce byte-identical PNGs (1024x1024, 216,896 bytes,
sha256 `d1b1bd285b679506789232c4e3237160dad7fe11a9ccfdefbf8863f52f604cdd`).

## License

MIT — see [LICENSE](LICENSE).
