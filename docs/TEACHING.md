# Learn this translate.js fork

This is a fork of [xnx3/translate](https://github.com/xnx3/translate) by 管雷鸣, licensed MIT. At `df9d77c85399470d10e2cb610f17e294ac107740`, the fork HEAD equals upstream HEAD checked on 2026-10-22; I found no AIEN-specific delta at this pin. Its retained role is an upstream browser translation reference, not an AIEN authored inference backend. The default branch is `master`.

[`translate.execute`](../translate.js/translate.js) picks explicit elements, configured documents or the whole page, extracts text into queues, then [`translate.request`](../translate.js/translate.js) sends requests to the configured translation service. [`translate.ignore`](../translate.js/translate.js) protects selected tags, classes, IDs and text; [`translate.listener`](../translate.js/translate.js) can observe dynamic page changes. The default API host is `api.translate.zvo.cn`; `client.edge` in the upstream [demo](../translate.js/demo.html) is an external browser translation channel. Neither path invokes local AIEN inference. The separate [aien-translate](https://github.com/aien-dev/aien-translate) project owns any AIEN integration at its own source pin.

## Fresh checkout exercise

Prerequisites: Git and Node 22. Checkout `df9d77c85399470d10e2cb610f17e294ac107740`, then run from repository root:

```sh
node --check translate.js/translate.js
```

Expected no stdout, exit 0. This is a syntax check only. For a browser demonstration, open [`translate.js/demo.html`](../translate.js/demo.html) in a local HTTP server, observe the language selector, and change language. That page loads an external script and translation service, so text translation and network behavior are unqualified by this offline exercise. A network refusal is expected to leave translation unavailable; do not mistake that for local AIEN inference. [Replay receipt](teaching-replay-2026-10-22.txt).
