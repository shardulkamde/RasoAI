from collections import Counter
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from dataset_loader import load_recipes_from_excel
from recipe_retriever import RecipeRetriever

app = FastAPI(title="RasoAI API", version="3.0")

DATASET_PATH = "data/IndianFoodDatasetXLS.xlsx"
NON_INGREDIENT_KEYWORDS = {
    "all", "as", "big", "black", "boiled", "brown", "chopped", "cooking",
    "cut", "diced", "dry", "dried", "extra", "few", "finely", "fresh",
    "for", "garnish", "grated", "green", "inch", "into", "leaves", "medium", "of", "or",
    "peeled", "pinch", "powder", "purpose", "red", "required", "roughly",
    "seeds", "sliced", "small", "slit", "soaked", "sprig", "stick", "sweet",
    "taste", "thinly", "to", "virgin", "white", "whole",
}

recipes_data = load_recipes_from_excel(DATASET_PATH)
retriever = RecipeRetriever(recipes_data)
ingredient_counts = Counter(
    keyword
    for recipe in recipes_data
    for keyword in set(recipe["ingredients_keywords"])
    if keyword not in NON_INGREDIENT_KEYWORDS
)


class RecipeQuery(BaseModel):
    ingredients: List[str]


@app.get("/")
def home():
    return {"message": "Welcome to RasoAI API. Go to /docs to test."}


@app.get("/ingredients")
def list_ingredients():
    return {"ingredients": [name for name, _ in ingredient_counts.most_common()]}


@app.post("/chat")
def chat(query: RecipeQuery):
    best_recipe = retriever.get_best_recipe(query.ingredients)

    if not best_recipe:
        return {
            "status": "no_match",
            "message": "No recipe found matching at least half of the entered ingredients."
        }

    chatbot_response = (
        f"Recipe: {best_recipe['recipe_name']}\n\n"
        f"Ingredients: {best_recipe['ingredients_text']}\n\n"
        f"Instructions (from dataset): {best_recipe['instructions']}"
    )

    return {
        "status": "success",
        "best_match": best_recipe,
        "chatbot_response": chatbot_response
    }
