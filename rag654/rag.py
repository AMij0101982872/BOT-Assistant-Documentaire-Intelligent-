import streamlit as st
import base64
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from PyPDF2 import PdfReader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 1. --- CONFIGURATION ---
load_dotenv(override=True)
st.set_page_config(page_title="JR DOC | Vision", page_icon="🎨", layout="wide")

# 2. --- LOGO GÉNÉRATION ---
def generate_pop_logo():
    img_size = (400, 400)
    image = Image.new('RGBA', img_size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    # Fond carré arrondi JAUNE
    draw.rounded_rectangle([5, 5, 395, 395], radius=70, fill="#FFD700")

    # Texte JAIM — chercher la meilleure police disponible
    font = None
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
        "Arial Bold.ttf",
    ]
    for fp in font_paths:
        try:
            font = ImageFont.truetype(fp, 130)
            break
        except:
            continue
    if font is None:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), "BOT DOC", font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    x = (400 - text_w) // 2
    y = (400 - text_h) // 2 - 10
    draw.text((x, y), "BOT DOC", fill="#1a1a1a", font=font)

    # Resize to display size
    image = image.resize((200, 200), Image.LANCZOS)

    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return f"data:image/png;base64,{base64.b64encode(buffered.getvalue()).decode()}"

logo_b64 = generate_pop_logo()

