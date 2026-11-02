import unittest

from recipe_retriever import RecipeRetriever
from utils import extract_keywords


def make_recipe(name: str, ingredients: str) -> dict:
    return {
        "srno": 1,
        "recipe_name": name,
        "cuisine": "Indian",
        "course": "Dinner",
        "diet": "Vegetarian",
        "prep_time": 10,
        "cook_time": 20,
        "total_time": 30,
        "servings": "2",
        "url": "",
        "ingredients_text": ingredients,
        "ingredients_keywords": extract_keywords(ingredients),
        "instructions": "Cook and serve.",
    }


class RecipeRetrieverTests(unittest.TestCase):
    def test_prefers_exact_ingredient_over_partial_word_match(self):
        recipes = [
            make_recipe("Spiced dish", "spice, turmeric"),
            make_recipe("Rice dish", "rice, lentils"),
        ]

        match = RecipeRetriever(recipes).get_best_recipe(["rice"])

        self.assertEqual(match["recipe_name"], "Rice dish")
        self.assertGreater(match["similarity_score"], 50)

    def test_scores_supplied_ingredients_not_recipe_word_count(self):
        recipes = [
            make_recipe("Seafood stew", "milk, lemon juice, fish, garlic, tomato"),
            make_recipe("Homemade Paneer", "3 liter Milk, 4 tablespoons Lemon juice"),
        ]

        match = RecipeRetriever(recipes).get_best_recipe(["milk", "lemon juice"])

        self.assertEqual(match["recipe_name"], "Homemade Paneer")
        self.assertGreater(match["similarity_score"], 80)

    def test_rejects_recipes_matching_less_than_half_the_input(self):
        recipe = make_recipe("Milk dish", "milk, sugar")

        match = RecipeRetriever([recipe]).get_best_recipe(["milk", "rice", "tomato"])

        self.assertIsNone(match)

    def test_keeps_small_spelling_variations(self):
        recipe = make_recipe("Tomato dish", "tomato, onion")

        match = RecipeRetriever([recipe]).get_best_recipe(["tomatoe"])

        self.assertEqual(match["recipe_name"], "Tomato dish")


if __name__ == "__main__":
    unittest.main()
