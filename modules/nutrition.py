import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from config import (
    PROFILE_PATH,
    PROTEIN_PER_LBM,
    ACTIVITY_MULTIPLIER,
    DAILY_DEFICIT,
    DAY_MODIFIERS,
    FAT_PCT,
    MEAL_DISTRIBUTION,
    MEAL_IDEAS,
)


def load_profile() -> dict:
    with open(PROFILE_PATH) as f:
        return json.load(f)


def get_tdee(profile: dict) -> int:
    return round(profile["bmr_kcal"] * ACTIVITY_MULTIPLIER)


def get_avg_target_calories(profile: dict) -> int:
    return get_tdee(profile) - DAILY_DEFICIT


def get_macros(profile: dict, day_type: str) -> dict:
    avg = get_avg_target_calories(profile)
    calories = round(avg * DAY_MODIFIERS[day_type])

    protein_g = round(profile["lean_body_mass_lbs"] * PROTEIN_PER_LBM)
    fat_g = round(calories * FAT_PCT[day_type] / 9)
    carbs_g = max(round((calories - protein_g * 4 - fat_g * 9) / 4), 50)

    return {
        "calories": calories,
        "protein_g": protein_g,
        "fat_g": fat_g,
        "carbs_g": carbs_g,
    }


def get_meal_breakdown(macros: dict) -> list[dict]:
    meals = []
    for i, dist in enumerate(MEAL_DISTRIBUTION):
        meal_cal = round(macros["calories"] * dist["cal_pct"])
        meal_pro = round(macros["protein_g"] * dist["pro_pct"])
        meal_fat = round(macros["fat_g"] * dist["fat_pct"])
        meal_carbs = max(round((meal_cal - meal_pro * 4 - meal_fat * 9) / 4), 0)
        key = f"meal_{i + 1}"
        meals.append({
            "label": dist["label"],
            "time": dist["time"],
            "calories": meal_cal,
            "protein_g": meal_pro,
            "fat_g": meal_fat,
            "carbs_g": meal_carbs,
            "ideas": MEAL_IDEAS[key],
        })
    return meals
