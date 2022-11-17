from datetime import datetime
from sqlite3 import connect
from typing import List

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

# Configuration
# Note: If you want, you can turn these variables into command line inputs using [https://docs.python.org/3/library/argparse.html](ArgParse).
DATABASE = "mydb.sqlite3"
ELIMITY_INSIGHTS_URL = "https://example.elimity.com"
ELIMITY_INSIGHTS_SOURCE_ID = "1"
ELIMITY_INSIGHTS_SOURCE_API_TOKEN = "34kj328ukj291ukjsdkj394ukjdf"


def main() -> None:
    config = Config(ELIMITY_INSIGHTS_SOURCE_ID, ELIMITY_INSIGHTS_URL, ELIMITY_INSIGHTS_SOURCE_API_TOKEN)
    client = Client(config)
    with connect(DATABASE, isolation_level=None) as connection:

        connection.executescript("BEGIN")

        # To load the data of the database into Elimity Insights, we have to construct a "domain graph".
        # Essentially, this domain graph contains the list of entities and their attribute assignments,
        # and the relationships between these entities.
        entities: List[Entity] = []
        relationships: List[Relationship] = []

        # Step 1. Turn the users into entities with attribute assignments.
        for display_name, first_name, id, last_logon, last_name in connection.execute("""
            SELECT display_name, first_name, CAST(id AS TEXT), last_logon, last_name
            FROM users
        """):
            assignments: List[AttributeAssignment] = [
                AttributeAssignment("firstName", StringValue(first_name)),
                AttributeAssignment("lastName", StringValue(last_name))
            ]
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
                assignments.append(AttributeAssignment("lastLogon", last_logon_value))
            entities.append(Entity(assignments, id, display_name, "user"))

        # Step 2. Turn the roles into entities with attribute assignments
        for id, name, security_level in connection.execute("""
            SELECT CAST(id AS TEXT), name, security_level
            FROM roles
        """):
            assignments: List[AttributeAssignment] = [
                AttributeAssignment("securityLevel", NumberValue(security_level))
            ]
            entities.append(Entity(assignments, id, name, "role"))

        # Step 3. Turn the relationships table into relationships
        for user_id, role_id in connection.execute("""
            SELECT CAST(user_id AS TEXT), CAST(role_id AS TEXT)
            FROM user_roles
        """):
            # Relationships can be assigned attributes as well, but this example does not include that.
            assignments: List[AttributeAssignment] = []
            entities.append(Relationship(assignments, user_id, "user", role_id, "role"))

        # Step 4. Upload the entities and relationships as a domain graph
        graph = DomainGraph(entities, relationships)
        client.reload_domain_graph(graph)