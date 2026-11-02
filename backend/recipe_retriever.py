from typing import List, Dict
from rapidfuzz import fuzz
from utils import extract_keywords


class RecipeRetriever:
    MIN_MATCH_SCORE = 50
    FUZZY_MATCH_THRESHOLD = 90

    def __init__(self, recipes: List[Dict]):
        self.recipes = recipes

    def _matched_keyword_count(self, user_keywords: list, recipe_keywords: list) -> int:
        recipe_keywords = set(recipe_keywords)
        return sum(
            1
            for user_keyword in set(user_keywords)
            if any(
                fuzz.ratio(user_keyword, recipe_keyword) >= self.FUZZY_MATCH_THRESHOLD
                for recipe_keyword in recipe_keywords
            )
        )

    def _matched_ingredient_count(self, user_ingredients: List[str], recipe_keywords: list) -> int:
        recipe_keywords = set(recipe_keywords)
        matched = 0

        for ingredient in user_ingredients:
            keywords = extract_keywords(ingredient)
            if keywords and self._matched_keyword_count(keywords, recipe_keywords) == len(set(keywords)):
                matched += 1

        return matched

    def score_recipe(self, user_keywords: list, recipe_keywords: list) -> float:
        user_keywords = set(user_keywords)
        recipe_keywords = set(recipe_keywords)
        if not user_keywords or not recipe_keywords:
            return 0

        matched_keywords = self._matched_keyword_count(
            list(user_keywords),
            list(recipe_keywords),
        )
        return (2 * matched_keywords / (len(user_keywords) + len(recipe_keywords))) * 100

    def get_best_recipe(self, user_ingredients: List[str]) -> Dict | None:
        user_ingredients = [
            ingredient for ingredient in user_ingredients if extract_keywords(ingredient)
        ]
        if not user_ingredients:
            return None

        user_text = ",".join(user_ingredients)
        user_keywords = extract_keywords(user_text)

        best_recipe = None
        best_score = 0
        best_rank = (0, 0)

        for recipe in self.recipes:
            recipe_keywords = recipe["ingredients_keywords"]
            matched_ingredients = self._matched_ingredient_count(
                user_ingredients,
                recipe_keywords,
            )
            coverage = (matched_ingredients / len(user_ingredients)) * 100
            if coverage < self.MIN_MATCH_SCORE:
                continue

            score = self.score_recipe(user_keywords, recipe_keywords)
            rank = (coverage, score)

            if rank > best_rank:
                best_rank = rank
                best_score = score
                best_recipe = recipe

        if best_recipe:
            return {
                "srno": best_recipe["srno"],
                "recipe_name": best_recipe["recipe_name"],
                "cuisine": best_recipe["cuisine"],
                "course": best_recipe["course"],
                "diet": best_recipe["diet"],
                "prep_time_mins": best_recipe["prep_time"],
                "cook_time_mins": best_recipe["cook_time"],
                "total_time_mins": best_recipe["total_time"],
                "servings": best_recipe["servings"],
                "url": best_recipe["url"],
                "ingredients_text": best_recipe["ingredients_text"],
                "instructions": best_recipe["instructions"],
                "similarity_score": round(best_score, 2)
            }

        return None
