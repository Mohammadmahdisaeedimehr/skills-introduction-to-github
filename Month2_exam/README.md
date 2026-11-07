# Month 2 Exam

This is a closed-book implementation exercise. Do not use AI to write the solution.

## Goal

Build a very small database-backed Python feature from scratch and demonstrate that you understand the architecture.

## Deliverables

Create your work inside this folder only:

- a small SQL schema
- exactly 5 useful SQL queries
- a Python database connection layer
- tests
- a short README describing how to run it

You choose the small domain yourself.

## Minimum requirements

### Schema

Use 2 or 3 related tables.

Include:

- primary keys
- at least one foreign key
- at least one NOT NULL constraint
- at least one meaningful CHECK or UNIQUE constraint

### Five queries

Write exactly five named queries. Together they should demonstrate that you can retrieve and summarize data, not just insert rows.

### Python connection

Connect from Python to PostgreSQL using configuration from the environment. Do not hard-code credentials.

### Tests

Test both a successful path and at least one failure/constraint path.

Tests must be repeatable and must not depend on manually editing production data.

## Exam rules

- Do not copy code from the existing project.
- Do not ask AI to generate the schema, queries, connection code, or tests.
- You may use your own notes from the previous month.
- Environment/tooling help is allowed if the problem is unrelated to the implementation logic.

## Definition of done

The exam is complete when:

1. the schema can be created cleanly;
2. sample data can be inserted;
3. all five queries run;
4. Python can connect and execute at least one query;
5. tests pass;
6. no password or secret is committed;
7. you can explain the architecture without reading the code.
