from sqlalchemy import create_engine, inspect, text

from configurations.configs import get_db_uri

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


def get_packages_source_text() -> str:
    """Fetches PL/SQL package and package body source from current user and returns as a single text blob."""
    engine = create_engine(get_db_uri())
    try:
        with engine.connect() as conn:
            # USER_SOURCE works for the connected schema; avoids extra grants needed for ALL_SOURCE/DBA_SOURCE
            result = conn.execute(text(
                """
                SELECT NAME, TYPE, LINE, TEXT
                FROM USER_SOURCE
                WHERE TYPE IN ('PACKAGE', 'PACKAGE BODY')
                ORDER BY NAME, TYPE, LINE
                """
            ))
            packages = {}
            for name, typ, line, txt in result:
                key = (name, typ)
                if key not in packages:
                    packages[key] = []
                packages[key].append(txt or "")

            parts = []
            for (name, typ), lines in packages.items():
                parts.append(f"-- {typ}: {name}")
                # USER_SOURCE returns one row per line; join with newlines to preserve formatting
                parts.append("\n".join(lines))
                parts.append("\n")
            return "\n".join(parts)
    except Exception as e:
        return ""