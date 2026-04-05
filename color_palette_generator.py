import os, json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

try:
    import streamlit as st
    api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    api_key = os.environ.get("GROQ_API_KEY", "")

client = Groq(api_key=api_key)
def generate_palette(mood, category, num_colors=5):
    prompt = f"""You are a color palette creator. Create {num_colors} colors for the theme: "{mood}" (category: {category}).
First, identify "{mood}":
- Is it a CHARACTER (Batman, Elsa, Iron Man)? → Then select colors as used in their costume. Batman includes black + dark grey + yellow. Do not choose random colors.
- Is it a BRAND (Nike, Coca-Cola)? → Then pick only the actual brand colors.
- Is it a MOOD or PLACE (sunset, ocean, dark academia, forest)? → Then select colors found there. Sunset colors include warm oranges, reds, pinks, and purples. Ocean colors include blue and teal. Do not give characters and brands random colors.
The rules are strict:
- Give colors descriptive names (e.g., "Amber Orange", "Deep Navy", "Dusty Rose"), not random brands or characters, except when it comes to a specific character/brand.
- The hex code must visually correspond to the color name. For example, the hex code for an amber-orange color must be orange-like; otherwise, the app breaks.
- The {num_colors} color palette should feel like "{mood}". People should get the idea about the mood by looking at your color palette.
- Avoid selecting very similar colors.

Return ONLY a JSON array, nothing else:
[{{"name":"...","hex":"#RRGGBB","rgb":[R,G,B],"description":"one sentence connecting this color to {mood}"}}]"""
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    raw = response.choices[0].message.content.strip()
    if "```" in raw:
        for part in raw.split("```"):
            part = part.strip().lstrip("json").strip()
            if part.startswith("["):
                raw = part
                break
    if not raw.startswith("["):
        s, e = raw.find("["), raw.rfind("]")
        raw = raw[s:e+1]

    return json.loads(raw)