<p align="center"><img src="docs/pipe.png" alt="1pipe" width="250" height="250"></p>

<h1 align="center">1pipe</h1>

<p align="center"><b>English</b> · <a href="i18n/README.de.md">Deutsch</a></p>

<p align="right">
<a href="https://github.com/Ollornog/1pipe/actions/workflows/ci.yml"><img src="https://github.com/Ollornog/1pipe/actions/workflows/ci.yml/badge.svg" alt="tests"></a>
<a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-informational.svg" alt="License: MIT"></a>
<img src="https://img.shields.io/badge/python-3.10%2B-blue.svg" alt="Python">
</p>

> 🚧 **Work in progress** — under active development; interfaces and structure may still change before a stable `1.0` release.

### A lean, self-hosted AI chat platform and connector framework for Rocket.Chat.

1pipe puts an assistant into a team's own chat and gives it tools: search a document
archive, keep a per-person todo list, run a web-research task. A small connector registry maps
each channel to what the assistant may do there. It is meant to replace a heavy visual automation
tool with a few hundred lines of explicit Python.

Built with FastAPI. The language model is pluggable; the reference wiring targets a provider with
a native web-search tool. Sign-in is delegated to [TinySesam](https://github.com/Ollornog/TinySesam).
It is a companion to [paperlaiss](https://github.com/Ollornog/paperlaiss), which it drives through
that project's JSON API rather than duplicating it.

---

## Status

**Early — the platform is being built.** This repository currently carries the project skeleton:
licence, docs, the shared test base and the hardened CI. The application code lands incrementally
behind it. Watch the [releases feed](https://github.com/Ollornog/1pipe/releases); there will be
no `latest` tag on purpose.

## What it will do

- **Bridge a chat room to an assistant.** An incoming webhook carries a message in; the reply goes
  back through the chat API, with a guard against the bot answering itself.
- **Route by channel.** A connector registry decides which tools a message in a given channel may
  reach — the document connector in one room, research in another.
- **Remember across restarts.** Conversation memory is read from the chat server's own history, not
  a separate store that can drift or vanish on a redeploy.
- **Ask before it changes anything.** Mutating actions require an explicit yes/no confirmation; the
  assistant does not act on an inferred intent.

## Design

- **One ecosystem.** Python and FastAPI throughout, so the LLM, archive and chat building blocks are
  shared with [paperlaiss](https://github.com/Ollornog/paperlaiss) — one deploy and one auth pattern.
- **Configuration from the environment.** No endpoint, token or model is baked into the code; the
  repository ships neutral examples only.
- **Auth is delegated.** The platform panel sits behind [TinySesam](https://github.com/Ollornog/TinySesam)
  and an OIDC provider — 1pipe stores no passwords.
- **Small on purpose.** A connector is a handful of tools with a clear contract, not a plugin zoo.

## Connectors

| Connector | What it does |
|-----------|--------------|
| **Archive** | Search, open and re-classify documents in a Paperless-ngx archive (via paperlaiss); upload through its ingest API. |
| **Todo** | A per-person task list, the person tied to their chat / OIDC identity. |
| **Research** | A web-research task run through the model's search tool, interactive or scheduled, that stays quiet when there is nothing to report. |

## Development

```bash
./scripts/check.sh          # hygiene tests (more suites land with the app code)
git config core.hooksPath .githooks
```

The suite is **repeatable**: running it twice must be green twice. See
[`CONTRIBUTING.md`](CONTRIBUTING.md).

## Security

Report vulnerabilities privately — see [`SECURITY.md`](SECURITY.md).

## Licence

[MIT](LICENSE)

## Credits

Icon: <a href="https://www.flaticon.com/authors/vectorsmarket15" target="_blank" rel="noopener">Pipe PNG Image by vectorsmarket15 - flaticon.com</a>
