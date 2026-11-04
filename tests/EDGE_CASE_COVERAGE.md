# Manual edge-case coverage

## normalize_status

- lowercase valid input: `inside`
- leading/trailing spaces: `" INSIDE "`
- mixed case: `Outside`
- trailing newline: `" review\n"`
- empty string
- whitespace-only string
- non-string values: `None`, integer, float, list, dict

## database

- all valid statuses: `inside`, `outside`, `review`
- invalid statuses: empty, unknown, uppercase variant, null
- confidence below 0
- confidence above 1
- confidence lower boundary: 0.0
- confidence middle value: 0.5
- confidence upper boundary: 1.0
- fresh database fixture for every test

The DB fixture uses an in-memory SQLite database so tests do not modify development or production data.
