import os
import json
import datetime
import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from google import genai
from google.genai import types

# --- CONFIGURATION ---
BASE_DIR = Path("../../static/recipes")
IMAGE_SAVE_DIR = Path("../../static/recipes_images")
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

# --- IMAGE PROCESSING ---

def add_watermark(image, watermark_text="Hippocooking.com"):
    width, height = image.size
    draw = ImageDraw.Draw(image)
    font_size = int(height * 0.05)
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()
    
    bbox = draw.textbbox((0, 0), watermark_text, font=font)
    text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = 10
    y = height - text_height - 30

    watermark_image = Image.new("RGBA", image.size, (0, 0, 0, 0))
    watermark_draw = ImageDraw.Draw(watermark_image)
    watermark_draw.text((x, y), watermark_text, font=font, fill=(255, 255, 255, 128))

    watermarked_image = Image.alpha_composite(image.convert("RGBA"), watermark_image)
    return watermarked_image.convert("RGB")

def scale_image(image, target_width=1440):
    width, height = image.size
    aspect_ratio = height / width
    new_height = int(target_width * aspect_ratio)
    return image.resize((target_width, new_height), Image.Resampling.LANCZOS)

def process_and_save_image(source_path, recipe_id):
    try:
        IMAGE_SAVE_DIR.mkdir(parents=True, exist_ok=True)
        output_path = IMAGE_SAVE_DIR / f"{recipe_id}.jpg"
        with Image.open(source_path) as img:
            scaled_img = scale_image(img)
            watermarked_img = add_watermark(scaled_img)
            watermarked_img.save(output_path, "JPEG", quality=85, optimize=True)
        return True
    except Exception as e:
        print(f"Fehler bei Bildverarbeitung: {e}")
        return False

# --- UTILS ---
def load_api_key(filename="../../.geminikey.txt"):
    p = Path(filename)
    return p.read_text(encoding="utf-8").strip() if p.exists() else None

def validate_id(recipe_id):
    return recipe_id.isdigit() and len(recipe_id) == 5

def get_concatenated_input():
    author = author_input.get().strip()
    desc = desc_input.get("1.0", tk.END).strip()
    ingr = ingr_input.get("1.0", tk.END).strip()
    inst = inst_input.get("1.0", tk.END).strip()
    
    if not desc or not ingr or not inst:
        return None
    
    return f"Author: {author if author else 'Daniel'}\n\n1. Description:\n{desc}\n\n2. Ingredients:\n{ingr}\n\n3. Instruction:\n{inst}"

