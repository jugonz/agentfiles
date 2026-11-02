---
name: do-ticket
description: Implement a ticket strictly to its stated acceptance criteria, with an explicit checkpoint before expanding persistence, contracts, or architecture.
---

# Do Ticket

Treat the ticket's description, acceptance criteria, and explicitly agreed
decisions as the implementation boundary. Do not interpret an open technical
choice as permission to broaden the product or architecture.

Before editing, state the concrete acceptance criteria being implemented and
identify any known work deliberately deferred to another ticket.

Continue implementation and verification until the ticket reaches a fixed
point: all stated acceptance criteria are delivered and verified, or a
concrete blocker requires user input. Do not report a partial status as the
final answer while an executable implementation or focused verification step
remains.

Before sending a final response, enumerate every ticket acceptance criterion
and name the implementation and focused verification that satisfies it. If any
criterion cannot be marked done, continue working. A partial final response is
permitted only when a concrete blocker requires user input; name the blocked
criterion, the dependency, and the exact decision or external change needed.

## Scope Deltas

Stop and ask for a decision before adding a new persistence model or backend,
storage bucket or object class, service dependency, queue, workflow contract,
or externally visible API/proto surface that the ticket does not require.

Present the need, smallest viable alternatives, operational consequences, and
what would change in the current ticket. Do not implement the expansion until
the user explicitly chooses it.

Fix defects only when they are necessary to meet the ticket's acceptance
criteria. Report adjacent risks separately and leave future-ticket behavior
for its planned work.

Do not stop after setup, scaffolding, a partial edit, or an avoidable broad
verification failure when ticket acceptance criteria remain and another
implementation or focused verification step can proceed. Only close with a
partial status for a real blocker or explicit checkpoint request.

At completion, distinguish delivered criteria from deferred criteria and name
any decision that prevented further work.
