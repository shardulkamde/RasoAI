import re


def clean_text(text: str) -> str:
    if text is None:
        return ""

    text = str(text).lower()

    # remove brackets content
    text = re.sub(r"\(.*?\)", " ", text)

    # remove digits
    text = re.sub(r"\d+", " ", text)

    # remove special characters
    text = re.sub(r"[^a-zA-Z\s]", " ", text)

    # remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text


def extract_keywords(ingredients_text: str) -> list:
    cleaned = clean_text(ingredients_text)

    words = cleaned.split()

    stop_words = {
        "to", "taste", "required", "as", "and", "or", "of",
        "tablespoon", "tablespoons", "teaspoon", "teaspoons",
        "tbsp", "tsp", "cup", "cups", "grams", "gram", "kg", "ml",
        "liter", "litre", "small", "big", "medium", "finely",
        "chopped", "sliced", "fresh", "boiled"
    }

    keywords = []
    for w in words:
        if w not in stop_words and len(w) > 2:
            keywords.append(w)

    return list(set(keywords))
