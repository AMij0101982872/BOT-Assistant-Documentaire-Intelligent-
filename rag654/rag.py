import streamlit as st
from PyPDF2 import PdfReader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv(override=True)

# Configuration de la page
st.set_page_config(page_title="Assistant PDF Intelligent", page_icon="📚", layout="centered")

# Style CSS personnalisé pour affiner l'interface
st.markdown("""
    <style>
    .stApp {
        background-color: #f8f9fa;
    }
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #007bff;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

prompt_template = """
Réponds à la question suivante en te basant uniquement sur le contexte fourni :
<context>
    {context}
</context>
<question>
    {input}
</question>
"""

llm = ChatOpenAI(model="gpt-4o", temperature=0)

def main():
    # --- HEADER ---
    st.title("📚 JR DOC")
    st.markdown("Posez des questions à vos documents PDF en toute simplicité.")
    st.divider()

    # --- SIDEBAR: GESTION DES FICHIERS ---
    with st.sidebar:
        st.header("⚙️ Configuration")
        pdf_docs = st.file_uploader("Étape 1 : Chargez vos PDFs", accept_multiple_files=True, type="pdf")
        
        if st.button("Indexer les documents"):
            if pdf_docs:
                with st.status("Traitement des documents...", expanded=True) as status:
                    st.write("Extraction du texte...")
                    content = ""
                    for pdf in pdf_docs:
                        reader = PdfReader(pdf)
                        for page in reader.pages:
                            content += page.extract_text()

                    st.write("Découpage en blocs...")
                    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
                        chunk_size=512, chunk_overlap=32
                    )
                    chunks = splitter.split_text(content)

                    st.write("Génération des embeddings...")
                    embedding_model = OpenAIEmbeddings()
                    vector_store = Chroma.from_texts(
                        chunks,
                        embedding_model,
                        collection_name="data_collection",
                    )
                    
                    st.session_state.retriever = vector_store.as_retriever(search_kwargs={"k": 5})
                    status.update(label="Indexation terminée !", state="complete", expanded=False)
                st.success("Documents prêts pour l'analyse.")
            else:
                st.error("Veuillez charger au moins un fichier PDF.")

    # --- ZONE DE CHAT ---
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Affichage de l'historique
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Entrée utilisateur
    if user_question := st.chat_input("Posez votre question ici..."):
        if "retriever" not in st.session_state:
            st.warning("Veuillez d'abord indexer vos documents dans la barre latérale.")
            return

        # Afficher le message utilisateur
        st.session_state.messages.append({"role": "user", "content": user_question})
        with st.chat_message("user"):
            st.markdown(user_question)

        # Générer la réponse
        with st.chat_message("assistant"):
            with st.spinner("Recherche dans les documents..."):
                context_docs = st.session_state.retriever.invoke(user_question)
                context_text = "\n\n".join([d.page_content for d in context_docs])
                
                full_prompt = prompt_template.format(context=context_text, input=user_question)
                response = llm.invoke(full_prompt)
                
                st.markdown(response.content)
                
                # Optionnel : Afficher les sources en petit
                with st.expander("Voir les sources extraites"):
                    for i, doc in enumerate(context_docs):
                        st.caption(f"Source {i+1}: {doc.page_content[:200]}...")

        st.session_state.messages.append({"role": "assistant", "content": response.content})

if __name__ == "__main__":
    main()