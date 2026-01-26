import os
import json
import datetime
from pathlib import Path
from google import genai
from google.genai import types

# --- CONFIGURATION ---
BASE_DIR = Path("./static/recipes")
INPUT_FILE = Path("recipe_input.txt")
LANGUAGES = ["de", "en", "es", "fr"]

# Taxonomy definition for the prompt
TAXONOMY = {
    "categories": {
        "de": ["Vorspeise", "Hauptspeise", "Dessert", "Kuchen", "Kekse", "Frühstück"],
        "en": ["Appetizer", "Main Course", "Dessert", "Cake", "Cookies", "Breakfast"],
        "es": ["Entrante", "Plato Principal", "Postre", "Pastel", "Galletas", "Desayuno"],
        "fr": ["Entrée", "Plat Principal", "Dessert", "Gâteau", "Biscuits", "Petit Déjeuner"]
    },
    "cuisines": {
        "de": ["Indisch", "Deutsch", "Italienisch", "Chinesisch", "Mexikanisch"],
        "en": ["Indian", "German", "Italian", "Chinese", "Mexican"],
        "es": ["India", "Alemana", "Italiana", "China", "Mexicana"],
        "fr": ["Indienne", "Allemande", "Italienne", "Chinoise", "Mexicaine"]
    },
    "keywords": {
        "de": ["Gesund", "Schnell", "Vegetarisch", "Vegan", "Einfach"],
        "en": ["Healthy", "Quick", "Vegetarian", "Vegan", "Easy"],
        "es": ["Saludable", "Rápido", "Vegetariano", "Vegano", "Fácil"],
        "fr": ["Sain", "Rapide", "Végétarien", "Végétalien", "Facile"]
    }
}

# --- API KEY LOADER ---
def load_api_key(filename=".geminikey.txt"):
    p = Path(filename)
    if not p.exists():
        print(f"❌ Error: {filename} not found.")
        return None
    return p.read_text(encoding="utf-8").strip()

# --- UTILS ---
def get_next_recipe_id():
    """Checks all language folders to find the absolute highest ID."""
    existing_ids = []
    for lang in LANGUAGES:
        path = BASE_DIR / lang
        if path.exists():
            existing_ids.extend([int(f.stem) for f in path.glob("*.json") if f.stem.isdigit()])
    
    next_num = max(existing_ids) + 1 if existing_ids else 0
    return f"{next_num:05d}"

# --- CORE AGENT ---
def run_agent():
    api_key = load_api_key()
    if not api_key:
        print("🛑 Script stopped: Missing API Key.")
        return
    
    client = genai.Client(api_key=api_key)

    if not INPUT_FILE.exists():
        print(f"❌ Error: {INPUT_FILE} not found.")
        return

    recipe_text = INPUT_FILE.read_text(encoding="utf-8")
    recipe_id = get_next_recipe_id()
    current_date = datetime.date.today().isoformat()
    
    print(f"🚀 Analyzing ID {recipe_id} with Gemini 2.0 Flash...")

    # Reference structure for the AI
    example_format = {
        "@context": "https://schema.org",
        "@type": "Recipe",
        "name": "Recipe Name",
        "author": {"@type": "Person", "name": "Daniel"},
        "datePublished": current_date,
        "description": "Full storytelling intro...",
        "descriptionShort": "Short summary...",
        "prepTime": "PT10M",
        "cookTime": "PT0M",
        "totalTime": "PT10M",
        "recipeYield": "1 serving",
        "recipeCategory": "Category from Taxonomy",
        "recipeCuisine": "Cuisine from Taxonomy",
        "keywords": "Keyword1, Keyword2 from Taxonomy",
        "recipeIngredient": ["item 1"],
        "recipeInstructions": [{"@type": "HowToStep", "name": "Title", "text": "Details"}],
        "nutrition": {
            "@type": "NutritionInformation",
            "calories": "0 kcal",
            "proteinContent": "0 g",
            "carbohydrateContent": "0 g",
            "fatContent": "0 g",
            "servingSize": "1",
            "servingCalories": "0 kcal"
        }
    }

    # Integration of your specific 11-point requirements
    master_prompt = f"""
        Act as a professional Culinary Data Analyst.
        Convert the input text into a structured JSON for these languages: {", ".join(LANGUAGES)}.

        STRICT INSTRUCTIONS:
        1. OUTPUT FORMAT: A single JSON object with language codes as top-level keys: {LANGUAGES}.
        2. DATA INTEGRITY: You MUST include the full 'description' (storytelling) and a 'descriptionShort'.
        3. TAXONOMY: 
           - recipeCategory MUST be one of: {json.dumps(TAXONOMY['categories'])}
           - recipeCuisine MUST be one of: {json.dumps(TAXONOMY['cuisines'])}
           - keywords MUST be a comma-separated string from: {json.dumps(TAXONOMY['keywords'])}
           Note: Use the correct translated value for each language based on the taxonomy index.
        4. DATE: Use '{current_date}' for datePublished.
        5. SPELLING: Make sure that the spelling is correct in all languages.
        6. DERIVE: Estimate prepTime, cookTime, totalTime (ISO 8601), and recipeYield.
        7. NUTRITION: Estimate calories, proteinContent, carbohydrateContent, fatContent, servingCalories.
        8. SERVING SIZE: For the Nutrition, assume always a servingSize of 1.
        9. NO NULLS: If a value cannot be derived, provide a best-guess estimate based on culinary standards rather than leaving it null.
        10. STYLE: Preserve the personal, emotional tone of the original description.
        11. LOCALIZATION: Translate EVERYTHING that is a string value. 
            - For 'recipeYield', use 'Portionen' (DE), 'servings' (EN), 'raciones' (ES), 'portions' (FR).
            - Ensure ingredients and instructions are fully translated, not just the name.

        REFERENCE STRUCTURE:
        {json.dumps(example_format, indent=2)}

        INPUT TEXT:
        {recipe_text}
    """

    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=master_prompt,
            config=types.GenerateContentConfig(
                response_mime_type='application/json',
                temperature=0.2,
                top_p=0.95
            )
        )
        
        all_languages_json = json.loads(response.text)

        for lang in LANGUAGES:
            if lang in all_languages_json:
                target_folder = BASE_DIR / lang
                target_folder.mkdir(parents=True, exist_ok=True)
                
                file_path = target_folder / f"{recipe_id}.json"
                
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(all_languages_json[lang], f, indent=2, ensure_ascii=False)
                
                print(f"✅ Saved: {file_path}")
            else:
                print(f"⚠️ Warning: Language '{lang}' missing in AI response.")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    run_agent()