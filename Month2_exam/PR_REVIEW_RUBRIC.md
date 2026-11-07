# Hypothetical PR review rubric

A separate practice PR will be provided after your implementation.

Review it as if it were going into production.

Check at least:

- correctness
- data integrity
- SQL safety
- secret/config handling
- transaction behavior
- test quality
- naming/readability
- unnecessary complexity
- backward compatibility
- whether the PR should be approved, commented on, or blocked

For every blocking issue, explain the concrete failure mode rather than only saying that the code is "bad".
