from typing import List, Optional
from django.db.migrations.operations.base import Operation


class CreateView(Operation):
    class Join:
        """Represents a SQL JOIN clause."""

        def __init__(self, db_table: str, on_conditions: List[str]) -> None:
            self.db_table = db_table
            self.on_conditions = on_conditions

        def __str__(self):
            return f"JOIN {self.db_table} ON " + " AND ".join(self.on_conditions)

    reversible = True

    def __init__(
        self,
        db_table: str,
        select: List[str],
        from_table: str,
        join: Optional[List[Join]] = None,
        where: Optional[List[str]] = None,
        order_by: Optional[List[str]] = None,
    ):
        """
        Initialize the CreateView operation.

        Args:
            db_table: Name of the view to create.
            select: List of fields to include in the SELECT statement.
            from_table: The base table for the view.
            join: A list of Join objects representing JOIN clauses.
            where: A list of WHERE conditions.
        """
        self.db_table = db_table
        self.select = ', '.join(select)
        self.from_table = from_table
        self.join = "\n".join(map(str, join)) if join else ""
        self.where = f'WHERE {" AND ".join(where)}' if where else ""
        self.order_by = f'ORDER BY {", ".join(order_by)}' if order_by else ""

    def state_forwards(self, app_label, state):
        # This operation doesn't affect Django's model state.
        pass

    def database_forwards(self, app_label, schema_editor, from_state, to_state):
        """Generate and execute the SQL to create the view."""
        backend = schema_editor.connection.vendor
        if backend not in ['postgresql', 'sqlite', 'mysql']:
            raise NotImplementedError(f"Unsupported backend: {backend}")

        query = f"""
            CREATE VIEW {self.db_table} AS
            SELECT {self.select}
            FROM {self.from_table}
            {self.join}
            {self.where}
            {self.order_by}
        """
        schema_editor.execute(query)

    def database_backwards(self, app_label, schema_editor, from_state, to_state):
        """Drop the view if it exists."""
        schema_editor.execute(f"DROP VIEW IF EXISTS {self.db_table}")

    def describe(self):
        return f"Create database view '{self.db_table}'"
