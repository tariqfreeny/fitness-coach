from datetime import date

# ── Strength workout library ───────────────────────────────────────────────────
STRENGTH_WORKOUTS = [
    {
        "id": "lower_power",
        "name": "Lower Body Power",
        "tag": "Squat Focus",
        "est_duration": "60–75 min",
        "exercises": [
            {"name": "Back Squat",            "sets": 4, "reps": "4–6",    "load": "85% 1RM",   "note": "Belt optional, brace hard"},
            {"name": "Romanian Deadlift",      "sets": 3, "reps": "8–10",  "load": "Mod-Heavy", "note": "Hip hinge, slight knee bend"},
            {"name": "Bulgarian Split Squat",  "sets": 3, "reps": "8/leg", "load": "Moderate",  "note": "Torso upright, front foot forward"},
            {"name": "Leg Press",              "sets": 3, "reps": "10–12", "load": "Moderate",  "note": "Full ROM, don't lock out"},
            {"name": "Standing Calf Raise",    "sets": 4, "reps": "15–20", "load": "Moderate",  "note": "Pause at bottom stretch"},
            {"name": "Ab Wheel Rollout",       "sets": 3, "reps": "8–12",  "load": "BW",        "note": "Brace core, don't hyperextend"},
        ],
    },
    {
        "id": "upper_power",
        "name": "Upper Body Power",
        "tag": "Push/Pull Strength",
        "est_duration": "60–75 min",
        "exercises": [
            {"name": "Barbell Bench Press",    "sets": 4, "reps": "4–6",   "load": "85% 1RM",   "note": "Retract scapula, controlled descent"},
            {"name": "Weighted Pull-Up",       "sets": 4, "reps": "4–6",   "load": "+25–45 lb", "note": "Dead hang to chin over bar"},
            {"name": "Overhead Press",         "sets": 3, "reps": "6–8",   "load": "Mod-Heavy", "note": "Brace core, no lumbar arch"},
            {"name": "Pendlay Row",            "sets": 3, "reps": "6–8",   "load": "Mod-Heavy", "note": "Bar to lower chest, explosive pull"},
            {"name": "Incline DB Press",       "sets": 3, "reps": "8–10",  "load": "Moderate",  "note": "30–45° incline"},
            {"name": "Face Pull",              "sets": 3, "reps": "15–20", "load": "Light",     "note": "External rotation at peak"},
        ],
    },
    {
        "id": "lower_hypertrophy",
        "name": "Lower Body Hypertrophy",
        "tag": "Hinge Focus",
        "est_duration": "65–80 min",
        "exercises": [
            {"name": "Conventional Deadlift",  "sets": 4, "reps": "5–6",    "load": "80–85% 1RM", "note": "Bar stays close, drive through floor"},
            {"name": "Barbell Hip Thrust",     "sets": 4, "reps": "10–12",  "load": "Mod-Heavy",  "note": "Full hip extension, squeeze top"},
            {"name": "Hack Squat",             "sets": 3, "reps": "10–12",  "load": "Moderate",   "note": "High foot placement for glute bias"},
            {"name": "Nordic Hamstring Curl",  "sets": 3, "reps": "6–8",    "load": "BW/Asst.",   "note": "Slow eccentric, control descent"},
            {"name": "Single-Leg RDL",         "sets": 3, "reps": "10/leg", "load": "Light-Mod",  "note": "Hip hinge, control descent"},
            {"name": "Hanging Leg Raise",      "sets": 3, "reps": "12–15",  "load": "BW",         "note": "Control the swing, no kip"},
        ],
    },
    {
        "id": "upper_hypertrophy",
        "name": "Upper Body Hypertrophy",
        "tag": "Volume + Arms",
        "est_duration": "65–75 min",
        "exercises": [
            {"name": "Cable Row (Wide Grip)",     "sets": 4, "reps": "10–12", "load": "Moderate", "note": "Full stretch, squeeze at peak"},
            {"name": "Chest-Supported DB Row",    "sets": 3, "reps": "10–12", "load": "Moderate", "note": "No body English"},
            {"name": "Dumbbell Shoulder Press",   "sets": 4, "reps": "10–12", "load": "Moderate", "note": "Slight forward lean"},
            {"name": "Lat Pulldown",              "sets": 3, "reps": "10–12", "load": "Moderate", "note": "Lean back slightly, pull to chest"},
            {"name": "EZ Bar Curl",               "sets": 3, "reps": "10–12", "load": "Moderate", "note": "Elbows fixed, no swing"},
            {"name": "Tricep Rope Pushdown",      "sets": 3, "reps": "12–15", "load": "Moderate", "note": "Spread rope at bottom"},
            {"name": "Lateral Raise",             "sets": 3, "reps": "15–20", "load": "Light",    "note": "Lead with elbows, control descent"},
        ],
    },
]

