from pathlib import Path

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
PROFILE_PATH = DATA_DIR / "profile.json"

# ── Nutrition constants ────────────────────────────────────────────────────────
PROTEIN_PER_LBM = 1.1       # g per lb of lean body mass
ACTIVITY_MULTIPLIER = 1.65  # very active (5–7 days/week intense training)
DAILY_DEFICIT = 625         # kcal/day → ~1.25 lb fat loss/week

# Calorie modifiers applied to the daily average target
DAY_MODIFIERS = {
    "strength": 1.06,
    "cardio":   0.97,
    "rest":     0.86,
}

# Fat as % of daily calories by day type (carb-cycling: higher carbs on training days)
FAT_PCT = {
    "strength": 0.25,
    "cardio":   0.30,
    "rest":     0.35,
}

# Meal distribution within the IF window (% of daily totals)
MEAL_DISTRIBUTION = [
    {"label": "Meal 1 — Lunch",    "time": "12:00 PM", "cal_pct": 0.40, "pro_pct": 0.40, "fat_pct": 0.35},
    {"label": "Meal 2 — Mid-Aft.", "time": " 4:00 PM", "cal_pct": 0.35, "pro_pct": 0.35, "fat_pct": 0.40},
    {"label": "Meal 3 — Dinner",   "time": " 7:30 PM", "cal_pct": 0.25, "pro_pct": 0.25, "fat_pct": 0.25},
]

EATING_WINDOW = ("12:00 PM", "8:00 PM")

# ── Meal ideas keyed to user preferences (ground beef, tuna, lean turkey) ─────
MEAL_IDEAS = {
    "meal_1": [
        "8 oz 90/10 ground beef · 1.5 cups white rice · mixed greens",
        "8 oz lean ground turkey · 1.5 cups rice · roasted peppers & onion",
        "2 cans chunk light tuna · 2 cups rice · 1 tbsp olive oil · cucumber",
    ],
    "meal_2": [
        "2 cans chunk light tuna · whole grain crackers · apple",
        "Protein shake (40g whey) · 1 cup oatmeal · banana",
        "6 oz lean ground turkey · 1 medium sweet potato",
    ],
    "meal_3": [
        "6 oz 93/7 ground beef · large salad · 1 tbsp olive oil",
        "6 oz lean ground turkey · roasted broccoli & zucchini",
        "2 cans tuna · 1 slice whole grain toast · sliced avocado",
    ],
}

# ── Recovery tools at Lifetime Fitness River North ────────────────────────────
RECOVERY_OPTIONS = [
    "Cold plunge (10–15 min, 50–55°F)",
    "Infrared sauna (20–30 min post-workout)",
    "Steam room (10 min)",
    "Foam roll + static stretch (10–15 min)",
    "Normatec compression boots (20 min)",
]
