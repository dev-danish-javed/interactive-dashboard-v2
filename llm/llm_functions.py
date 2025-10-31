from google.genai.types import FunctionDeclaration, Schema, Type

from utils.db_utils.oracle_utils import execute_query

execute_sql_query_function_declaration = FunctionDeclaration(
    name="execute_query",
    description="Schedules a meeting with specified attendees at a given time and date.",
    parameters=Schema(
        type=Type.OBJECT,
        properties={
            "query": Schema(type=Type.STRING, description="Query to execute in oracle db.")
        },
        required=["query"]
    )
)

# --- Map function names to Python functions ---
LLM_FUNCTION_MAP = {
    "execute_query": lambda **args: execute_query(**args)
}