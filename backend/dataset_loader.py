import pandas as pd
from typing import List, Dict
from utils import extract_keywords


def load_recipes_from_excel(excel_path: str) -> List[Dict]:
    df = pd.read_excel(excel_path)

    required_columns = [
        "Srno",
        "RecipeName",
        "Ingredients",
        "Instructions",
        "Cuisine",
        "Course",
        "Diet",
        "PrepTimeInMins",
        "CookTimeInMins",
        "TotalTimeInMins",
        "Servings",
        "URL"
    ]

    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"❌ Missing required column: {col}")

    recipes = []

    for _, row in df.iterrows():
        ingredients_text = str(row["Ingredients"]).strip()

        recipes.append({
            "srno": int(row["Srno"]) if pd.notna(row["Srno"]) else None,
            "recipe_name": str(row["RecipeName"]).strip(),
            "ingredients_text": ingredients_text,
            "ingredients_keywords": extract_keywords(ingredients_text),
            "instructions": str(row["Instructions"]).strip(),
            "cuisine": str(row["Cuisine"]).strip(),
            "course": str(row["Course"]).strip(),
            "diet": str(row["Diet"]).strip(),
            "prep_time": int(row["PrepTimeInMins"]) if pd.notna(row["PrepTimeInMins"]) else 0,
            "cook_time": int(row["CookTimeInMins"]) if pd.notna(row["CookTimeInMins"]) else 0,
            "total_time": int(row["TotalTimeInMins"]) if pd.notna(row["TotalTimeInMins"]) else 0,
            "servings": str(row["Servings"]).strip(),
            "url": str(row["URL"]).strip()
        })

    return recipes