# ── Cardio session library ─────────────────────────────────────────────────────
CARDIO_SESSIONS = [
    {
        "id": "tempo_run",
        "name": "Tempo Run",
        "tag": "Threshold Work",
        "est_duration": "40 min",
        "heart_rate_zone": "Zone 3–4 (85–92% max HR)",
        "structure": [
            "10 min easy warm-up (Zone 2)",
            "20 min threshold pace — comfortably hard, 7–8/10 effort",
            "10 min easy cool-down",
        ],
        "target_pace": "~8:30–9:00 min/mile at threshold",
        "notes": "Chicago lakefront path is ideal. Focus on breathing rhythm.",
    },
    {
        "id": "zone2_cross",
        "name": "Zone 2 + Cross Training",
        "tag": "Aerobic Base",
        "est_duration": "50 min",
        "heart_rate_zone": "Zone 2 (65–75% max HR)",
        "structure": [
            "20 min easy treadmill or outdoor run (Zone 2)",
            "15 min row machine — steady Zone 2 pace",
            "15 min assault bike — conversational effort",
        ],
        "target_pace": "Conversational pace throughout",
        "notes": "Prioritizes fat oxidation. Use Lifetime's row + assault bike combo.",
    },
    {
        "id": "recovery_run",
        "name": "Recovery Run",
        "tag": "Optional / Active Recovery",
        "est_duration": "45–60 min",
        "heart_rate_zone": "Zone 1–2 (60–70% max HR)",
        "structure": [
            "Full easy run at conversational pace",
            "No pace targets — this is active recovery",
            "Stop early if you feel fatigued or heavy",
        ],
        "target_pace": "10:00–11:00 min/mile easy",
        "notes": "Optional. Can swap for cold plunge + sauna at Lifetime instead.",
    },
]

# ── Weekly schedule: day_of_week → (session_type, library_index) ──────────────
#   0=Mon  1=Tue  2=Wed  3=Thu  4=Fri  5=Sat  6=Sun
WEEKLY_SCHEDULE = {
    0: ("strength", 0),  # Monday    → Lower Power
    1: ("cardio",   0),  # Tuesday   → Tempo Run
    2: ("strength", 1),  # Wednesday → Upper Power
    3: ("cardio",   1),  # Thursday  → Zone 2 + Cross Training
    4: ("strength", 2),  # Friday    → Lower Hypertrophy
    5: ("strength", 3),  # Saturday  → Upper Hypertrophy
    6: ("rest",     2),  # Sunday    → Rest / Optional Recovery Run
}

DAY_NAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def get_session(day_of_week: int) -> tuple[str, dict]:
    session_type, idx = WEEKLY_SCHEDULE[day_of_week]
    if session_type == "strength":
        return session_type, STRENGTH_WORKOUTS[idx]
    else:
        return session_type, CARDIO_SESSIONS[idx]


def get_today_session() -> tuple[str, dict]:
    return get_session(date.today().weekday())


def get_week_schedule() -> list[dict]:
    entries = []
    for dow, name in enumerate(DAY_NAMES):
        session_type, session = get_session(dow)
        entries.append({
            "day": name,
            "day_idx": dow,
            "type": session_type,
            "session": session,
        })
    return entries
