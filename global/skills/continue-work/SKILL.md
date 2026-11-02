---
name: continue-work
description: Continue an active implementation or plan step and close with an explicit account of completed work, remaining scope, stopping reason, and next action. Use for requests such as "continue work", "continue the plan", or "ct".
---

# Continue Work

Continue the active task rather than merely reporting progress. Read the current
workspace, prior plan, and recent task context to identify the next executable
piece of work. Implement and verify it unless the user has asked only for
planning, status, or a decision.

Continue implementation and verification until the named step reaches a fixed
point: all acceptance criteria are delivered and verified, or a concrete
blocker requires user input. Do not report a partial status as the final answer
while an executable implementation or focused verification step remains.

Before sending a final response, enumerate every acceptance criterion and name
the implementation and focused verification that satisfies it. If any criterion
cannot be marked done, continue working. A partial final response is permitted
only when a concrete blocker requires user input; name the blocked criterion,
the dependency, and the exact decision or external change needed.

## Scope Boundary

When continuing a ticket or larger issue, retain its stated acceptance criteria
and explicitly agreed decisions as the scope boundary. Before adding a new
persistence model or backend, storage bucket or object class, service
dependency, queue, workflow contract, or externally visible API/proto surface
that is not required by the active step, stop and present the need, smallest
viable alternatives, and operational consequences for a user decision.

Do not use continuation as permission to pull future-ticket behavior into the
current work. Fix adjacent defects only when required for the active step's
acceptance criteria; otherwise report them as deferred work.

## Stopping Boundary

Do not stop at an arbitrary checkpoint. Stop only when one of these is true:

- The requested plan step is complete and verified.
- A real dependency, user decision, approval, or external-state change prevents
  meaningful progress.
- The user requested a checkpoint, a plan, or a status-only response.

An unsuccessful broad build, test, lint, or generation command does not end
the loop when an independent implementation, inspection, or focused
verification step remains available. Fix the relevant failure or continue
through another executable step; do not send a final partial-status response.

At the end, make the boundary unmistakable. Do not write only "started" or
describe the implemented portion without naming the remainder.

State, in this order when relevant:

1. **Status:** whether the named plan step is complete, partially complete, or
   blocked.
2. **Completed:** concrete behavior or artifacts delivered and verification run.
3. **Not completed:** the remaining acceptance criteria or implementation work.
4. **Why stopped:** the exact completion condition or blocker; identify any
   decision as a decision rather than presenting it as incidental context.
5. **Next:** the single most useful next action, including who must act when it
   is not the agent.

For a partial implementation, distinguish deliberately deferred work from work
that was discovered but is necessary for correctness. If a prior design choice
is revisited, say whether it is germane to the current stopping point and what
would change based on the answer.

Treat `ct` in ordinary user text as shorthand for this skill. Explicit skill
invocation uses `continue-work`; the canonical skill name remains
`continue-work`.
