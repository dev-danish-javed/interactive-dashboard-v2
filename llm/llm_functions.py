from google.genai.types import FunctionDeclaration, Schema, Type
from numpy import histogram

from utils.chart_utils import area_chart, bar_chart, box_plot, bubble_chart, donut_chart, grouped_bar_chart, heatmap, line_chart, multi_line_chart, pie_chart, radar_chart, scatter_chart, violin_plot, waterfall_chart
from utils.db_utils.oracle_utils import execute_query

execute_sql_query_function_declaration = FunctionDeclaration(
    name="execute_query",
    description="Executes a query in the oracle db and returns the result",
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



# --- Function Declarations ---
bar_chart_function = FunctionDeclaration(
    name="bar_chart",
    description="Renders a bar chart from data and returns HTML <img> string.",
    parameters=Schema(
        type=Type.OBJECT,
        properties={
            "data": Schema(type=Type.ARRAY, description="List of numeric values."),
            "labels": Schema(type=Type.ARRAY, description="Labels for each bar."),
            "title": Schema(type=Type.STRING, description="Chart title."),
            "xlabel": Schema(type=Type.STRING, description="X-axis label."),
            "ylabel": Schema(type=Type.STRING, description="Y-axis label.")
        },
        required=["data", "labels"]
    )
)

grouped_bar_chart_function = FunctionDeclaration(
    name="grouped_bar_chart",
    description="Renders a grouped bar chart and returns HTML <img> string.",
    parameters=Schema(
        type=Type.OBJECT,
        properties={
            "data_groups": Schema(type=Type.ARRAY, description="List of value lists, one per group."),
            "labels": Schema(type=Type.ARRAY, description="Category labels."),
            "group_names": Schema(type=Type.ARRAY, description="Names of each group.")
        },
        required=["data_groups", "labels", "group_names"]
    )
)

line_chart_function = FunctionDeclaration(
    name="line_chart",
    description="Renders a line chart and returns HTML <img> string.",
    parameters=Schema(
        type=Type.OBJECT,
        properties={
            "x": Schema(type=Type.ARRAY, description="X-axis values."),
            "y": Schema(type=Type.ARRAY, description="Y-axis values."),
            "title": Schema(type=Type.STRING),
            "xlabel": Schema(type=Type.STRING),
            "ylabel": Schema(type=Type.STRING)
        },
        required=["x", "y"]
    )
)

multi_line_chart_function = FunctionDeclaration(
    name="multi_line_chart",
    description="Renders multiple line series on a single chart and returns HTML.",
    parameters=Schema(
        type=Type.OBJECT,
        properties={
            "x": Schema(type=Type.ARRAY),
            "y_series": Schema(type=Type.ARRAY, description="List of Y-series data arrays."),
            "labels": Schema(type=Type.ARRAY, description="Names for each series.")
        },
        required=["x", "y_series", "labels"]
    )
)

area_chart_function = FunctionDeclaration(
    name="area_chart",
    description="Renders an area chart and returns HTML.",
    parameters=Schema(
        type=Type.OBJECT,
        properties={
            "x": Schema(type=Type.ARRAY),
            "y": Schema(type=Type.ARRAY),
            "title": Schema(type=Type.STRING),
            "xlabel": Schema(type=Type.STRING),
            "ylabel": Schema(type=Type.STRING)
        },
        required=["x", "y"]
    )
)

pie_chart_function = FunctionDeclaration(
    name="pie_chart",
    description="Renders a pie chart and returns HTML.",
    parameters=Schema(
        type=Type.OBJECT,
        properties={
            "data": Schema(type=Type.ARRAY),
            "labels": Schema(type=Type.ARRAY),
            "title": Schema(type=Type.STRING)
        },
        required=["data", "labels"]
    )
)

donut_chart_function = FunctionDeclaration(
    name="donut_chart",
    description="Renders a donut chart and returns HTML.",
    parameters=Schema(
        type=Type.OBJECT,
        properties={
            "data": Schema(type=Type.ARRAY),
            "labels": Schema(type=Type.ARRAY),
            "title": Schema(type=Type.STRING)
        },
        required=["data", "labels"]
    )
)

scatter_chart_function = FunctionDeclaration(
    name="scatter_chart",
    description="Renders a scatter plot and returns HTML.",
    parameters=Schema(
        type=Type.OBJECT,
        properties={
            "x": Schema(type=Type.ARRAY),
            "y": Schema(type=Type.ARRAY),
            "title": Schema(type=Type.STRING),
            "xlabel": Schema(type=Type.STRING),
            "ylabel": Schema(type=Type.STRING)
        },
        required=["x", "y"]
    )
)

bubble_chart_function = FunctionDeclaration(
    name="bubble_chart",
    description="Renders a bubble chart and returns HTML.",
    parameters=Schema(
        type=Type.OBJECT,
        properties={
            "x": Schema(type=Type.ARRAY),
            "y": Schema(type=Type.ARRAY),
            "sizes": Schema(type=Type.ARRAY, description="Bubble sizes."),
            "title": Schema(type=Type.STRING)
        },
        required=["x", "y", "sizes"]
    )
)

histogram_function = FunctionDeclaration(
    name="histogram",
    description="Renders a histogram and returns HTML.",
    parameters=Schema(
        type=Type.OBJECT,
        properties={
            "data": Schema(type=Type.ARRAY),
            "bins": Schema(type=Type.INTEGER),
            "title": Schema(type=Type.STRING)
        },
        required=["data"]
    )
)

box_plot_function = FunctionDeclaration(
    name="box_plot",
    description="Renders a box plot and returns HTML.",
    parameters=Schema(
        type=Type.OBJECT,
        properties={
            "data": Schema(type=Type.ARRAY),
            "labels": Schema(type=Type.ARRAY),
            "title": Schema(type=Type.STRING)
        },
        required=["data"]
    )
)

violin_plot_function = FunctionDeclaration(
    name="violin_plot",
    description="Renders a violin plot and returns HTML.",
    parameters=Schema(
        type=Type.OBJECT,
        properties={
            "data": Schema(type=Type.ARRAY),
            "labels": Schema(type=Type.ARRAY),
            "title": Schema(type=Type.STRING)
        },
        required=["data"]
    )
)

heatmap_function = FunctionDeclaration(
    name="heatmap",
    description="Renders a heatmap and returns HTML.",
    parameters=Schema(
        type=Type.OBJECT,
        properties={
            "matrix": Schema(type=Type.ARRAY),
            "x_labels": Schema(type=Type.ARRAY),
            "y_labels": Schema(type=Type.ARRAY),
            "title": Schema(type=Type.STRING)
        },
        required=["matrix", "x_labels", "y_labels"]
    )
)

radar_chart_function = FunctionDeclaration(
    name="radar_chart",
    description="Renders a radar chart and returns HTML.",
    parameters=Schema(
        type=Type.OBJECT,
        properties={
            "categories": Schema(type=Type.ARRAY),
            "values": Schema(type=Type.ARRAY),
            "title": Schema(type=Type.STRING)
        },
        required=["categories", "values"]
    )
)

waterfall_chart_function = FunctionDeclaration(
    name="waterfall_chart",
    description="Renders a waterfall chart and returns HTML.",
    parameters=Schema(
        type=Type.OBJECT,
        properties={
            "values": Schema(type=Type.ARRAY),
            "labels": Schema(type=Type.ARRAY),
            "title": Schema(type=Type.STRING)
        },
        required=["values", "labels"]
    )
)

# --- Function Map ---
LLM_CHARTS_FUNCTION_MAP = {
    "bar_chart": lambda **args: bar_chart(**args),
    "grouped_bar_chart": lambda **args: grouped_bar_chart(**args),
    "line_chart": lambda **args: line_chart(**args),
    "multi_line_chart": lambda **args: multi_line_chart(**args),
    "area_chart": lambda **args: area_chart(**args),
    "pie_chart": lambda **args: pie_chart(**args),
    "donut_chart": lambda **args: donut_chart(**args),
    "scatter_chart": lambda **args: scatter_chart(**args),
    "bubble_chart": lambda **args: bubble_chart(**args),
    "histogram": lambda **args: histogram(**args),
    "box_plot": lambda **args: box_plot(**args),
    "violin_plot": lambda **args: violin_plot(**args),
    "heatmap": lambda **args: heatmap(**args),
    "radar_chart": lambda **args: radar_chart(**args),
    "waterfall_chart": lambda **args: waterfall_chart(**args)
}
