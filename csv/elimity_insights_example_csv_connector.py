from argparse import ArgumentParser, Namespace
from csv import DictReader
from datetime import datetime
from typing import (
    Annotated,
    Iterable,
    TypeVar,
    Callable,
    Literal,
    Union,
)

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
    Value,
)
from pydantic import BaseModel, parse_obj_as, BeforeValidator


def main() -> None:
    args = _parser.parse_args()
    config = Config(args.source_id, args.url, args.source_token)
    client = Client(config)
    entities = _parse_rows(_parse_entity, args)
    relationships = _parse_rows(_parse_relationship, args)
    graph = DomainGraph(entities, relationships)
    client.reload_domain_graph(graph)


def _validate_datetime(value: object) -> object:
    return datetime.min if value == "" else value


_validator = BeforeValidator(_validate_datetime)
_T = TypeVar("_T")


class _Role(BaseModel):
    role_id: str
    role_name: str
    role_security_level: float
    type: Literal["role"]


class _User(BaseModel):
    type: Literal["user"]
    user_display_name: str
    user_first_name: str
    user_id: str
    user_last_logon: Annotated[datetime, _validator]
    user_last_name: str


class _UserRole(BaseModel):
    type: Literal["user_role"]
    user_role_rid: str
    user_role_uid: str


_Row = Union[_Role, _User, _UserRole]


def _make_attribute_assignments(
    assignments: dict[str, object]
) -> Iterable[AttributeAssignment]:
    for attribute_type_id, value in assignments.items():
        for val in _make_value(value):
            yield AttributeAssignment(attribute_type_id, val)


def _make_entity(
    assignments: dict[str, object], id: str, name: str, type: str
) -> Entity:
    ass = _make_attribute_assignments(assignments)
    return Entity(ass, id, name, type)


def _make_value(value: object) -> Iterable[Value]:
    if isinstance(value, datetime) and value != datetime.min:
        time = DateTime(
            value.year,
            value.month,
            value.day,
            value.hour,
            value.minute,
            value.second,
        )
        yield DateTimeValue(time)

    if isinstance(value, float):
        yield NumberValue(value)

    if isinstance(value, str):
        yield StringValue(value)


def _parse_entity(row: _Row) -> Iterable[Entity]:
    if isinstance(row, _Role):
        role_assignments: dict[str, object] = {"securityLevel": row.role_security_level}
        yield _make_entity(role_assignments, row.role_id, row.role_name, "role")

    if isinstance(row, _User):
        user_assignments: dict[str, object] = {
            "firstName": row.user_first_name,
            "lastLogon": row.user_last_logon,
            "lastName": row.user_last_name,
        }
        yield _make_entity(user_assignments, row.user_id, row.user_display_name, "user")


def _parse_relationship(row: _Row) -> Iterable[Relationship]:
    if isinstance(row, _UserRole):
        assignments: list[AttributeAssignment] = []
        yield Relationship(
            assignments, row.user_role_uid, "user", row.user_role_rid, "role"
        )


def _parse_rows(
    parse_function: Callable[[_Row], Iterable[_T]], namespace: Namespace
) -> Iterable[_T]:
    with open(namespace.file, newline="") as file:
        reader = DictReader(file)
        for row in reader:
            r = parse_obj_as(_Row, row)
            yield from parse_function(r)


def _add_flag(help: str, name: str, type_int: bool = False) -> None:
    _parser.add_argument(name, help=help, required=True, type=int if type_int else str)


_parser = ArgumentParser(
    description="Example Elimity Insights custom connector importing from a CSV file"
)
_add_flag("path to the CSV file", "--file")
_add_flag(
    "identifier for authenticating the source in Elimity Insights", "--source-id", True
)
_add_flag("token for authenticating the source in Elimity Insights", "--source-token")
_add_flag("URL of the Elimity Insights server", "--url")
