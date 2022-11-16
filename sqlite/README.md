# Elimity Insights example SQLite connector

This Python package implements an example Elimity Insights custom connector importing from a SQLite (version 3.37.0 or
higher) database. The Elimity Insights data model can be found in the [`data-model.json`](data-model.json) file.

## Usage

```console
(venv) $ elimity-insights-example-sqlite-connector --help
usage: elimity-insights-example-sqlite-connector [-h] --database DATABASE [--generate-database] --source-id SOURCE_ID --source-token SOURCE_TOKEN --url URL

Example Elimity Insights custom connector importing from a SQLite database

optional arguments:
  -h, --help            show this help message and exit
  --database DATABASE   path to the SQLite database file
  --generate-database   generate a new sample database before importing
  --source-id SOURCE_ID
                        identifier for authenticating the source in Elimity Insights
  --source-token SOURCE_TOKEN
                        token for authenticating the source in Elimity Insights
  --url URL             URL of the Elimity Insights server
```
