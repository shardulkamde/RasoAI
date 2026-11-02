import re
import time

import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/chat"
INGREDIENTS_URL = "http://127.0.0.1:8000/ingredients"
INGREDIENT_RESULTS_LIMIT = 20
POPULAR_INGREDIENTS = [
    "salt", "oil", "chilli", "garlic", "ginger", "onion", "mustard",
    "cumin", "turmeric", "tomato", "coriander", "rice", "potato",
    "peas", "capsicum", "carrot", "beans", "dal", "milk", "lemon",
    "coconut", "pepper", "chicken", "paneer",
]


@st.cache_data(ttl=3600, max_entries=1)
def load_ingredient_choices() -> list[str]:
    response = requests.get(INGREDIENTS_URL, timeout=10)
    response.raise_for_status()
    return response.json()["ingredients"]


def toggle_ingredient(ingredient: str) -> None:
    selected = st.session_state["selected_ingredients"]
    if ingredient in selected:
        selected.remove(ingredient)
    else:
        selected.append(ingredient)


def split_instruction_steps(instructions: str) -> list[str]:
    lines = [line.strip() for line in instructions.splitlines() if line.strip()]
    step_pattern = re.compile(
        r"^(?:(?:step\s*)?\d+[.)]|[-*•])\s+(.+)$",
        re.IGNORECASE,
    )
    existing_steps = [step_pattern.match(line) for line in lines]
    if existing_steps and all(existing_steps):
        return [match.group(1).strip() for match in existing_steps if match]

    paragraphs = re.split(r"\n\s*\n", instructions.strip())
    steps = []
    for paragraph in paragraphs:
        normalized = re.sub(r"\s+", " ", paragraph).strip()
        steps.extend(
            sentence.strip()
            for sentence in re.split(
                r"(?<=[.!?])\s+(?=[A-Z0-9“\"])",
                normalized,
            )
            if sentence.strip()
        )
    return steps


