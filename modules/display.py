import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.rule import Rule
from rich import box

from config import EATING_WINDOW, RECOVERY_OPTIONS
from modules.training import get_today_session, get_week_schedule
from modules.nutrition import (
    load_profile,
    get_macros,
    get_meal_breakdown,
    get_tdee,
    get_avg_target_calories,
)

console = Console()

_TYPE_COLOR = {"strength": "green", "cardio": "cyan", "rest": "yellow"}
_TYPE_LABEL = {"strength": "STRENGTH", "cardio": "CARDIO", "rest": "REST"}


# ── Weekly plan ────────────────────────────────────────────────────────────────

def display_weekly_plan() -> None:
    profile = load_profile()
    schedule = get_week_schedule()
    today_dow = date.today().weekday()

    console.print()
    console.print(Panel(
        f"[bold white]Weekly Training Plan[/bold white]  ·  {profile['name']}  ·  Body Recomposition Phase",
        style="bold blue",
        padding=(0, 2),
    ))
    console.print()

    table = Table(
        box=box.ROUNDED,
        header_style="bold white",
        border_style="bright_black",
        pad_edge=False,
    )
    table.add_column("Day",      style="bold", width=14)
    table.add_column("Type",     width=11)
    table.add_column("Session",  width=32)
    table.add_column("Duration", width=12)
    table.add_column("Calories", width=12, justify="right")

    for entry in schedule:
        day_type = entry["type"]
        session  = entry["session"]
        color    = _TYPE_COLOR[day_type]
        is_today = entry["day_idx"] == today_dow

        nutrition_type = day_type if day_type in DAY_MODIFIERS_KEYS else "rest"
        macros = get_macros(profile, nutrition_type)

        day_str     = f"[bold]{'> ' if is_today else '  '}{entry['day']}[/bold]"
        type_str    = f"[{color}]{_TYPE_LABEL[day_type]}[/{color}]"
        session_str = (
            f"[{'bold white' if is_today else 'white'}]{session['name']}[/]"
            f"\n[dim]{session.get('tag', '')}[/dim]"
        )
        duration_str = session.get("est_duration", "—")
        cal_str      = f"[{color}]{macros['calories']} kcal[/{color}]"

        row_style = "on grey11" if is_today else ""
        table.add_row(day_str, type_str, session_str, duration_str, cal_str, style=row_style)

    console.print(table)
    console.print()

    tdee    = get_tdee(profile)
    avg_cal = get_avg_target_calories(profile)
    console.print(
        f"  [dim]TDEE est.[/dim] {tdee} kcal"
        f"  ·  [dim]Daily avg target[/dim] {avg_cal} kcal"
        f"  ·  [dim]Deficit[/dim] ~625 kcal/day"
        f"  →  [bold green]~1.25 lb fat/week[/bold green]"
    )
    console.print()


# ── Today ──────────────────────────────────────────────────────────────────────

def display_today() -> None:
    profile      = load_profile()
    session_type, session = get_today_session()
    today        = date.today()
    day_names    = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    day_name     = day_names[today.weekday()]
    color        = _TYPE_COLOR[session_type]

    console.print()
    console.print(Panel(
        f"[bold]{day_name}, {today.strftime('%B %-d, %Y')}[/bold]"
        f"  ·  [{color}]{_TYPE_LABEL[session_type]}[/{color}]"
        f"  ·  [bold white]{session['name']}[/bold white]",
        style=f"bold {color}",
        padding=(0, 2),
    ))

    if session_type == "strength":
        _render_strength_session(session)
    else:
        _render_cardio_session(session, session_type)

    nutrition_type = session_type if session_type in ("strength", "cardio") else "rest"
    macros = get_macros(profile, nutrition_type)
    meals  = get_meal_breakdown(macros)
    _render_nutrition(macros, meals, nutrition_type)


# ── Nutrition standalone ───────────────────────────────────────────────────────

def display_nutrition(day_type_arg: str) -> None:
    profile = load_profile()

    if day_type_arg == "auto":
        session_type, _ = get_today_session()
        day_type = session_type if session_type in ("strength", "cardio") else "rest"
    elif day_type_arg in ("strength", "training"):
        day_type = "strength"
    elif day_type_arg in ("cardio", "hybrid"):
        day_type = "cardio"
    else:
        day_type = "rest"

    macros = get_macros(profile, day_type)
    meals  = get_meal_breakdown(macros)

    console.print()
    console.print(Panel(
        f"[bold white]Daily Nutrition Guide[/bold white]  ·  {profile['name']}  ·  {day_type.upper()} DAY",
        style="bold blue",
        padding=(0, 2),
    ))
    _render_nutrition(macros, meals, day_type, show_all_ideas=True)


