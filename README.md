# 📚 Assistant Documentaire Intelligent (RAG avec Streamlit + LangChain)

Une application **Streamlit** permettant de **poser des questions à des documents PDF** grâce à l’IA.
Le système utilise une architecture **RAG (Retrieval Augmented Generation)** avec embeddings et base vectorielle.

---

## 🚀 Fonctionnalités

✅ Upload de plusieurs fichiers PDF
✅ Extraction automatique du texte
✅ Découpage intelligent en chunks
✅ Génération d’embeddings (vectorisation)
✅ Recherche sémantique dans les documents
✅ Chat interactif basé uniquement sur le contenu des PDF
✅ Affichage optionnel des sources
✅ Interface simple et moderne

---

## 🧠 Architecture du projet

L'application repose sur :

* **Streamlit** → Interface utilisateur
* **LangChain** → Orchestration IA
* **OpenAI Embeddings** → Vectorisation du texte
* **ChromaDB** → Base vectorielle locale
* **GPT-4o** → Génération de réponses
* **PyPDF2** → Lecture des PDF

### 🔎 Pipeline RAG utilisé

1. Upload des PDF
2. Extraction du texte
3. Split en chunks
4. Création des embeddings
5. Stockage vectoriel (Chroma)
6. Recherche des passages pertinents
7. Génération de réponse basée sur contexte


## ▶️ Lancer l’application

```bash
streamlit run app.py
```

Puis ouvrir :

```
http://localhost:8501
```

---

## 🖥️ Utilisation

### Étapes :

1. Charger un ou plusieurs PDF
2. Cliquer sur **Indexer les documents**
3. Poser des questions dans le chat
4. Voir les sources si nécessaire

---

## 📊 Paramètres techniques importants

### Splitter

```
chunk_size = 512
chunk_overlap = 32
```

👉 Permet d’optimiser :

* la qualité des réponses
* la recherche sémantique

### Retriever

```
k = 5
```

👉 Nombre de passages envoyés au LLM

---

## 🧩 Prompt Engineering utilisé

Le modèle répond **uniquement avec le contexte** :

```
Réponds à la question suivante en te basant uniquement sur le contexte fourni
```

➡️ Permet :

* Réduction des hallucinations
* Réponses plus fiables

---

## 🚀 Améliorations possibles

* Sauvegarde Chroma persistante
* Authentification utilisateur
* Support PDF image (OCR)
* Streaming des réponses
* Upload DOCX / TXT / CSV
* Résumé automatique des documents
* Dashboard analytics

---

## 🧑‍💻 Auteur

**Ivan Junior Ake**

Projet réalisé dans le cadre de :

* apprentissage IA
* RAG
* LLM Apps
* Data Engineering

## 💡 Concept clé

Ce projet démontre comment construire une **application IA professionnelle** capable de :

✔️ Exploiter la connaissance contenue dans des documents
✔️ Créer un assistant intelligent métier
✔️ Implémenter une architecture RAG moderne

---




