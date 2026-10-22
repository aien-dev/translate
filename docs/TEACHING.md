# Learn this translate.js fork

This is a fork of [xnx3/translate](https://github.com/xnx3/translate) by 管雷鸣, licensed MIT. At `df9d77c85399470d10e2cb610f17e294ac107740`, the fork HEAD equals upstream HEAD checked on 2026-10-22; I found no AIEN-specific delta at this pin. Its retained role is an upstream browser translation reference, not an AIEN authored inference backend. The default branch is `master`.

[`translate.execute`](../translate.js/translate.js) picks explicit elements, configured documents or the whole page, extracts text into queues, then [`translate.request`](../translate.js/translate.js) sends requests to the configured translation service. [`translate.ignore`](../translate.js/translate.js) protects selected tags, classes, IDs and text; [`translate.listener`](../translate.js/translate.js) can observe dynamic page changes. The default API host is `api.translate.zvo.cn`; `client.edge` in the upstream [demo](../translate.js/demo.html) is an external browser translation channel. Neither path invokes local AIEN inference. The separate [aien-translate](https://github.com/aien-dev/aien-translate) project owns any AIEN integration at its own source pin.

## Fresh checkout exercise

Prerequisites: Git and Node 22. Checkout `df9d77c85399470d10e2cb610f17e294ac107740`, then run from repository root:

```sh
node --check translate.js/translate.js
```

Expected no stdout, exit 0. This is a syntax check only. For a browser demonstration, open [`translate.js/demo.html`](../translate.js/demo.html) in a local HTTP server, observe the language selector, and change language. That page loads an external script and translation service, so text translation and network behavior are unqualified by this offline exercise. A network refusal is expected to leave translation unavailable; do not mistake that for local AIEN inference. [Replay receipt](teaching-replay-2026-10-22.txt).

## Local browser boundary demo, with external services disabled

The upstream syntax check above is not a browser exercise. This additional [local fixture](local-boundary.html) loads the preserved repository script, queues `Hello world`, excludes a synthetic `ignore` element and a `code` element, and intercepts `translate.request.post` **before sending**. A `connect-src 'none'` policy blocks external connections. It supplies no fake translation response and does not pretend to run AIEN inference. The original DOM stays unchanged because translation itself is NOT_RUN.

Prerequisites: Git, Python 3, `uv`, and an installed Google Chrome. The automated checker uses Playwright **1.60.0** through an isolated uv environment (the first use may download the Python package; it does not download a model or install an account service). Chrome **155.0.8059.85** was observed in the recorded run; other browser versions have not been qualified by this receipt.

```sh
set -eu
: "${TMPDIR:?set TMPDIR to a writable scratch directory}"
work=$(mktemp -d "$TMPDIR/translate-boundary.XXXXXX")
git clone --quiet --branch docs/teaching-20261022 https://github.com/aien-dev/translate.git "$work/tree"
cd "$work/tree"
git checkout --quiet --detach 2f9d7f2493a3f38e6d2f0cee82d57be279a8441c
uv run --with playwright==1.60.0 python docs/replay-local-boundary.py
uv run --with playwright==1.60.0 python docs/replay-local-boundary.py --prove-ignore-control
```

Both commands exit **0**. The first must report all four booleans true. The control removes only the fixture's `ignore` class in the browser response and must report `ignoredClassExcluded: false` plus `PROTECTION_REMOVAL_CAUGHT`; no source file or upstream code is changed. In the positive run, `eligibleTextQueued`, `ignoredClassExcluded`, `codeTagExcluded` and `originalDOMUnchanged` must all be `true`, and `observed_external_request_attempts` must be **0**. The helper starts and stops its own loopback-only HTTP server. [Observed browser replay and a protection-removal negative control](local-boundary-replay.txt).

To inspect it manually, serve this pinned checkout with `python3 -m http.server 8765 --bind 127.0.0.1` and open `http://127.0.0.1:8765/docs/local-boundary.html`. The page shows the request-boundary result and explicitly says translation NOT_RUN. Stop that local server when finished. The original upstream demo remains a separate external-service route, not part of this local demonstration.


### Parent fresh-checkout replay

A separate coordination replay is retained in [the parent receipt](parent-replay-2026-10-22.txt). Its scope and observed exit are explicit; source review and final desk qualification remain separate. A recorded absence or expected failing baseline is not a passing implementation.
