# agentfiles

Dotfiles for agent instructions and skills.

`agentfiles` keeps one canonical source tree and materializes it into the
locations expected by local agents such as Codex and Claude.

## Layout

```text
agentfiles/
  global/
    instructions/
      00-working-agreements.md
      10-command-approval-hygiene.md
    skills/
      dev-ask/
        SKILL.md
      dev-request/
        SKILL.md
  repos/
    example-app/
      instructions/
        00-guidance.md
      skills/
        app-review/
          SKILL.md
  bin/
    agentfiles
```

The first version is convention-based. There is no manifest:

- `global/instructions/*.md` are concatenated in lexical order.
- `global/skills/*/SKILL.md` are installed as global skills.
- `repos/<name>/instructions/*.md` can be included as path-conditional guidance.
- `repos/<name>/skills/*/SKILL.md` can be installed globally with a repo prefix,
  so the target repository does not need to be modified.

## Included global skills

| Skill | Purpose |
| :--- | :--- |
| `dev-ask` | Answer a narrow question with facts, without making changes. |
| `dev-explain` | Investigate and explain how something works, without making changes. |
| `dev-fyi` | Acknowledge information without starting new work. |
| `dev-request` | Carry out a precisely scoped instruction. |
| `continue-work` | Continue an active task and report what remains. |
| `do-ticket` | Implement a ticket to its stated acceptance criteria. |
| `review-loop` | Review changes and fix findings until no actionable findings remain. |

Run `bin/agentfiles install --mode link` to make this repo the shared source
for Codex and Claude. In Claude, invoke them as `/dev-ask`, `/dev-request`,
`/dev-explain`, or `/dev-fyi` followed by the question or instruction.

## Targets

| Target | Instructions | Skills |
| :--- | :--- | :--- |
| Codex | `~/.codex/AGENTS.md` | `~/.agents/skills`, `~/.codex/skills` |
| Claude | `~/.claude/CLAUDE.md` | `~/.claude/skills` |

## Usage

Preview an install:

```bash
bin/agentfiles install --dry-run
```

Install global instructions and skills for Codex and Claude:

```bash
bin/agentfiles install
```

Install by symlink, which keeps target skill folders pointed at this repo:

```bash
bin/agentfiles install --mode link
```

Install by copy:

```bash
bin/agentfiles install --mode copy
```

After adding `repos/example-app/instructions/` or
`repos/example-app/skills/` to this source tree, include that overlay without
touching the target repo:

```bash
bin/agentfiles install \
  --repo-overlay example-app=/path/to/example-app
```

Validate the source tree:

```bash
bin/agentfiles doctor
```

Add a new global skill skeleton:

```bash
bin/agentfiles add-skill code-review --description "Review code changes."
```

Add a repo-specific skill skeleton:

```bash
bin/agentfiles add-skill app-review --repo example-app
```

Import an existing skill folder:

```bash
bin/agentfiles add-skill code-review --from /path/to/code-review
```

Render the instruction file without installing:

```bash
bin/agentfiles render --target codex
```

## Safety

`agentfiles` writes a generated header into instruction files. On later runs it
will update files with that header, but it refuses to overwrite unmanaged files
unless `--force` is passed.

For installed skill copies, `agentfiles` writes a `.agentfiles-managed` marker.
For symlinked skills, the symlink itself is treated as managed.

`--clean` removes stale managed skill installs that are no longer present in the
selected source tree. It does not remove unmanaged directories.

