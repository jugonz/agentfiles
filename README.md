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
    skills/
      my-skill/
        SKILL.md
        scripts/
        references/
  repos/
    baton-claude-enterprise/
      instructions/
        00-guidance.md
      skills/
        claude-enterprise-review/
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

Include a repo overlay without touching that repo:

```bash
bin/agentfiles install \
  --repo-overlay baton-claude-enterprise=/Users/jugonzalez/Documents/repos/baton-claude-enterprise
```

Validate the source tree:

```bash
bin/agentfiles doctor
```

Add a new global skill skeleton:

```bash
bin/agentfiles add-skill connector-review --description "Review Baton connector access models."
```

Add a repo-specific skill skeleton:

```bash
bin/agentfiles add-skill claude-enterprise-review --repo baton-claude-enterprise
```

Import an existing skill folder:

```bash
bin/agentfiles add-skill connector-review --from /path/to/connector-review
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

