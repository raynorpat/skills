# Gitea Actions

Gitea Actions runs GitHub Actions-style workflow YAML on self-hosted runners. Most of the examples in `SKILL.md` work after the adjustments below. Gitea's compatibility has changed release to release, so confirm version-specific points against the "Comparison with GitHub Actions" page in the docs for the installed Gitea version.

## Where things live

| Concern | Gitea Actions |
|---|---|
| Workflow files | `.gitea/workflows/*.yaml`. If that directory is absent, Gitea falls back to `.github/workflows/`. Use `.gitea/` when the repo is mirrored to GitHub and the two need different pipelines. |
| Runners | `act_runner`, always self-hosted. Nothing runs until at least one runner is registered at instance, organization, or repository level. |
| Secrets and variables | Repository, organization, or user settings, then `${{ secrets.NAME }}` and `${{ vars.NAME }}`. Names may not start with `GITHUB_` or `GITEA_`. |
| Contexts | `gitea.*` is available and `github.*` is kept as an alias, so `github.event_name`, `github.ref`, and `github.sha` keep working. |
| Job token | An automatic token is provided per job (`secrets.GITEA_TOKEN`, also exposed as `secrets.GITHUB_TOKEN`). Its scope is narrower than GitHub's; use a dedicated access token stored as a secret for cross-repository or package operations if the automatic one is refused. |
| Required checks | Branch protection, "Enable Status Check", listing the workflow job names. |

## What to change when porting a GitHub workflow

1. **`runs-on` must match a runner label.** Labels are defined when the runner is registered and map to a container image or to the host, for example `ubuntu-latest:docker://node:22-bookworm` or `linux-amd64:host`. There are no hosted images: a job whose label no runner offers waits forever. Check which labels exist before writing `runs-on`.
2. **Know where `uses:` resolves.** `uses: actions/checkout@v4` is fetched from the instance's configured default actions URL (`[actions] DEFAULT_ACTIONS_URL`), which is GitHub by default on current versions but may be the Gitea instance itself or blocked on an air-gapped install. An absolute URL removes the ambiguity: `uses: https://github.com/actions/checkout@v4` or `uses: https://gitea.example.com/actions/checkout@v4`.
3. **Check the tool images.** Default runner images are much smaller than GitHub's. Tools you assumed were preinstalled (Node, Docker CLI, browsers, cloud CLIs) may be missing; install them in the job or use a label mapped to a fuller image.
4. **Expect some keys to be ignored.** Historically ignored or unsupported: `permissions`, `concurrency`, `environment`, `run-name`, job-level `timeout-minutes` and `continue-on-error`, and some `defaults.run` settings. Newer releases have added several of these. If a gate depends on one (a concurrency group that prevents overlapping deploys, for example), confirm it works on the installed version instead of assuming.
5. **Artifacts and cache.** `actions/upload-artifact` and `actions/download-artifact` v4 need a recent Gitea; on older versions pin v3. `actions/cache` works against the cache server built into `act_runner`; on multi-runner setups make sure the runners can reach it.
6. **Service containers** (`services:`) work when the job runs in a container label. With a `host` label, the job reaches services on `localhost` only if they are started another way.
7. **Docker inside jobs.** Building images needs the Docker socket mounted into the job container or a Docker-in-Docker runner configuration. This is a runner setting, not a workflow setting.

## Basic pipeline

```yaml
# .gitea/workflows/ci.yaml
name: CI

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

jobs:
  quality:
    runs-on: ubuntu-latest   # must be a label a registered runner offers
    steps:
      - uses: https://github.com/actions/checkout@v4
      - uses: https://github.com/actions/setup-node@v4
        with:
          node-version: '22'
          cache: 'npm'
      - run: npm ci
      - run: npm run lint
      - run: npx tsc --noEmit
      - run: npm test -- --coverage
      - run: npm run build
```

## Features that differ

- **Dependency updates.** Dependabot is a GitHub service and does not exist here. Run Renovate against the Gitea platform, either as a scheduled workflow in a dedicated repository or as a separate service, with a bot account token.
- **Preview deployments.** No built-in environments or deployment records. Deploy from a workflow step and post the URL back as a pull-request comment through the Gitea API.
- **Scheduled and manual runs.** `schedule:` cron triggers run on the default branch. `workflow_dispatch` needs a reasonably recent Gitea.
- **Larger runners.** Scale by registering more or bigger `act_runner` instances and giving them distinct labels (`runs-on: big`).
- **Packages.** Gitea has its own package and container registry; log in with a token secret and push to `gitea.example.com/owner/image`.

## Feeding failures back to an agent

Job logs are available in the web UI and through the Gitea API (`/api/v1/repos/{owner}/{repo}/actions/...`; available endpoints depend on version). The `tea` CLI covers pull requests and issues. When the API on the installed version does not expose logs, have the workflow upload test reports as an artifact or post a failure summary as a pull-request comment so the output is retrievable.

## Red flags specific to Gitea

- A workflow copied from GitHub that has never completed a run because no runner offers its `runs-on` label.
- Relying on `permissions:` or `concurrency:` for safety without confirming the installed version honors them.
- One shared host-mode runner executing untrusted pull-request code with access to the host and its Docker socket.
- Secrets exposed to workflows triggered by forks.
