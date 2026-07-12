# Security Policy

<b>English</b> · <a href="i18n/SECURITY.de.md">Deutsch</a>
<br /><br />

## Reporting a vulnerability

Please report privately through GitHub's
[private vulnerability reporting](https://github.com/Ollornog/1pipe/security/advisories/new)
rather than opening a public issue. Expect a first reply within a week.

## Scope and design decisions worth knowing

The application is still being built; this policy states the design intent that its code is held to.

- **Secrets come from the environment, never the repo.** Chat, model and archive endpoints and their
  tokens are read from environment variables. The repository ships neutral examples only.
- **Authentication is delegated** to [TinySesam](https://github.com/Ollornog/TinySesam) and an OIDC
  provider. 1pipe stores no passwords.
- **A message from the chat is untrusted input.** The bridge guards against answering its own
  messages (a webhook loop) and treats every incoming message as attacker-controlled text before it
  reaches a tool.
- **Mutating actions require an explicit confirmation.** The assistant does not delete, re-classify
  or write on an inferred intent; a yes/no step stands between a suggestion and an effect.
- **Connectors are scoped by channel.** A tool the registry does not grant a channel is not
  reachable from it. Keep the grant per room as small as the room needs.

## Not in scope

The security of the third-party services 1pipe connects to (the chat server, the model provider,
the archive), and anything an authenticated operator can do by design.

<br /><br />
<p align="right"><img src="docs/pipe.png" alt="1pipe" width="60" height="60"></p>
