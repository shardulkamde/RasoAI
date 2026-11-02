# RasoAI - Local Recipe Finder (Excel Dataset + FastAPI + Streamlit)

## Project Overview
RasoAI is a local recipe finder that suggests recipes based on user-provided ingredients.

The system loads an Indian food dataset from an Excel file (`IndianFoodDatasetXLS.xlsx`), matches the supplied ingredients, and returns recipe details and instructions directly from the dataset. Recipe instructions are not rewritten by an LLM.

This project works offline once its Python dependencies and dataset are available.

---

## Features
- Loads Indian recipe dataset directly from Excel (`.xlsx`)
- Accepts ingredients from user input (comma-separated)
- Finds the best matching recipe from the dataset
- Uses ingredient matching with limited fuzzy matching for spelling variations
- Shows a match score based on ingredient overlap and requires at least half of the entered ingredients to match
- Offers searchable ingredient buttons based on the loaded dataset, alongside custom ingredient entry
- Returns recipe instructions verbatim from the dataset
- Clean web interface using Streamlit
- API-based backend using FastAPI

---

## Tech Stack
- Python 3.10+
- FastAPI (Backend API Server)
- Streamlit (Frontend UI)
- RapidFuzz (Fuzzy matching engine)
- Pandas + OpenPyXL (Excel file processing)

---

## Project Structure
```
RasoAI/
│
├── backend/
│   ├── main.py
│   ├── dataset_loader.py
│   ├── recipe_retriever.py
│   ├── utils.py
│   ├── data/
│   │   └── IndianFoodDatasetXLS.xlsx
│   ├── requirements.txt
│
├── frontend/
│   ├── .streamlit/
│   │   └── config.toml
│   ├── static/
│   │   └── background.mp4
│   ├── web_ui.py
│   ├── requirements.txt
│
└── README.md
```

---

## Dataset Requirement
This project requires the Indian Food Excel dataset file.

Place the dataset here:

```
backend/data/IndianFoodDatasetXLS.xlsx
```

Dataset Columns Used:
- Srno
- RecipeName
- Ingredients
- Instructions
- Cuisine
- Course
- Diet
- PrepTimeInMins
- CookTimeInMins
- TotalTimeInMins
- Servings
- URL

---

# Setup Instructions (Windows/Linux)

## Step 1: Install Python
Make sure Python 3.10+ is installed.

Check version:
```bash
python --version
```

---

# Installation Commands

## Backend Installation
Go to backend folder:

```bash
cd backend
```

Install backend dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

---

## Frontend Installation
Go to frontend folder:

```bash
cd frontend
```

Install frontend dependencies:

```bash
python -m pip install -r requirements.txt
```

---

# How to Run the Project

## Step 1: Start Backend API (FastAPI)
Open Terminal 1:

```bash
cd backend
python -m uvicorn main:app --reload
```

Backend will run at:

```
http://127.0.0.1:8000
```

Swagger API Docs:

```
http://127.0.0.1:8000/docs
```

---

## Step 2: Start Frontend UI (Streamlit)
Open Terminal 2:

```bash
cd frontend
streamlit run web_ui.py
```

Streamlit UI will run at:

```
http://localhost:8501
```

The UI uses `frontend/static/background.mp4` as a muted, looping background video.
Replace that file to use a different clip.

---

# Sample Input and Expected Output

## Sample Input
User enters in Streamlit textbox:

```
egg
```

OR

```
onion, tomato
```

---

## Expected Output
The UI will display:

### 1. Recipe response
The response contains the selected recipe name, ingredients, and instructions exactly as stored in the dataset.

### 2. Best Recipe Match Details
- Recipe Name
- Cuisine
- Course
- Diet
- Total Time
- Similarity Score
- URL

The listed time is copied from the dataset and may not include resting or refrigeration time mentioned in the instructions.

### 3. Dataset Ingredients and Instructions
Ingredients and full instructions will be displayed below the recipe details.

---

# API Usage (Verification)

## Endpoint
```
POST /chat
```

Available ingredient choices for the UI:
```
GET /ingredients
```

In the Streamlit app, search for an ingredient and click its button to add or
remove it. You can also enter comma-separated ingredients that are not in the
suggestions.

## Sample Request Body
```json
{
  "ingredients": ["egg"]
}
```

## Sample Response Output (JSON)
```json
{
  "status": "success",
  "best_match": {
    "recipe_name": "How To Boil Eggs At Home - Boiled Eggs Recipe",
    "cuisine": "Continental",
    "total_time_mins": 10,
    "similarity_score": 33.33
  },
  "chatbot_response": "..."
}
```

---

# Common Issues and Fixes

## Issue: "No recipe found matching at least half of the given ingredients"
Reason: Fewer than half of the entered ingredients match the dataset.
Fix: Check ingredient spellings or try common dataset ingredients like:
- onion
- tomato
- egg
- potato
- rice
- paneer

---



# AI Assistance Disclosure (Efficiency Improvement)
This project was developed with assistance from AI tools (ChatGPT) to improve development efficiency, code structuring, and modular design.

AI support was used for:
- Generating initial project structure
- Writing modular backend and frontend code
- Improving fuzzy matching logic using RapidFuzz
- Writing professional documentation

All generated code was reviewed, tested, and manually modified to ensure correctness and successful execution.

---

# Author
Nikhil Kota
