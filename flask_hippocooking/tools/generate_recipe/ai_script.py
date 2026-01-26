import os
import json
import datetime
import tkinter as tk
from tkinter import messagebox, scrolledtext
from pathlib import Path
from google import genai
from google.genai import types

# --- CONFIGURATION ---
BASE_DIR = Path("../../static/recipes")
LANGUAGES = ["de", "en", "es", "fr"]

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
def load_api_key(filename="../../.geminikey.txt"):
    p = Path(filename)
    if not p.exists():
        return None
    return p.read_text(encoding="utf-8").strip()

# --- UTILS ---
def validate_id(recipe_id):
    """Checks if the ID is exactly 5 digits."""
    return recipe_id.isdigit() and len(recipe_id) == 5

def get_concatenated_input():
    desc = desc_input.get("1.0", tk.END).strip()
    ingr = ingr_input.get("1.0", tk.END).strip()
    inst = inst_input.get("1.0", tk.END).strip()
    
    if not desc or not ingr or not inst:
        return None
    
    return f"1. Description:\n{desc}\n\n2. Ingredients:\n{ingr}\n\n3. Instruction:\n{inst}"

# --- CORE AGENT ---
def run_agent(recipe_text, recipe_id):
    api_key = load_api_key()
    if not api_key:
        messagebox.showerror("Error", "Missing API Key in .geminikey.txt")
        return
    
    client = genai.Client(api_key=api_key)
    current_date = datetime.date.today().isoformat()
    
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
        
        messagebox.showinfo("Success", f"Recipe ID {recipe_id} generated and saved successfully.")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# --- UI LOGIC ---
def on_preview():
    text = get_concatenated_input()
    recipe_id = id_input.get().strip()
    
    if not text:
        messagebox.showwarning("Warning", "Please fill in all text fields.")
        return
    
    preview_win = tk.Toplevel(root)
    preview_win.title("Preview")
    preview_win.geometry("500x600")
    
    tk.Label(preview_win, text=f"Target Filename: {recipe_id if recipe_id else '[EMPTY ID]'}.json", font=("Arial", 10, "bold")).pack(pady=5)
    tk.Label(preview_win, text="Prompt Content:", font=("Arial", 10, "italic")).pack(pady=5)
    
    ptxt = scrolledtext.ScrolledText(preview_win, wrap=tk.WORD)
    ptxt.insert(tk.END, text)
    ptxt.config(state=tk.DISABLED)
    ptxt.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    
    tk.Button(preview_win, text="Close", command=preview_win.destroy).pack(pady=10)

def on_submit():
    text = get_concatenated_input()
    recipe_id = id_input.get().strip()
    
    if not validate_id(recipe_id):
        messagebox.showerror("Invalid ID", "The ID must be exactly a 5-digit number (e.g., 00123).")
        return
        
    if not text:
        messagebox.showwarning("Warning", "Please fill in all fields.")
        return
        
    run_agent(text, recipe_id)

# --- UI SETUP ---
root = tk.Tk()
root.title("Recipe AI Generator")
root.geometry("600x850")

# ID Field
tk.Label(root, text="Recipe ID (5 digits, e.g. 00042)", font=("Arial", 10, "bold")).pack(pady=(15, 0))
id_input = tk.Entry(root, font=("Arial", 12), justify='center')
id_input.pack(padx=20, pady=5)
id_input.insert(0, "00000") # Default placeholder

# Text Fields
tk.Label(root, text="1. Description", font=("Arial", 10, "bold")).pack(pady=(15, 0))
desc_input = scrolledtext.ScrolledText(root, height=6)
desc_input.pack(padx=20, pady=5, fill=tk.X)

tk.Label(root, text="2. Ingredients", font=("Arial", 10, "bold")).pack(pady=(15, 0))
ingr_input = scrolledtext.ScrolledText(root, height=10)
ingr_input.pack(padx=20, pady=5, fill=tk.X)

tk.Label(root, text="3. Instruction", font=("Arial", 10, "bold")).pack(pady=(15, 0))
inst_input = scrolledtext.ScrolledText(root, height=12)
inst_input.pack(padx=20, pady=5, fill=tk.X)

# Buttons
btn_frame = tk.Frame(root)
btn_frame.pack(pady=25)

tk.Button(btn_frame, text="👁 Preview Text", command=on_preview, width=15, height=2).pack(side=tk.LEFT, padx=10)
tk.Button(btn_frame, text="🚀 Generate Recipe", command=on_submit, bg="#2e7d32", fg="white", font=("Arial", 10, "bold"), width=20, height=2).pack(side=tk.LEFT, padx=10)

root.mainloop()