#!/usr/bin/env python3
"""Personal Fitness Coach — Body Recomposition CLI"""
import typer
from typing_extensions import Annotated

app = typer.Typer(
    help="Personal Fitness Coach — Body Recomposition Program",
    add_completion=False,
    no_args_is_help=True,
)


@app.command()
def plan():
    """Show this week's full 7-day training plan."""
    from modules.display import display_weekly_plan
    display_weekly_plan()


@app.command()
def today():
    """Show today's training session and nutrition targets."""
    from modules.display import display_today
    display_today()


@app.command()
def nutrition(
    day: Annotated[
        str,
        typer.Option(
            "--day", "-d",
            help="Day type: strength | cardio | rest | auto (default: auto-detect from today)",
        ),
    ] = "auto",
):
    """Show daily nutrition targets, meal breakdown, and meal ideas."""
    from modules.display import display_nutrition
    display_nutrition(day)


@app.command()
def stats():
    """Show baseline InBody stats and recomposition targets."""
    from modules.display import display_stats
    display_stats()


if __name__ == "__main__":
    app()
