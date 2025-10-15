import logging

from sqlalchemy import create_engine, inspect, text

from configurations.configs import get_db_uri

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger(__name__)

# Format into readable text for embeddings
def schema_to_text(schema_dict):
    """Converts db scneba text to normal string"""
    text_parts = []
    for table, info in schema_dict.items():
        text_parts.append(f"Table: {table}")
        for col in info["columns"]:
            text_parts.append(
                f"  - Column '{col['name']}' ({col['type']}), "
                f"{'NULL allowed' if col['nullable'] else 'NOT NULL'}"
                + (f", default: {col['default']}" if col['default'] else "")
            )
        if info["primary_keys"]:
            text_parts.append(f"  Primary Keys: {', '.join(info['primary_keys'])}")
        text_parts.append('\n')
        for fk in info["foreign_keys"]:
            text_parts.append(
                f"  Foreign Key: {fk['column']} → {fk['referred_table']}({fk['referred_columns']})"
            )
        if info["indexes"]:
            for idx in info["indexes"]:
                text_parts.append(
                    f"  Index: {idx['name']} on {idx['columns']} "
                    f"{'(unique)' if idx['unique'] else ''}"
                )
        text_parts.append("")
    return "\n".join(text_parts)

def get_db_schema():
    """Extracts db schema"""
    schema = {}
    engine = create_engine(get_db_uri())
    insp = inspect(engine)
    # pull data from db
    for table_name in insp.get_table_names():
        logger.info(f"Fetching table details for table: {table_name}")
        table_info = {"columns": [], "primary_keys": [], "foreign_keys": [], "indexes": []}

        # Columns info
        for col in insp.get_columns(table_name):
            table_info["columns"].append({
                "name": col["name"],
                "type": str(col["type"]),
                "nullable": col["nullable"],
                "default": col.get("default")
            })

        # Primary keys
        table_info["primary_keys"] = insp.get_pk_constraint(table_name).get("constrained_columns", [])

        # Foreign keys
        fks = insp.get_foreign_keys(table_name)
        for fk in fks:
            table_info["foreign_keys"].append({
                "column": fk["constrained_columns"],
                "referred_table": fk["referred_table"],
                "referred_columns": fk["referred_columns"]
            })

        # Indexes
        for idx in insp.get_indexes(table_name):
            table_info["indexes"].append({
                "name": idx["name"],
                "columns": idx["column_names"],
                "unique": idx.get("unique", False)
            })

        schema[table_name] = table_info
    return schema

def execute_query(query: str):
    """Executes the db query and returns the results"""
    engine = create_engine(get_db_uri())
    with engine.connect() as conn:
        result = conn.execute(text(query))
        rows = result.fetchall()
    return rows