# ── Stats ──────────────────────────────────────────────────────────────────────

def display_stats() -> None:
    profile = load_profile()
    tdee    = get_tdee(profile)
    avg_cal = get_avg_target_calories(profile)
    target_weight = round(profile["weight_lbs"] - profile["fat_loss_target_lbs"], 1)
    target_bf_pct = round(
        (profile["body_fat_mass_lbs"] - profile["fat_loss_target_lbs"])
        / profile["weight_lbs"] * 100, 1
    )

    console.print()
    console.print(Panel(
        f"[bold white]Baseline Stats & Recomposition Targets[/bold white]"
        f"  ·  InBody Assessment {profile['assessment_date']}",
        style="bold blue",
        padding=(0, 2),
    ))
    console.print()

    table = Table(box=box.SIMPLE, show_header=True, header_style="bold dim", border_style="bright_black")
    table.add_column("Metric",   style="dim",        width=28)
    table.add_column("Baseline", style="bold white",  width=18)
    table.add_column("Target",   style="bold green",  width=24)

    rows = [
        ("Height",               profile["height"],                          "—"),
        ("Weight",               f"{profile['weight_lbs']} lb",              f"~{target_weight} lb  (−{profile['fat_loss_target_lbs']} lb)"),
        ("Body Fat %",           f"{profile['body_fat_pct']}%",              f"~{target_bf_pct}%"),
        ("Body Fat Mass",        f"{profile['body_fat_mass_lbs']} lb",       f"~{profile['body_fat_mass_lbs'] - profile['fat_loss_target_lbs']:.1f} lb"),
        ("Lean Body Mass",       f"{profile['lean_body_mass_lbs']} lb",      "Maintain 211+ lb"),
        ("Skeletal Muscle Mass", f"{profile['skeletal_muscle_mass_lbs']} lb","Maintain 122+ lb"),
        ("BMI",                  str(profile["bmi"]),                        "~30.1"),
        ("Visceral Fat Level",   str(profile["visceral_fat_level"]),         "< 9  (target)"),
        ("Waist-Hip Ratio",      str(profile["waist_hip_ratio"]),            "< 0.95"),
        ("BMR",                  f"{profile['bmr_kcal']} kcal",              "—"),
        ("TDEE (estimated)",     f"{tdee} kcal",                             "—"),
        ("Daily calorie target", f"{avg_cal} kcal avg",                     "Cycles by day type"),
    ]
    for metric, baseline, target in rows:
        table.add_row(metric, baseline, target)

    console.print(table)
    console.print()

    console.print(Rule("[bold white]Recomposition Timeline[/bold white]", style="bright_black"))
    console.print()
    weeks = round(profile["fat_loss_target_lbs"] / 1.25, 1)
    console.print(f"  [bold]Fat loss target:[/bold]   {profile['fat_loss_target_lbs']} lb at ~1.25 lb/week aggressive pace")
    console.print(f"  [bold]Estimated duration:[/bold] {weeks} weeks  (~11 weeks from program start)")
    console.print(f"  [bold]Calorie protocol:[/bold]  {avg_cal} kcal/day avg  ·  Carb-cycled by day type")
    console.print(f"  [bold]IF window:[/bold]         {EATING_WINDOW[0]} – {EATING_WINDOW[1]}  (8-hour eating window)")
    console.print(f"  [bold]Protein target:[/bold]    ~233g/day  (1.1g × {profile['lean_body_mass_lbs']} lb LBM)")
    console.print()
    console.print(
        "  [dim]Strategy: High-protein intake + heavy compound lifting preserves lean mass\n"
        "  during the cut. Calorie cycling keeps training performance high while creating\n"
        "  a sustained weekly deficit.[/dim]"
    )
    console.print()


# ── Internal renderers ─────────────────────────────────────────────────────────

