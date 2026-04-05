import streamlit as st
import streamlit.components.v1 as components
from color_palette_generator import generate_palette
from features import create_palette_image
from PIL import Image
import base64

st.set_page_config(page_title="SpectrumAI", page_icon=Image.open("logo3.png"), layout="wide")

def to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

bg   = to_base64("bg9.png")
logo = to_base64("logo3.png")

css = open("style.css").read()
bg_rule = f".stApp {{ background: linear-gradient(rgba(10,8,6,0.50),rgba(10,8,6,0.50)), url('data:image/jpg;base64,{bg}') center/cover fixed; }}"
st.markdown(f"<style>{css}\n{bg_rule}</style>", unsafe_allow_html=True)

st.markdown(f"""
<div class="navbar">
    <img src="data:image/png;base64,{logo}" />
    <div>
        <h1>SpectrumAI</h1>
        <p>AI Color Palette Generator</p>
    </div>
</div>
<div class="gold-line"></div>
""", unsafe_allow_html=True)

if "palette" not in st.session_state:
    st.session_state.palette = None
if "mood" not in st.session_state:
    st.session_state.mood = ""

CATEGORIES = ["Interior Design", "Fashion & Clothing", "Art & Painting",
              "Event & Party", "Nature & Outdoors", "Brand & Logo",
              "Website & UI", "Presentation", "Other"]

col1, col2, col3 = st.columns([2.5,2.5,1], gap="medium")
mood       = col1.text_input("Mood or theme", placeholder="eg. sunset, technology, happy, etc.")
category   = col2.selectbox("Category", CATEGORIES)
num_colors = col3.slider("Colors", 3, 8, 5)

st.write("")
_, btn, _ = st.columns([2, 1, 2])
if btn.button("Generate Palette :)"):
    if not mood.strip():
        st.error("Please enter a mood or theme.")
    else:
        with st.spinner("Generating…"):
            try:
                st.session_state.palette = generate_palette(mood.strip(), category, num_colors)
                st.session_state.mood = mood.strip()
            except Exception as e:
                st.error(f"Something went wrong: {e}")
if st.session_state.palette:
    palette = st.session_state.palette
    st.markdown(f"<br><p style='font-family:Cormorant Garamond,serif;font-size:1.8rem;margin:0 0 16px'>\"{st.session_state.mood}\"</p>", unsafe_allow_html=True)

    for col, color in zip(st.columns(len(palette), gap="medium"), palette):
        r, g, b = color["rgb"]
        with col:
            st.markdown(f"""
            <div class="polaroid">
                <div class="swatch" style="background:{color['hex']};"></div>
                <div class="name">{color['name']}</div>
                <div class="hex">{color['hex']}</div>
                <div class="rgb">rgb({r}, {g}, {b})</div>
                <div class="desc">{color['description']}</div>
            </div>""", unsafe_allow_html=True)

            components.html(f"""
            <button onclick="navigator.clipboard.writeText('{color['hex']}').then(()=>{{
                this.textContent='Copied!'; setTimeout(()=>this.textContent='Copy HEX',1500);
            }})" style="width:100%;background:transparent;border:1px solid rgba(201,168,76,0.35);
                color:#c9a84c;padding:7px 0;border-radius:6px;font-size:.74rem;cursor:pointer;">
            Copy HEX</button>""", height=36, scrolling=False)
    st.write("")
    st.write("")
    _, dl, _ = st.columns([1, 1, 1])
    with dl:
        st.download_button("⬇ Download PNG",
                           create_palette_image(palette),
                           file_name=f"palette_{st.session_state.mood[:20]}.png",
                           mime="image/png", use_container_width=True)  

st.divider()
st.markdown('<p class="footer">Made with ❤️ by the SpectrumAI team</p>', unsafe_allow_html=True)                