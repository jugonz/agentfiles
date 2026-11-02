---
name: review-loop
description: Review the specified changes, verify and fix actionable findings, and repeat until no actionable findings remain. Use for requests such as review and fix until fixed point or review fixes until clean.
---

# Review Loop

Own the review, fixes, and verification through convergence. A request to review
and fix authorizes corrections within the established requirements, not a redesign.

## Scope

Identify the exact review target from the request and conversation: uncommitted
changes, a commit, a branch diff, or just the latest round of edits. Record its
base and affected files before editing, including untracked files. Keep that
boundary throughout the loop; "latest round" does not mean the whole PR.
Read surrounding code and callers as needed without expanding the change scope.
If the target is materially ambiguous, ask before reviewing unrelated work.

## Review and fix

1. Use one independent, read-only reviewer when delegation is available. Give
   it the exact scope, established requirements, accepted tradeoffs, deliberate
   deferrals, and validation evidence. Ask it to inspect the code, return all
   concrete actionable findings, and avoid editing or further delegation. Use
   an available review skill when it fits; do not require a particular skill
   installation. If independent review is unavailable, review locally and say so.
2. Verify each finding against the current code and a reachable failure scenario.
   Fix confirmed defects with the smallest change that meets the requirements.
   Reject stale, speculative, pre-existing, or already-resolved findings with a
   brief reason. Complexity alone does not establish a correctness defect.
3. Run focused verification for the changed behavior. Add regression coverage
   when it meaningfully proves the fix. Respect session restrictions on tools
   and checks; reuse unchanged validation evidence instead of repeating broad
   suites. Distinguish observed failures from checks that were unavailable.
4. After fixes, request another review of the updated scoped diff, including
   interactions with the fixes. Carry forward finding dispositions so resolved
   or deliberately deferred issues do not restart the same debate. Continue
   until a complete pass finds no actionable defects and relevant verification
   passes. A clean first pass needs no invented changes or extra rounds.

## Boundaries and stopping

Established requirements and explicit user decisions remain authoritative.
Before introducing a new abstraction, persistence contract, architectural
change, or stronger guarantee, explain the concrete harm, why the existing
requirements are insufficient (if they are), and the smallest alternatives.
Get a decision before implementing that expansion. Continue independent,
already-authorized fixes where possible.

Do not call the work converged merely because a finding was deferred or a check
could not run. If a repeated finding cannot be resolved within scope, or a real
blocker requires user input, report the outstanding issue and exact decision
needed rather than generating more code or repeating equivalent reviews.

A review request alone does not authorize commits, amendments, pushes, merges,
or external review comments. Existing explicit authorization still applies.

Finish with the concrete fixes, verification results, and whether the final
review was clean. Name any unresolved issue or required decision. If no fixes
were needed, say so plainly.
