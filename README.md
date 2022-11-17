# Elimity Insights custom connector examples

These Python packages implement example Elimity Insights custom connectors importing from different sources.

## Installation

Installing the connectors requires Python version 3.9 or higher. Since these are just example scripts, they are not
publicly available on PyPI. Local installation in a virtual environment is recommended for trying out the connectors:

```console
$ python -m venv venv
$ source venv/bin/activate
(venv) $ pip install <connector-directory>
```

## Usage

After installing, a CLI for the chosen connector should be available in the virtual environment:

```console
(venv) $ elimity-insights-example-<connector-name>-connector --help
```

## Development

Contributing to these connectors requires [Poetry](https://python-poetry.org/). The examples below show how to perform
some common development tasks, with the working directory set for a specific connector.

### Installing the development environment

```console
$ poetry install
```

### Formatting

```console
$ poetry run black .
```

### Type-checking

```console
$ poetry run mypy .
```
