import sqlite3


class SQLiteDatabaseInitializer:
    def __init__(self, db_name: str = ":memory:"):
        self._conn = sqlite3.connect(db_name)

    def create_employee_table(self) -> None:
        cursor = self._conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS employee (
                employee_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                position TEXT NOT NULL,
                email TEXT NOT NULL,
                salary REAL NOT NULL,
                created_at TEXT NOT NULL,
                modified_at TEXT NOT NULL
            )
        """
        )
        self._conn.commit()
        cursor.close()
