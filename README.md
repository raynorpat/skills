# agent-skills

A personal collection of agent skills for Claude Code, Codex, and OpenCode. Each top-level folder is one skill: a `SKILL.md` plus any reference files or scripts it needs.

## Install

```bash
./install.sh
```

```powershell
./install.ps1
```

Both copy every skill into all three agents' skill folders. Pass one or more targets to narrow it: `claude`, `codex`, `opencode`, `all`, or a folder path.

| Target | Folder |
|---|---|
| `claude` | `~/.claude/skills` |
| `codex` | `~/.agents/skills` |
| `opencode` | `~/.config/opencode/skills` |

The scripts overwrite existing files and never delete, so a file removed from this repo stays in an old install until you remove it by hand.

## Skills

### Development workflow

These six are linked. A driving skill decides what shapes the work and calls planning to generate tasks; implementation executes them; doubt-driven checks the plan and non-trivial increments along the way.

| Skill | What it does |
|---|---|
| [dev-spec-driven](dev-spec-driven/SKILL.md) | Writes and gets approval for a spec before any code. Driver. |
| [dev-test-driven](dev-test-driven/SKILL.md) | Red-green-refactor: failing test first, then the code. Driver. |
| [dev-source-driven](dev-source-driven/SKILL.md) | Grounds framework and library code in official documentation, with citations. Driver. |
| [planning-and-task-breakdown](planning-and-task-breakdown/SKILL.md) | Turns a spec or requirements into ordered, verifiable tasks. The only place tasks are generated. |
| [dev-incremental-implementation](dev-incremental-implementation/SKILL.md) | Executes the task list in thin slices: implement, test, verify, commit. |
| [dev-doubt-driven](dev-doubt-driven/SKILL.md) | Adversarial fresh-context review of a plan or increment, run on a higher-tier model. |

`dev-incremental-implementation` reads the definition of done from `planning-and-task-breakdown`, so install those two together.

### Code quality and engineering

| Skill | What it does |
|---|---|
| [test-audit](test-audit/SKILL.md) | Gate for new tests and audit of existing ones: rejects duplicate, self-referential, or implementation-coupled tests and removes test-only production seams. |
| [technical-deslop](technical-deslop/SKILL.md) | Removes AI-style noise from staged and branch diffs without changing behavior. Includes C/C++ guidance. |
| [technical-documentation](technical-documentation/SKILL.md) | Builds and reviews technical docs and agent instruction files (`AGENTS.md`, `CLAUDE.md`). Carries the Karpathy coding guidelines and clean-commit rules. |
| [technical-ci-automation](technical-ci-automation/SKILL.md) | CI/CD pipelines and quality gates on GitHub Actions, Gitea Actions, or TeamCity. |
| [technical-reverse-engineering](technical-reverse-engineering/SKILL.md) | Reverse engineering of native, managed, JavaScript, packaged, and firmware targets with the REA tool, which must be installed separately. Adds guides for DOS and 16-bit Windows targets, games and DirectX/OpenGL tracking, and Capstone scans. |

### Repository maintenance

| Skill | What it does |
|---|---|
| [repo-git-cleanup](repo-git-cleanup/SKILL.md) | Sorts local branches and worktrees into merged, squash-merged, superseded, needs review, and keep, then deletes only what you confirm at two gates. Runs only when you invoke it. In Claude Code the analysis runs as a workflow of subagents; other agents use the inline fallback. |

### Writing and design

| Skill | What it does |
|---|---|
| [writing-deslop](writing-deslop/SKILL.md) | Writes or edits prose so it does not read as model-written. Covers blog posts, essays, fiction, and role play. |
| [novel-writing](novel-writing/SKILL.md) | Fiction planning, drafting, and review: character knowledge, scene causality, dialogue, style fidelity. Includes a manuscript checker for English and Chinese. |
| [ui-deslop](ui-deslop/SKILL.md) | Catalog of visual tells that make an interface look AI-generated, for generating and reviewing UI. |

## Sources

Every skill here started from someone else's work and was then renamed, generalized, or extended. Where a skill was brought in before being changed, the unmodified upstream is its own commit, so `git log -- <skill>` shows what was altered.

| Skill | Upstream | Upstream license | Changes here |
|---|---|---|---|
| test-audit | [openclaw/openclaw](https://github.com/openclaw/openclaw/tree/main/.agents/skills/test-audit) | MIT | Repo-specific links and commands removed; oracle, dominance, closed-loop, and fixture rules added from ideas in [MrZoyo/deslop-GPT](https://github.com/MrZoyo/deslop-GPT/tree/main/skills/deslop) (MIT) |
| technical-documentation | [openclaw/openclaw](https://github.com/openclaw/openclaw/tree/main/.agents/skills/technical-documentation), itself from [vincentkoc/dotskills](https://github.com/vincentkoc/dotskills) | MIT | OpenClaw overlay generalized into `references/page-types.md`; [Karpathy guidelines](https://github.com/multica-ai/andrej-karpathy-skills) added with a clean-commits section |
| technical-deslop | [vincentkoc/dotskills](https://github.com/vincentkoc/dotskills/tree/main/skills/technical-deslop) | MIT | C/C++ guidance added |
| technical-ci-automation | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main/skills/ci-cd-and-automation) | MIT | Renamed; Gitea Actions and TeamCity references added |
| dev-spec-driven, dev-test-driven, dev-source-driven, dev-doubt-driven, dev-incremental-implementation, planning-and-task-breakdown | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main/skills) | MIT | Renamed and cross-linked into one workflow; references to skills not in this repo removed; doubt-driven's cross-model step replaced with a higher-tier reviewer |
| writing-deslop | [axel-pm/deslopify](https://github.com/axel-pm/deslopify) | MIT | Form detection, draft mode, and `references/forms.md` for blog posts, fiction, and role play |
| ui-deslop | [kmaida/deslop-skills](https://github.com/kmaida/deslop-skills/tree/main/deslop-ui) | None stated | Renamed; generation checklist and roughly double the catalog |
| technical-reverse-engineering | [morluto/rea](https://github.com/morluto/rea/tree/main/.agents/skills/reverse-engineer-anything) | MIT | Renamed; DOS and 16-bit Windows, games and graphics, and Capstone references added, plus `scripts/capstone_scan.py` |
| novel-writing | [wgwtest/novel-writing](https://github.com/wgwtest/novel-writing/tree/main/novel-writing) | MIT | Manuscript checker extended to English |
| repo-git-cleanup | [trailofbits/skills](https://github.com/trailofbits/skills/tree/main/plugins/git-cleanup) | CC BY-SA 4.0 | Plugin slash command converted to a skill; plugin-root lookup replaced with the skill directory; evals not included. Share-alike: this skill stays under CC BY-SA 4.0 |

Two upstreams have no license file: `kmaida/deslop-skills` (ui-deslop) and `multica-ai/andrej-karpathy-skills` (the guidelines inside technical-documentation). Get permission or replace that material before publishing this repo.
