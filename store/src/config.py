import os


def try_parse(type, value: str):
    try:
        return type(value)
    except Exception:
        return None


# Configuration for POSTGRES
PG_HOST = os.environ.get("POSTGRES_HOST") or "localhost"
PG_PORT = try_parse(int, os.environ.get("POSTGRES_PORT")) or 5432
PG_USER = os.environ.get("POSTGRES_USER") or "user"
PG_PASS = os.environ.get("POSTGRES_PASS") or "pass"
PG_DB = os.environ.get("POSTGRES_DB") or "test_db"
