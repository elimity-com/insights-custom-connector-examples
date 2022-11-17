# Elimity Insights example SQLite connector

This Python package implements a basic connector importing data from a SQLite (version 3.37.0 or
higher) database. 

Note: For larger datasets we recommend avoiding loading all data into memory at once. 
[This](../sqlite_streaming) example connector extends the basic example with streaming to avoid this.

## Example data

This example script expects the database to contain users and roles, both with metadata.

You can use the following query to initialize an example database:

```sqlite
BEGIN;

CREATE TABLE users (
    display_name TEXT NOT NULL,
    first_name TEXT NOT NULL,
    id INTEGER PRIMARY KEY,
    last_name TEXT NOT NULL,
    last_logon INTEGER
) STRICT;

INSERT INTO users (display_name, first_name, last_name, last_logon)
VALUES
    ('dduck', 'Donald', 'Duck', 1668603363),
    ('mmouse', 'Mickey', 'Mouse', NULL);
CREATE TABLE roles (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    security_level INTEGER NOT NULL
) STRICT;

INSERT INTO roles (name, security_level)
VALUES
    ('Reader', 0),
    ('Writer', 1);

CREATE TABLE user_roles (
    id INTEGER PRIMARY KEY,
    role_id INTEGER NOT NULL REFERENCES roles (id),
    user_id INTEGER NOT NULL REFERENCES users (id),
    UNIQUE (role_id, user_id)
) STRICT;

INSERT INTO user_roles (role_id, user_id)
VALUES
    (1, 1),
    (1, 2),
    (2, 2);

COMMIT
```

## Data model for Elimity Insights

The data model for a custom source in Elimity Insights can be found in the [`data-model.json`](data-model.json) file.