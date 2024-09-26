# Elimity Insights example CSV connector

This Python package implements an example connector importing data from a CSV file.

## Usage

```console
(venv) $ elimity-insights-example-csv-connector --help
usage: elimity-insights-example-csv-connector [-h] --file FILE --source-id SOURCE_ID --source-token SOURCE_TOKEN --url URL

Example Elimity Insights custom connector importing from a CSV file

optional arguments:
  -h, --help            show this help message and exit
  --file FILE           path to the CSV file
  --source-id SOURCE_ID
                        identifier for authenticating the source in Elimity Insights
  --source-token SOURCE_TOKEN
                        token for authenticating the source in Elimity Insights
  --url URL             URL of the Elimity Insights server
```

## Example data

This example script expects the CSV file to contain users and roles, both with metadata.
You can use the [`example.csv`](example.csv) file as a starting point.

## Data model for Elimity Insights

The data model for a custom source in Elimity Insights can be found in the [`data-model.json`](data-model.json) file.