# translate (preserved AIEN fork of translate.js)

> This repository is AIEN's preserved copy of translate.js (https://github.com/xnx3/translate), the MIT-licensed browser library that translates a web page in place with two lines of JavaScript, published on npm as `i18n-jsautotranslate`. AIEN keeps it so the exact upstream code its translation server talks to stays available. The AIEN translation server lives in a separate repository, https://github.com/aien-dev/aien-translate. Apart from this AGENTS.md, the default branch `master` matches upstream `xnx3/translate` `master`.
Shared rules: read https://www.aienos.com/agents/RULES.md first. This file adds what is specific to this repository; where the two differ, this file wins here.

## Scope

- This is a fork kept as a faithful copy. Upstream code, history, tags and attribution are preserved as published.
- Changes accepted here:
  - Syncing from upstream `xnx3/translate` `master`, as a merge that keeps upstream commits and tags unchanged.
  - Edits to this AGENTS.md.
- Changes not accepted here: edits to upstream files (`translate.js/`, `extend/`, `deploy/`, `dev/`, `doc/`, `README.md`, `CLAUDE.md`, `package.json`, `LICENSE`, `.github/workflows/`), rewritten or deleted upstream tags, and AIEN integration code. Fixes to translate.js go upstream to `xnx3/translate`; AIEN integration goes to `aien-dev/aien-translate`.
- Main areas, as described in `CLAUDE.md`: `translate.js/translate.js` is the core library (with `translate.min.js` and `debug.js` beside it); `extend/` holds framework integrations and a Java core library; `deploy/` holds server install scripts; `dev/` holds the npm version tooling; `doc/` holds documentation. `extend/react` is a git submodule pointing to a third-party repository.

## Installation

```bash
git clone https://github.com/aien-dev/translate.git
cd translate
git remote add upstream https://github.com/xnx3/translate.git
```

There is no build step for the core library; `translate.js/translate.js` is loaded directly by a page. The repository has no `npm` dependencies at its root. The demos under `extend/` (Vue 3, Vant, React) each have their own `package.json` and need `npm install` with network access.

## Usage

```bash
# Syntax check of the core library (Node.js, no network)
node --check translate.js/translate.js

# Compare this fork with upstream
git fetch upstream
git log --oneline master..upstream/master
```

Using the library in a page, and pointing it at an aien-translate server, is documented in the aien-translate README:

```html
<script src="/translate.js"></script>
<script>
  translate.service.use('translate.service');
  translate.request.setHost('https://your-server.example/');
  translate.execute();
</script>
```

## Conventions

- Upstream conventions in `CLAUDE.md` apply to the upstream code: the version string between `// AUTO_VERSION_START` and `// AUTO_VERSION_END` is written by `dev/update-version.js`, configuration fields live in `translate.config.data`, and new framework integrations go under `extend/`. They matter here only when reading the code, since upstream files are not edited in this fork.
- Upstream documentation and commit messages are mostly in Chinese. Keep them as they are.

## Safety and approvals

- Do not run `npm run version` or `npm run postversion`. `version` rewrites and stages `translate.js/translate.js`; `postversion` runs `git push && git push --tags`.
- Do not create `v*.*.*` tags or GitHub releases on this fork. `.github/workflows/release.yml` drafts a release on such tags and `.github/workflows/publish.yml` runs `npm publish` on a published release; npm publishing belongs to upstream.
- Do not run the scripts in `deploy/`. They install and upgrade translation services on a server and need root.
- Ask before syncing from upstream, and never force-push `master`.

## Further reading

- `CLAUDE.md`: upstream's architecture and development notes (Chinese).
- `README.md`: upstream's user guide (Chinese).
- `dev/README.md`: upstream's npm release procedure.
- https://github.com/xnx3/translate: upstream repository.
- https://github.com/aien-dev/aien-translate: the AIEN translation server for translate.js.