def _render_strength_session(session: dict) -> None:
    console.print()
    console.print(f"  [bold green]EXERCISES[/bold green]  [dim]· {session['est_duration']}[/dim]")
    console.print()

    table = Table(
        box=box.SIMPLE_HEAD,
        header_style="bold dim",
        border_style="bright_black",
        pad_edge=True,
    )
    table.add_column("#",        style="dim",          width=3,  justify="right")
    table.add_column("Exercise",                       width=28)
    table.add_column("Sets",                           width=5,  justify="center")
    table.add_column("Reps",                           width=8,  justify="center")
    table.add_column("Load",     style="yellow",       width=14)
    table.add_column("Cue",      style="dim")

    for i, ex in enumerate(session["exercises"], 1):
        table.add_row(
            str(i),
            f"[bold white]{ex['name']}[/bold white]",
            str(ex["sets"]),
            ex["reps"],
            ex["load"],
            ex["note"],
        )

    console.print(table)
    console.print()
    console.print(f"  [dim]Post-session recovery:[/dim]  " + "  ·  ".join(RECOVERY_OPTIONS[:3]))


def _render_cardio_session(session: dict, session_type: str) -> None:
    color = _TYPE_COLOR[session_type]
    console.print()
    console.print(
        f"  [{color}]{_TYPE_LABEL[session_type]} SESSION[/{color}]"
        f"  [dim]· {session['est_duration']}[/dim]"
    )
    console.print()
    console.print(f"  [bold white]{session['name']}[/bold white]  [dim]({session.get('tag', '')})[/dim]")
    console.print(f"  [dim]HR Zone:[/dim]  {session['heart_rate_zone']}")
    console.print()
    for step in session["structure"]:
        console.print(f"  [{color}]>[/{color}]  {step}")
    console.print()
    if "target_pace" in session:
        console.print(f"  [dim]Target:[/dim]  {session['target_pace']}")
    if "notes" in session:
        console.print(f"  [dim]Note:[/dim]    {session['notes']}")

    if session_type == "rest":
        console.print()
        console.print(f"  [dim]Recovery options at Lifetime:[/dim]")
        for opt in RECOVERY_OPTIONS:
            console.print(f"    [dim]·[/dim] {opt}")


def _render_nutrition(macros: dict, meals: list[dict], day_type: str, show_all_ideas: bool = False) -> None:
    color = _TYPE_COLOR.get(day_type, "white")
    console.print()
    console.print(Rule(
        f"[{color}]NUTRITION — {day_type.upper()} DAY[/{color}]",
        style="bright_black",
    ))
    console.print()

    console.print(
        f"  [bold white]{macros['calories']} kcal[/bold white]"
        f"  ·  [bold green]Protein {macros['protein_g']}g[/bold green]"
        f"  ·  [bold yellow]Carbs {macros['carbs_g']}g[/bold yellow]"
        f"  ·  [bold cyan]Fat {macros['fat_g']}g[/bold cyan]"
    )
    console.print()
    console.print(
        f"  [dim]Eating window:[/dim]  [bold]{EATING_WINDOW[0]}[/bold]  →  [bold]{EATING_WINDOW[1]}[/bold]"
        f"  [dim](8-hour window · fast until noon)[/dim]"
    )
    console.print()

    table = Table(
        box=box.SIMPLE_HEAD,
        header_style="bold dim",
        border_style="bright_black",
        pad_edge=True,
    )
    table.add_column("Meal",    width=22)
    table.add_column("Time",    width=10, justify="center")
    table.add_column("kcal",    width=7,  justify="right")
    table.add_column("Protein", width=9,  justify="right")
    table.add_column("Carbs",   width=8,  justify="right")
    table.add_column("Fat",     width=7,  justify="right")
    table.add_column("Sample",  style="dim")

    for meal in meals:
        table.add_row(
            f"[bold]{meal['label']}[/bold]",
            meal["time"],
            str(meal["calories"]),
            f"[green]{meal['protein_g']}g[/green]",
            f"[yellow]{meal['carbs_g']}g[/yellow]",
            f"[cyan]{meal['fat_g']}g[/cyan]",
            meal["ideas"][0],
        )

    console.print(table)

    if show_all_ideas:
        console.print()
        console.print("  [dim bold]MORE MEAL IDEAS[/dim bold]")
        for i, meal in enumerate(meals, 1):
            console.print(f"  [bold]Meal {i}[/bold]")
            for idea in meal["ideas"]:
                console.print(f"    [dim]·[/dim] {idea}")

    console.print()


# Sentinel used in display_weekly_plan to guard day type lookup
DAY_MODIFIERS_KEYS = ("strength", "cardio", "rest")