def find_recipe(ingredients: list[str]) -> None:
    try:
        response = requests.post(
            API_URL,
            json={"ingredients": ingredients},
            timeout=30,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        st.session_state["recipe_error"] = f"Backend error: {exc}"
        st.session_state["recipe_result"] = None
        return

    st.session_state["recipe_error"] = None
    result = response.json()
    st.session_state["recipe_result"] = result
    st.session_state["animate_instructions"] = result["status"] == "success"


st.set_page_config(
    page_title="RasoAI",
    page_icon=":material/restaurant:",
    layout="wide",
)
st.session_state.setdefault("selected_ingredients", [])
st.session_state.setdefault("recipe_result", None)
st.session_state.setdefault("recipe_error", None)
st.session_state.setdefault("animate_instructions", False)

st.html(
    """
    <style>
        .stApp,
        [data-testid="stAppViewContainer"] {
            background: transparent !important;
        }

        [data-testid="stHeader"] {
            background: rgba(15, 11, 9, 0.88) !important;
        }

        [data-testid="stMain"] {
            position: relative;
            z-index: 1;
            background: transparent !important;
        }

        [data-testid="stMainBlockContainer"] {
            max-width: 1540px;
            padding: 1.3rem 2rem 2rem;
        }

        #background-video {
            position: fixed;
            inset: 0;
            width: 100vw;
            height: 100vh;
            object-fit: cover;
            filter: brightness(0.38) saturate(0.9);
            z-index: 0;
            pointer-events: none;
        }

        .st-key-ingredient_panel,
        .st-key-results_panel {
            background: rgba(17, 16, 15, 0.84);
            border: 1px solid rgba(255, 255, 255, 0.35);
            border-radius: 15px;
            padding: 1rem 1.2rem;
            backdrop-filter: blur(8px);
        }

        .st-key-best_match {
            background: rgba(255, 255, 255, 0.96);
            border-radius: 13px;
            color: #171717;
            padding: 0.8rem 1rem;
        }

        .st-key-best_match h3,
        .st-key-best_match p,
        .st-key-best_match [data-testid="stMetricLabel"],
        .st-key-best_match [data-testid="stMetricValue"] {
            color: #171717;
        }

        .st-key-recipe_response {
            background: rgba(12, 47, 22, 0.88);
            border: 1px solid rgba(113, 207, 100, 0.8);
            border-radius: 12px;
            padding: 0.9rem 1rem;
        }

        .st-key-ingredient_panel [class*="st-key-available_"] button,
        .st-key-ingredient_panel [class*="st-key-selected_"] button {
            min-height: 2.8rem;
            border-radius: 0.8rem;
            padding: 0.45rem 0.65rem;
            border: 1px solid rgba(255, 255, 255, 0.24);
            background: linear-gradient(
                145deg,
                rgba(43, 38, 35, 0.96),
                rgba(25, 24, 24, 0.96)
            );
            color: #f7f1ed;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
            transition:
                border-color 140ms ease,
                background 140ms ease,
                box-shadow 140ms ease,
                transform 140ms ease;
        }

        .st-key-ingredient_panel [class*="st-key-available_"] button:hover {
            border-color: #ff625e;
            background: linear-gradient(
                145deg,
                rgba(111, 44, 39, 0.98),
                rgba(63, 31, 29, 0.98)
            );
            box-shadow: 0 4px 12px rgba(255, 62, 62, 0.18);
            transform: translateY(-1px);
        }

        .st-key-ingredient_panel [class*="st-key-available_"] button
        [data-testid="stIconMaterial"] {
            color: #ff756e;
        }

        .st-key-ingredient_panel [class*="st-key-selected_"] button {
            border-color: #ff7770;
            background: linear-gradient(135deg, #f44343, #d92e38);
            color: #fff;
            box-shadow: 0 3px 10px rgba(244, 67, 67, 0.25);
        }

        .st-key-ingredient_panel [class*="st-key-selected_"] button:hover {
            border-color: #ffaaa3;
            background: linear-gradient(135deg, #e23b3b, #bd2631);
            color: #fff;
        }

        .st-key-ingredient_panel [class*="st-key-selected_"] button
        [data-testid="stIconMaterial"] {
            color: #fff;
        }

        .st-key-ingredient_panel [class*="st-key-available_"] button p,
        .st-key-ingredient_panel [class*="st-key-selected_"] button p {
            font-size: 0.84rem;
            white-space: nowrap;
        }

        @media (max-width: 700px) {
            [data-testid="stMainBlockContainer"] {
                padding: 1rem 0.8rem;
            }
        }
    </style>
    <video id="background-video" autoplay muted loop playsinline aria-hidden="true">
        <source src="/app/static/background.mp4" type="video/mp4">
    </video>
    """
)

with st.container(horizontal=True, vertical_alignment="center"):
    with st.container():
        st.subheader(":material/restaurant: RasoAI")
        st.caption("AI-powered Indian recipe finder")
    st.markdown(
        "**:material/restaurant_menu: Select ingredients**"
        "　→　**:material/arrow_forward: Generate recipe**"
        "　→　**:material/restaurant: Cook Indian dishes**"
    )

st.divider()

ingredient_panel, results_panel = st.columns([0.4, 0.6], gap="medium")

with ingredient_panel:
    with st.container(border=True, key="ingredient_panel"):
        st.subheader(":material/shopping_basket: Choose ingredients")
        st.caption("Select ingredients from the dataset or search for your own.")

        try:
            available_ingredients = load_ingredient_choices()
        except requests.RequestException as exc:
            available_ingredients = []
            st.error(f"Could not load dataset ingredients: {exc}")

        selected_ingredients = st.session_state["selected_ingredients"]
        if selected_ingredients:
            st.caption("Selected ingredients · click to remove")
            selected_columns = st.columns(3)
            for index, ingredient in enumerate(selected_ingredients):
                with selected_columns[index % len(selected_columns)]:
                    st.button(
                        ingredient.title(),
                        key=f"selected_{ingredient}",
                        icon=":material/check:",
                        type="primary",
                        on_click=toggle_ingredient,
                        args=(ingredient,),
                        width="stretch",
                    )

        ingredient_search = st.text_input(
            "Search or add an ingredient",
            placeholder="Search onion, rice, garlic…",
            key="ingredient_search",
        )
        search_term = ingredient_search.strip().casefold()
        if search_term:
            matches = [
                ingredient for ingredient in available_ingredients
                if search_term in ingredient.casefold()
                and ingredient not in selected_ingredients
            ]
        else:
            ingredient_set = set(available_ingredients)
            matches = [
                ingredient for ingredient in POPULAR_INGREDIENTS
                if ingredient in ingredient_set
                and ingredient not in selected_ingredients
            ]

        visible_ingredients = matches[:INGREDIENT_RESULTS_LIMIT]
        st.caption("Matching dataset ingredients" if search_term else "Popular ingredients")
        if visible_ingredients:
            ingredient_columns = st.columns(3)
            for index, ingredient in enumerate(visible_ingredients):
                with ingredient_columns[index % len(ingredient_columns)]:
                    st.button(
                        ingredient.title(),
                        key=f"available_{ingredient}",
                        icon=":material/add:",
                        on_click=toggle_ingredient,
                        args=(ingredient,),
                        width="stretch",
                    )
            if len(matches) > INGREDIENT_RESULTS_LIMIT:
                st.caption(
                    f"Showing {INGREDIENT_RESULTS_LIMIT} of {len(matches)}. "
                    "Refine your search to see more."
                )
        elif search_term:
            st.caption("No dataset match. You can still add it below.")

        ingredients_text = st.text_input(
            "Or enter ingredients (comma separated)",
            placeholder="Example: onion, tomato, potato, cumin",
            key="custom_ingredients",
        )
        if st.button(
            "Generate recipe",
            type="primary",
            icon=":material/auto_awesome:",
            key="find_best_recipe",
            width="stretch",
        ):
            ingredients = list(selected_ingredients)
            ingredients.extend(
                ingredient.strip()
                for ingredient in ingredients_text.split(",")
                if ingredient.strip()
            )
            ingredients = list(
                dict.fromkeys(ingredient.casefold() for ingredient in ingredients)
            )

            if not ingredients:
                st.session_state["recipe_error"] = (
                    "Select or enter at least one ingredient first."
                )
                st.session_state["recipe_result"] = None
            else:
                with st.spinner("Finding your best recipe…"):
                    find_recipe(ingredients)

        if st.session_state["recipe_error"]:
            st.error(st.session_state["recipe_error"])

with results_panel:
    with st.container(border=True, key="results_panel"):
        with st.container(horizontal=True, vertical_alignment="center"):
            st.subheader(":material/soup_kitchen: Recipe results")
            if st.session_state["recipe_result"] is not None:
                st.badge(
                    "Recipe generated",
                    icon=":material/check_circle:",
                    color="green",
                )
            else:
                st.caption("Your recipe will appear here")

        result = st.session_state["recipe_result"]
        if result is None:
            st.info(
                "Choose a few ingredients, then select **Generate recipe** "
                "to see the closest match from the dataset."
            )
        elif result["status"] == "no_match":
            st.warning(result["message"])
        else:
            best = result["best_match"]
            st.markdown("#### :material/emoji_food_beverage: Best recipe match")
            with st.container(border=True, key="best_match"):
                st.subheader(best["recipe_name"])
                with st.container(horizontal=True):
                    st.badge(best["cuisine"], icon=":material/public:")
                    st.badge(best["course"], icon=":material/category:")
                    st.badge(
                        f"{best['total_time_mins']} min",
                        icon=":material/schedule:",
                    )
                    st.badge(
                        f"{best['similarity_score']}% match",
                        icon=":material/target:",
                    )
                if best["url"].startswith(("http://", "https://")):
                    st.link_button(
                        "Open original recipe",
                        best["url"],
                        icon=":material/open_in_new:",
                        type="primary",
                        key="open_source_recipe",
                        width="content",
                    )

            st.markdown("#### :material/eco: Recipe response (from dataset)")
            with st.container(border=True, key="recipe_response"):
                st.write(f"Recipe: {best['recipe_name']}")
                st.write(f"Ingredients: {best['ingredients_text']}")

            detail_columns = st.columns(2, gap="medium")
            with detail_columns[0]:
                st.markdown("#### :material/restaurant: Ingredients")
                for ingredient in best["ingredients_text"].split(","):
                    ingredient = ingredient.strip()
                    if ingredient:
                        st.markdown(f"- {ingredient}")
            with detail_columns[1]:
                st.markdown("#### :material/menu_book: Instructions")
                steps = split_instruction_steps(best["instructions"])
                if steps:
                    instructions_display = st.empty()
                    if st.session_state["animate_instructions"]:
                        revealed_steps = []
                        for index, step in enumerate(steps, start=1):
                            revealed_steps.append(f"{index}. {step}")
                            instructions_display.markdown(
                                "\n\n".join(revealed_steps)
                            )
                            if index < len(steps):
                                time.sleep(1)
                        st.session_state["animate_instructions"] = False
                    else:
                        instructions_display.markdown(
                            "\n\n".join(
                                f"{index}. {step}"
                                for index, step in enumerate(steps, start=1)
                            )
                        )
                else:
                    st.caption("No instructions are available for this recipe.")

            st.caption(
                "Times are copied from the dataset and may exclude resting or "
                "refrigeration time mentioned in the instructions."
            )
