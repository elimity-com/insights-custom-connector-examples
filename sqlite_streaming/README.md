# Elimity Insights example SQLite connector with data streaming

This Python package implements an example connector importing data from a SQLite (version 3.37.0 or
higher) database. 

This example extends [../sqlite_basic](the basic example) with data streaming
to avoid that all data is loaded into memory at once, which is useful for large datasets.

In addition, this example illustrates how to receive input parameters from the command line
using [https://docs.python.org/3/library/argparse.html](ArgParse).

## Usage

```console
(venv) $ elimity-insights-example-sqlite-connector --help
usage: elimity-insights-example-sqlite-connector [-h] --database DATABASE [--generate-database] --source-id SOURCE_ID --source-token SOURCE_TOKEN --url URL

Example Elimity Insights custom connector importing from a SQLite database

optional arguments:
  -h, --help            show this help message and exit
  --database DATABASE   path to the SQLite database file
  --source-id SOURCE_ID
                        identifier for authenticating the source in Elimity Insights
  --source-token SOURCE_TOKEN
                        token for authenticating the source in Elimity Insights
  --url URL             URL of the Elimity Insights server
```

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
    (2, 2)
```

## Data model for Elimity Insights

The data model for a custom source in Elimity Insights can be found in the [`data-model.json`](data-model.json) file.