# --- CORE AGENT ---
def run_agent(recipe_text, recipe_id, author_name, source_image_path):
    api_key = load_api_key()
    if not api_key:
        messagebox.showerror("Error", "Missing API Key in .geminikey.txt")
        return
    
    image_processed = False
    if source_image_path:
        image_processed = process_and_save_image(source_image_path, recipe_id)

    client = genai.Client(api_key=api_key)
    current_date = datetime.date.today().isoformat()
    
    example_format = {
        "@context": "https://schema.org",
        "@type": "Recipe",
        "name": "Recipe Name",
        "author": {"@type": "Person", "name": author_name if author_name else "Daniel"},
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
        12. AUTHOR: Use the name '{author_name if author_name else 'Daniel'}' for the author field in all recipe versions.

        REFERENCE STRUCTURE:
        {json.dumps(example_format, indent=2)}

        INPUT TEXT:
        {recipe_text}
    """

    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=master_prompt,
            config=types.GenerateContentConfig(response_mime_type='application/json', temperature=0.2, top_p=0.95)
        )
        
        all_languages_json = json.loads(response.text)

        for lang in LANGUAGES:
            if lang in all_languages_json:
                target_folder = BASE_DIR / lang
                target_folder.mkdir(parents=True, exist_ok=True)
                with open(target_folder / f"{recipe_id}.json", "w", encoding="utf-8") as f:
                    json.dump(all_languages_json[lang], f, indent=2, ensure_ascii=False)
        
        msg = f"Recipe ID {recipe_id} generated."
        if source_image_path:
            msg += "\nImage processed." if image_processed else "\nIMAGE ERROR."
        messagebox.showinfo("Success", msg)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# --- UI LOGIC ---

def select_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    if file_path:
        image_path_entry.delete(0, tk.END)
        image_path_entry.insert(0, file_path)

def on_preview():
    text = get_concatenated_input()
    recipe_id = id_input.get().strip()
    
    if not text:
        messagebox.showwarning("Warning", "Please fill in all text fields.")
        return
    
    preview_win = tk.Toplevel(root)
    preview_win.title("Preview")
    preview_win.geometry("500x650")
    
    tk.Label(preview_win, text=f"Target Filename: {recipe_id if recipe_id else '[EMPTY]'}.json", font=("Arial", 10, "bold")).pack(pady=5)
    tk.Label(preview_win, text="Full Prompt Content:", font=("Arial", 10, "italic")).pack(pady=5)
    
    ptxt = scrolledtext.ScrolledText(preview_win, wrap=tk.WORD)
    ptxt.insert(tk.END, text)
    ptxt.config(state=tk.DISABLED)
    ptxt.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    
    tk.Button(preview_win, text="Close Preview", command=preview_win.destroy).pack(pady=10)

def on_submit():
    text = get_concatenated_input()
    recipe_id = id_input.get().strip()
    author = author_input.get().strip()
    source_img = image_path_entry.get().strip()
    
    if not validate_id(recipe_id):
        messagebox.showerror("Invalid ID", "The ID must be exactly 5 digits.")
        return
    if not text:
        messagebox.showwarning("Warning", "Please fill in all recipe fields.")
        return
    run_agent(text, recipe_id, author, source_img)

# --- UI SETUP ---
root = tk.Tk()
root.title("Recipe AI & Image Manager")
root.geometry("600x980")

# Header: ID & Author
header_frame = tk.Frame(root)
header_frame.pack(pady=10, padx=20, fill=tk.X)

tk.Label(header_frame, text="ID (5 digits)", font=("Arial", 9, "bold")).grid(row=0, column=0, sticky='w', padx=5)
id_input = tk.Entry(header_frame, font=("Arial", 11), width=10, justify='center')
id_input.grid(row=1, column=0, padx=5, pady=5)
id_input.insert(0, "00000")

tk.Label(header_frame, text="Author", font=("Arial", 9, "bold")).grid(row=0, column=1, sticky='w', padx=5)
author_input = tk.Entry(header_frame, font=("Arial", 11), width=25)
author_input.grid(row=1, column=1, padx=5, pady=5)
author_input.insert(0, "Daniel")

# Image
tk.Label(root, text="Recipe Image (Optional)", font=("Arial", 10, "bold")).pack(pady=(5, 0))
img_frame = tk.Frame(root)
img_frame.pack(padx=20, pady=5, fill=tk.X)
image_path_entry = tk.Entry(img_frame, font=("Arial", 10))
image_path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
tk.Button(img_frame, text="Browse...", command=select_image).pack(side=tk.RIGHT, padx=5)

# Text Inputs
tk.Label(root, text="1. Description", font=("Arial", 10, "bold")).pack(pady=(10, 0))
desc_input = scrolledtext.ScrolledText(root, height=5)
desc_input.pack(padx=20, pady=5, fill=tk.X)

tk.Label(root, text="2. Ingredients", font=("Arial", 10, "bold")).pack(pady=(10, 0))
ingr_input = scrolledtext.ScrolledText(root, height=8)
ingr_input.pack(padx=20, pady=5, fill=tk.X)

tk.Label(root, text="3. Instruction", font=("Arial", 10, "bold")).pack(pady=(10, 0))
inst_input = scrolledtext.ScrolledText(root, height=10)
inst_input.pack(padx=20, pady=5, fill=tk.X)

# Buttons
btn_frame = tk.Frame(root)
btn_frame.pack(pady=20)

tk.Button(btn_frame, text="👁 Preview Text", command=on_preview, width=15, height=2).pack(side=tk.LEFT, padx=10)
tk.Button(btn_frame, text="🚀 Generate & Save", command=on_submit, bg="#2e7d32", fg="white", font=("Arial", 11, "bold"), width=20, height=2).pack(side=tk.LEFT, padx=10)

root.mainloop()