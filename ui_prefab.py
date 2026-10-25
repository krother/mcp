from prefab_ui.components import DataTable, DataTableColumn
from fastmcp import FastMCP

mcp = FastMCP("Directory")


@mcp.tool(app=True)
def team_directory() -> DataTable:
    """Browse the team directory."""
    employees = [
        {"name": "Alice Chen", "role": "Staff Engineer", "dept": "Platform"},
        {"name": "Bob Martinez", "role": "Lead Designer", "dept": "Design"},
        {"name": "Carol Johnson", "role": "Senior Engineer", "dept": "Platform"},
        {"name": "David Kim", "role": "Product Manager", "dept": "Product"},
        {"name": "Eva Mueller", "role": "Engineer", "dept": "Platform"},
        {"name": "Frank Lee", "role": "Data Scientist", "dept": "ML"},
        {"name": "Grace Park", "role": "Eng Manager", "dept": "Platform"},
    ]

    return DataTable(
        columns=[
            DataTableColumn(key="name", header="Name", sortable=True),
            DataTableColumn(key="role", header="Role", sortable=True),
            DataTableColumn(key="dept", header="Dept", sortable=True),
        ],
        rows=employees,
        search=True,
    )


if __name__ == "__main__":
    mcp.run()
