import importlib
from pathlib import Path
from src.services.database.db_service import get_connection

class DatabaseInitializer:
    def __init__(self):
        self.run_migrations()

    def run_migrations(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS migrations (
                    name TEXT PRIMARY KEY
                )
            """)
            conn.commit()
            
            migration_dir = Path(__file__).parent / "migrations"
            for migration_file in sorted(migration_dir.glob("*.py")):
                migration = migration_file.stem
                cursor.execute("SELECT name FROM migrations WHERE name = :migration", {"migration": migration})
                if not cursor.fetchone():
                    module = importlib.import_module(f"src.database.migrations.{migration}")
                    module.up(conn)
                    cursor.execute("INSERT INTO migrations (name) VALUES (:migration)", {"migration": migration})
                    conn.commit()
                    print(f"Ran migration: {migration}")