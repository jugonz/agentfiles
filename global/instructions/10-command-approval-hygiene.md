## Command Approval Hygiene

For every non-destructive command requiring escalation, attach the shortest safe
reusable `prefix_rule` at the executable/subcommand boundary.

Do not include variable file paths, Bazel labels, package paths, PIDs, or test
names in the prefix.

Before requesting approval, state the reusable prefix being requested. If shell
composition, environment wrappers, redirection, or destructive behavior makes a
reusable rule unsafe, explain why and request the narrowest exact approval.
