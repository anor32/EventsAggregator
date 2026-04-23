import typer
from dotenv import load_dotenv
from sqlalchemy import text

from app.settings.db_config import DB_NAME, system_engine

load_dotenv()


def main(
    operation: str = typer.Option(
        "check", "-op", "--operation", help="выбор операции"
    ),
):
    if operation == "create":
        create_db()
    elif operation == "drop":
        drop_db()
    else:
        check_db()


def create_db() -> None:
    """создает базу данных на основе env"""

    if not check_db():
        with system_engine.connect() as conn:
            stmt = text(f"CREATE DATABASE {DB_NAME}")
            conn.execute(stmt)

        print(f"База данных {DB_NAME} создана успешно")
    else:
        print("Ошибка создания база существует")


def drop_db() -> None:
    """Удаляет базу данных на основе env"""

    if not check_db():
        print("Ошибка удаления базы не существует")
        return
    with system_engine.connect() as conn:
        print(DB_NAME)
        stmt = text(f'DROP DATABASE IF EXISTS "{DB_NAME}"')
        conn.execute(stmt)

    print("База данных Удалена успешно")


def check_db() -> bool:
    try:
        with system_engine.connect() as conn:
            result = conn.execute(
                text("SELECT 1 FROM pg_database WHERE datname = :db_name"),
                {"db_name": DB_NAME},
            )
            db_exists = result.scalar() is not None
    except Exception as e:
        print("Ошибка базы данных")
        print(e)
        return False

    if db_exists:
        print("база существует")
        return True
    else:
        print(f"база {DB_NAME} существует")
        return False


if __name__ == "__main__":
    typer.run(main)
