## Working Agreements

- Treat `~/.agents/skills` as the canonical global skill source for shared local
  skills. Keep `~/.claude/skills` pointed at the same content when possible.
- Do not revert or "correct" fields in external systems after an update unless
  you explicitly changed that field or can prove the tool changed it. If another
  actor may have changed it concurrently, ask before changing it.
- Work within the established design and ticket requirements. Code-review
  suggestions, complexity-based approval deferrals, and possible interleavings
  do not themselves establish defects or authorize stronger guarantees.
- Before expanding scope, explain the concrete user-visible failure, why the
  existing requirements do not already address it, and the smallest viable fix.
  Discuss and obtain explicit approval before introducing new abstractions,
  persistence contracts, or stronger concurrency/ownership guarantees.
- For human-supervised workflows, distinguish safe, visible, recoverable
  in-flight work from actual harm. Do not build an ironclad guarantee system
  when the agreed goal is safe assistance to human operators. Human domain
  review is an acceptable outcome; do not add machinery to force agent approval.
- Minimize implementation churn and token/tool use to what serves the user's
  software goals. More code, tests, or review loops are not progress by themselves.
  Lesson: during connector rollout work, an agent overreacted to a complexity
  deferral by building an unapproved transaction/ownership redesign. Surface
  concerns for discussion instead of silently changing the requirements.
