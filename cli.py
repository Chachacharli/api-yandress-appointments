import subprocess

import typer

app = typer.Typer()


@app.command()
def run() -> None:
    """Levanta el servidor con uvicorn"""
    subprocess.run(["uvicorn", "app.api.main:app", "--reload"])


@app.command()
def makemigration(message: str) -> None:
    """Crear una nueva migración de Alembic."""
    subprocess.run(["alembic", "revision", "--autogenerate", "-m", message])


# @app.command()
# def migrate() -> None:
#     """Aplicar todas las migraciones pendientes."""
#     subprocess.run(["alembic", "upgrade", "head"])


# @app.command()
# def downgrade(revision: str = "-1") -> None:
#     """Hacer downgrade de la base de datos a una versión anterior."""
#     subprocess.run(["alembic", "downgrade", revision])


if __name__ == "__main__":
    app()
