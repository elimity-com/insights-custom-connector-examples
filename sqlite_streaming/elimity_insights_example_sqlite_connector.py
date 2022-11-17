from argparse import ArgumentParser
from datetime import datetime
from sqlite3 import Connection, connect
from typing import Iterable, List, Optional

from elimity_insights_client import (
    AttributeAssignment,
    Client,
    Config,
    DateTime,
    DateTimeValue,
    DomainGraph,
    Entity,
    NumberValue,
    Relationship,
    StringValue,
)


def main() -> None:
    args = _parser.parse_args()
    config = Config(args.source_id, args.url, args.source_token)
    client = Client(config)
    with connect(args.database, isolation_level=None) as connection:
        connection.execute("BEGIN")
        entities = _entities(connection)
        relationships = _relationships(connection)
        graph = DomainGraph(entities, relationships)
        client.reload_domain_graph(graph)


def _entities(connection: Connection) -> Iterable[Entity]:
    user_sql = """
        SELECT display_name, first_name, CAST(id AS TEXT), last_logon, last_name
        FROM users
    """
    for display_name, first_name, id, last_logon, last_name in connection.execute(
        user_sql
    ):
        assignments = _user_attribute_assignments(first_name, last_logon, last_name)
        yield Entity(assignments, id, display_name, "user")
    role_sql = """
        SELECT CAST(id AS TEXT), name, security_level
        FROM roles
    """
    for id, name, security_level in connection.execute(role_sql):
        security_level_value = NumberValue(security_level)
        security_level_assignment = AttributeAssignment(
            "securityLevel", security_level_value
        )
        assignments = [security_level_assignment]
        yield Entity(assignments, id, name, "role")


def _relationships(connection: Connection) -> Iterable[Relationship]:
    sql = """
        SELECT CAST(user_id AS TEXT), CAST(role_id AS TEXT)
        FROM user_roles
    """
    for user_id, role_id in connection.execute(sql):
        assignments: List[AttributeAssignment] = []
        yield Relationship(assignments, user_id, "user", role_id, "role")


def _user_attribute_assignments(
    first_name: str, last_logon: Optional[int], last_name: str
) -> Iterable[AttributeAssignment]:
    yield _string_attribute_assignment("firstName", first_name)
    yield _string_attribute_assignment("lastName", last_name)
    if last_logon is not None:
        last_logon_datetime = datetime.utcfromtimestamp(last_logon)
        last_logon_time = DateTime(
            last_logon_datetime.year,
            last_logon_datetime.month,
            last_logon_datetime.day,
            last_logon_datetime.hour,
            last_logon_datetime.minute,
            last_logon_datetime.second,
        )
        last_logon_value = DateTimeValue(last_logon_time)
        yield AttributeAssignment("lastLogon", last_logon_value)


def _add_flag(help: str, name: str, type_int: bool = False) -> None:
    _parser.add_argument(name, help=help, required=True, type=int if type_int else str)


def _string_attribute_assignment(
    attribute_type_id: str, raw_value: str
) -> AttributeAssignment:
    processed_value = StringValue(raw_value)
    return AttributeAssignment(attribute_type_id, processed_value)


_parser = ArgumentParser(
    description="Example Elimity Insights custom connector importing from a SQLite database"
)
_add_flag("path to the SQLite database file", "--database")
_add_flag(
    "identifier for authenticating the source in Elimity Insights", "--source-id", True
)
_add_flag("token for authenticating the source in Elimity Insights", "--source-token")
_add_flag("URL of the Elimity Insights server", "--url")
