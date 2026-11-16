# TeamCity

TeamCity is a build server with its own model, not a workflow-YAML runner. The quality gates in `SKILL.md` apply unchanged; the way they are expressed does not. Keep the configuration in the repository as Kotlin DSL so pipeline changes are reviewed like code.

DSL packages and option names shift between TeamCity versions. Before writing DSL by hand, open an existing build configuration in the UI and use "View as code" to see the exact form the installed server generates, and match the `version` it reports.

## Concept mapping

| GitHub Actions | TeamCity |
|---|---|
| Workflow file in `.github/workflows/` | Versioned settings: `.teamcity/settings.kts` (Kotlin DSL) in the repository |
| Workflow | Project containing one or more build configurations |
| Job | Build configuration (`BuildType`) |
| Step | Build step (`script`, `gradle`, `maven`, `dockerCommand`, and other runners) |
| `runs-on` | Agent requirements, matched against agent parameters; agent pools scope which agents a project may use |
| `needs:` | Snapshot dependency (same revision, ordered) plus artifact dependency (pass files) |
| Parallel jobs | Several build configurations in one build chain, or the parallel tests build feature to split one suite across agents |
| `on: push` / `pull_request` | VCS trigger with a branch filter; Pull Requests build feature to discover PR branches |
| Status checks on the PR | Commit Status Publisher build feature (supports GitHub, Gitea, GitLab, Bitbucket, and others) |
| `secrets.X` | Parameter of type password, referenced as `%name%`; stored outside the repository and shown in DSL as a `credentialsJSON:<id>` token |
| `vars.X` / `env` | Configuration parameters (`%name%`), `env.NAME` parameters for environment variables |
| `container:` | `dockerImage` on a step, which runs that step inside the image |
| `services:` | No direct equivalent. Start dependencies with a Docker Compose step, or run them on the agent |
| `upload-artifact` | `artifactRules` on the build configuration |
| `timeout-minutes` | Failure condition `executionTimeoutMin` |
| Reusable workflow | Build configuration template, or a shared Kotlin function or class in the DSL |
| `workflow_dispatch` inputs | Parameters with a prompt display, set in the Run custom build dialog |
| Scheduled workflow | Schedule trigger |
| Environment with approval | Deployment-type build configuration, optionally with the build approval feature |

## Basic pipeline as Kotlin DSL

```kotlin
// .teamcity/settings.kts
import jetbrains.buildServer.configs.kotlin.*
import jetbrains.buildServer.configs.kotlin.buildFeatures.commitStatusPublisher
import jetbrains.buildServer.configs.kotlin.buildFeatures.pullRequests
import jetbrains.buildServer.configs.kotlin.buildSteps.script
import jetbrains.buildServer.configs.kotlin.triggers.vcs

version = "2024.03" // match the server; copy from "View as code"

project {
    buildType(Quality)
}

object Quality : BuildType({
    name = "Quality gates"

    vcs {
        root(DslContext.settingsRoot)
    }

    steps {
        script {
            name = "Install"
            scriptContent = "npm ci"
            dockerImage = "node:22"
        }
        script {
            name = "Lint"
            scriptContent = "npm run lint"
            dockerImage = "node:22"
        }
        script {
            name = "Type check"
            scriptContent = "npx tsc --noEmit"
            dockerImage = "node:22"
        }
        script {
            name = "Test"
            scriptContent = "npm test -- --coverage"
            dockerImage = "node:22"
        }
        script {
            name = "Build"
            scriptContent = "npm run build"
            dockerImage = "node:22"
        }
    }

    triggers {
        vcs {
            branchFilter = "+:*"
        }
    }

    features {
        pullRequests {
            vcsRootExtId = "${DslContext.settingsRoot.id}"
            provider = github {
                authType = token { token = "credentialsJSON:<token-id>" }
                filterAuthorRole = PullRequests.GitHubRoleFilter.MEMBER
            }
        }
        commitStatusPublisher {
            vcsRootExtId = "${DslContext.settingsRoot.id}"
            publisher = github {
                githubUrl = "https://api.github.com"
                authType = personalToken { token = "credentialsJSON:<token-id>" }
            }
        }
    }

    failureConditions {
        executionTimeoutMin = 15
    }

    artifactRules = "coverage => coverage.zip"
})
```

A step that exits non-zero fails the build and, by default, skips the steps after it, which gives the same "no gate can be skipped" behavior as sequential workflow steps. For a Gitea-hosted repository, use the Gitea publisher in `commitStatusPublisher` and the matching provider in `pullRequests`.

## Patterns

- **Split gates into a build chain when the single configuration gets slow.** Make `Lint`, `Test`, and `Build` separate build configurations and add a composite configuration that has snapshot dependencies on all three. They run in parallel on separate agents, on the same revision, and the composite gives one status to require on the pull request.
- **Integration tests with a database.** Add a Docker Compose step that starts the database before the test step, or a script step running `docker compose up -d --wait`. Pass credentials as password parameters, never as literals in the DSL.
- **Test reporting.** Runners for common tools report tests automatically. For anything else, emit JUnit XML and add the XML report processing build feature, or print TeamCity service messages (`##teamcity[testStarted ...]`). Reported tests give flaky-test detection, muting, and investigation assignment.
- **Deployments.** Use a separate deployment-type build configuration with an artifact dependency on the build it ships. Trigger it on a finished build for staging; leave production manual or behind build approval.
- **Rollback.** Re-run the deployment configuration and choose an earlier build as the artifact source. Keep enough build history and artifacts for this to be possible (check the clean-up rules).
- **Caching.** Agents keep checkout directories and local package caches between builds by default, so repeat builds are warm on the same agent. For ephemeral or cloud agents, use the build cache feature where the server version has it, or a shared cache volume.
- **Secrets.** Define password parameters at the narrowest project level that needs them. With versioned settings, the repository contains only `credentialsJSON` tokens; the values stay on the server. Disable "Run custom build" parameter overrides on configurations that hold deploy credentials, and do not let pull requests from forks build configurations that can read them.
- **Failure conditions beyond exit codes.** Fail on a build log message, on a metric change (test count drops, coverage falls, artifact size grows), or on timeout.

## Features that differ

- **Dependency updates.** Not built in. Run Renovate as a scheduled build configuration or separate service against the VCS host.
- **Preview deployments.** A build configuration triggered by the Pull Requests feature deploys the preview; post the URL with a script step calling the VCS host's API, or surface it as a build status text.
- **Settings changes need care.** With versioned settings enabled, a change to `.teamcity/` on a branch can alter what that branch's build does. Decide whether builds use settings from the default branch only or from the branch being built, and restrict the latter for untrusted contributors.

## Feeding failures back to an agent

The REST API exposes build status, failed tests, and logs: `GET /app/rest/builds/<locator>`, `/app/rest/testOccurrences?locator=build:(id:<id>),status:FAILURE`, and `/downloadBuildLog.html?buildId=<id>`. Authenticate with an access token in an `Authorization: Bearer` header. Prefer the failed-test list over the raw log: it is structured and short.

## Red flags specific to TeamCity

- Pipeline configured only in the UI, with no versioned settings, so changes are unreviewed and unrecoverable.
- Deploy credentials defined on the root project and inherited by every configuration.
- Pull-request builds from forks running on agents that hold deployment secrets or a writable Docker socket.
- A build chain whose final composite is not the required status check, so a failed member does not block the merge.
- Clean-up rules that delete the artifacts a rollback would need.