# 3. --- CSS ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;700;900&display=swap');

    .stApp {{
        background: #F7F5F0 !important;
        font-family: 'Outfit', sans-serif;
    }}

    /* HEADER */
    .header-box {{
        background: linear-gradient(135deg, #FFD700 0%, #FFC200 100%);
        padding: 28px 20px;
        text-align: center;
        border-bottom: 3px solid #e6b800;
        border-radius: 0 0 20px 20px;
        margin-bottom: 30px;
        box-shadow: 0 4px 20px rgba(255,215,0,0.4);
    }}

    h1 {{
        color: #1a1a1a !important;
        font-size: 3.5rem !important;
        font-weight: 900 !important;
        margin-bottom: 0px !important;
        text-shadow: 0 2px 6px rgba(0,0,0,0.15);
    }}

    /* ==============================
       MESSAGES DE LA DISCUSSION
    ============================== */

    /* Message Utilisateur : fond or clair */
    [data-testid="stChatMessage"]:nth-child(even) {{
        background: #FFFBEA !important;
        border: 1.5px solid #FFD700 !important;
        border-radius: 14px !important;
        padding: 14px !important;
        margin-bottom: 12px !important;
        box-shadow: 0 2px 8px rgba(255,215,0,0.15) !important;
    }}

    /* Message Assistant : fond blanc */
    [data-testid="stChatMessage"]:nth-child(odd) {{
        background: #FFFFFF !important;
        border: 1.5px solid #E0E0E0 !important;
        border-radius: 14px !important;
        padding: 14px !important;
        margin-bottom: 12px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06) !important;
    }}

    /* Texte foncé lisible */
    [data-testid="stChatMessage"],
    [data-testid="stChatMessage"] p,
    [data-testid="stChatMessage"] span,
    [data-testid="stChatMessage"] div,
    [data-testid="stChatMessage"] li,
    [data-testid="stChatMessage"] strong,
    [data-testid="stChatMessage"] em {{
        color: #1a1a1a !important;
    }}

    .stMarkdown p {{
        font-size: 1.1rem !important;
        line-height: 1.7 !important;
        font-weight: 400 !important;
        color: #1a1a1a !important;
    }}

    /* ==============================
       SIDEBAR CLAIRE & ÉLÉGANTE
    ============================== */

    [data-testid="stSidebar"] {{
        background: #FFFFFF !important;
        border-right: 2px solid #FFD700 !important;
        box-shadow: 3px 0 15px rgba(0,0,0,0.08) !important;
    }}

    [data-testid="stSidebar"] > div {{
        background: #FFFFFF !important;
        padding: 24px 18px !important;
    }}

    /* Titre DOCUMENTS */
    [data-testid="stSidebar"] h2 {{
        color: #1a1a1a !important;
        font-size: 1.2rem !important;
        letter-spacing: 4px !important;
        font-weight: 900 !important;
        border-bottom: 2px solid #FFD700 !important;
        padding-bottom: 10px !important;
        margin-bottom: 20px !important;
    }}

    /* Zone d'upload */
    [data-testid="stSidebar"] [data-testid="stFileUploader"] {{
        background: #FAFAFA !important;
        border: 2px dashed #FFD700 !important;
        border-radius: 12px !important;
        padding: 15px !important;
    }}

    [data-testid="stSidebar"] [data-testid="stFileUploader"] span,
    [data-testid="stSidebar"] [data-testid="stFileUploader"] p,
    [data-testid="stSidebar"] [data-testid="stFileUploader"] small {{
        color: #555555 !important;
    }}

    /* Bouton Browse files */
    [data-testid="stSidebar"] [data-testid="stFileUploader"] button {{
        background: transparent !important;
        border: 1.5px solid #FFD700 !important;
        color: #1a1a1a !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        transition: all 0.2s ease !important;
    }}

    [data-testid="stSidebar"] [data-testid="stFileUploader"] button:hover {{
        background: #FFD700 !important;
        color: #000 !important;
    }}

    /* Fichier uploadé */
    [data-testid="stSidebar"] [data-testid="stFileUploaderFile"] {{
        background: #FFFBEA !important;
        border: 1px solid #FFD700 !important;
        border-radius: 8px !important;
        color: #1a1a1a !important;
        margin-top: 10px !important;
        padding: 8px !important;
    }}

    /* BOUTON LANCER L'INDEXATION */
    .stButton>button {{
        background: linear-gradient(135deg, #FFD700, #FFA500) !important;
        color: #000000 !important;
        font-weight: 900 !important;
        font-size: 0.95rem !important;
        letter-spacing: 2px !important;
        border-radius: 12px !important;
        border: none !important;
        width: 100% !important;
        padding: 14px !important;
        margin-top: 15px !important;
        box-shadow: 0 4px 20px rgba(255, 215, 0, 0.4) !important;
        transition: all 0.2s ease !important;
    }}

    .stButton>button:hover {{
        box-shadow: 0 6px 30px rgba(255, 215, 0, 0.7) !important;
        transform: translateY(-2px) !important;
    }}

    /* Zone de saisie en bas */
    .stChatInputContainer {{
        padding: 10px !important;
        background: #FFFFFF !important;
        border-top: 2px solid #FFD700 !important;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.06) !important;
    }}

    /* Espacement pour que le dernier message ne soit pas caché par l'input */
    .block-container {{
        padding-bottom: 150px !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# 4. --- LOGIQUE ---
llm = ChatOpenAI(model="gpt-4o", temperature=0)

def main():
    # --- UI HEADER ---
    st.markdown(f"""
    <div class="header-box">
        <h1>JR DOC</h1>
        <p style="color:#1a1a1a; letter-spacing:3px; font-weight:700;">ANALYSES DOCUMENTAIRES HAUTE PRÉCISION</p>
    </div>
    """, unsafe_allow_html=True)

    # --- SIDEBAR ---
    with st.sidebar:
        st.markdown("""
            <div style="
                background: linear-gradient(135deg, #FFD700, #FFA500);
                border-radius: 16px;
                padding: 22px 16px;
                margin-bottom: 20px;
                text-align: center;
                box-shadow: 0 4px 15px rgba(255,215,0,0.3);
            ">
                <div style="font-size: 2rem; font-weight: 900; color: #1a1a1a; letter-spacing: 6px;">BOT DOC </div>
                <div style="font-size: 0.7rem; font-weight: 700; color: #1a1a1a; letter-spacing: 3px; margin-top: 4px; opacity: 0.7;">DOCUMENT ANALYSER</div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("<h2 style='color:#FFD700'>DOCUMENTS</h2>", unsafe_allow_html=True)
        files = st.file_uploader("Fichiers PDF", type="pdf", accept_multiple_files=True, label_visibility="collapsed")
        
        if st.button("LANCER L'INDEXATION"):
            if files:
                with st.spinner("Traitement..."):
                    # ✅ RESET COMPLET : vider l'ancienne mémoire
                    if "retriever" in st.session_state:
                        del st.session_state.retriever
                    if "history" in st.session_state:
                        st.session_state.history = []

                    text = ""
                    for f in files:
                        r = PdfReader(f)
                        for p in r.pages: text += p.extract_text() or ""
                    chunks = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100).split_text(text)
                    
                    # ✅ Nouveau Chroma en mémoire vive à chaque fois
                    vector_db = Chroma.from_texts(
                        chunks, 
                        OpenAIEmbeddings(),
                        collection_name="session_" + str(id(files))  # collection unique
                    )
                    st.session_state.retriever = vector_db.as_retriever(search_kwargs={"k": 4})
                st.success("✅ NOUVEAU DOCUMENT CHARGÉ — mémoire réinitialisée")

    # --- CHAT AREA ---
    if "history" not in st.session_state: 
        st.session_state.history = []

    for m in st.session_state.history:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    if query := st.chat_input("Posez votre question ici..."):
        if "retriever" not in st.session_state:
            st.error("Indexez vos documents dans la barre latérale d'abord.")
            return

        st.session_state.history.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.markdown(query)

        with st.chat_message("assistant"):
            docs = st.session_state.retriever.invoke(query)
            context = "\n\n".join([d.page_content for d in docs])
            response = llm.invoke(f"Contexte: {context}\n\nQuestion: {query}")
            
            st.markdown(response.content)
            
            with st.expander("Consulter les extraits sources"):
                for d in docs:
                    st.info(d.page_content[:500] + "...")
        
        st.session_state.history.append({"role": "assistant", "content": response.content})

if __name__ == "__main__":
    main()
