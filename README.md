# Assistant Documentaire Intelligent — RAG avec Streamlit et LangChain

Une application Streamlit permettant de poser des questions sur des documents PDF grâce à l'IA.
Le système repose sur une architecture RAG (Retrieval Augmented Generation) combinant embeddings et base vectorielle.

---

## Table des matières

- [Fonctionnalites](#fonctionnalites)
- [Architecture](#architecture)
- [Installation](#installation)
- [Lancer l'application](#lancer-lapplication)
- [Utilisation](#utilisation)
- [Parametres techniques](#parametres-techniques)
- [Prompt Engineering](#prompt-engineering)
- [Ameliorations possibles](#ameliorations-possibles)
- [Auteur](#auteur)

---

## Fonctionnalites

- Upload de plusieurs fichiers PDF
- Extraction automatique du texte
- Decoupage intelligent en chunks
- Generation d'embeddings (vectorisation)
- Recherche semantique dans les documents
- Chat interactif base uniquement sur le contenu des PDF
- Affichage optionnel des sources
- Interface simple et moderne

---

## Architecture

L'application repose sur les composants suivants :

| Composant | Role |
|---|---|
| Streamlit | Interface utilisateur |
| LangChain | Orchestration IA |
| OpenAI Embeddings | Vectorisation du texte |
| ChromaDB | Base vectorielle locale |
| GPT-4o | Generation de reponses |
| PyPDF2 | Lecture des fichiers PDF |

### Pipeline RAG
```
1. Upload des PDF
2. Extraction du texte
3. Split en chunks
4. Creation des embeddings
5. Stockage vectoriel (Chroma)
6. Recherche des passages pertinents
7. Generation de reponse basee sur le contexte
```

---

## Installation

1. Cloner le depot :
```bash
git clone https://github.com/votre-utilisateur/rag-assistant.git
cd rag-assistant
```

2. Installer les dependances :
```bash
pip install -r requirements.txt
```

3. Creer un fichier `.env` a la racine :
```env
OPENAI_API_KEY=your_openai_api_key
```

---

## Lancer l'application
```bash
streamlit run app.py
```

Puis ouvrir dans le navigateur :
```
http://localhost:8501
```

---

## Utilisation

1. Charger un ou plusieurs fichiers PDF via l'interface
2. Cliquer sur **Indexer les documents**
3. Poser des questions dans le chat
4. Consulter les sources si necessaire

---

## Parametres techniques

### Splitter
```python
chunk_size    = 512
chunk_overlap = 32
```

Ces parametres permettent d'optimiser la qualite des reponses et la precision de la recherche semantique.

### Retriever
```python
k = 5
```

Nombre de passages extraits et envoyes au LLM comme contexte pour chaque question.

---

## Prompt Engineering

Le modele est contraint de repondre uniquement a partir du contexte fourni :
```
Reponds a la question suivante en te basant uniquement sur le contexte fourni.
```

Cette approche permet de reduire les hallucinations et d'obtenir des reponses plus fiables et tracables.

---

## Ameliorations possibles

- Sauvegarde Chroma persistante entre les sessions
- Authentification utilisateur
- Support PDF image via OCR
- Streaming des reponses
- Upload de fichiers DOCX, TXT et CSV
- Resume automatique des documents
- Dashboard analytics

---

## Auteur

**Ivan Junior Ake**

Projet realise dans le cadre d'un apprentissage personnel autour des themes suivants :
intelligence artificielle, RAG, applications LLM et Data Engineering.

---

## Concept cle

Ce projet demontre comment construire une application IA professionnelle capable d'exploiter
la connaissance contenue dans des documents, de creer un assistant metier intelligent
et d'implementer une architecture RAG moderne et maintenable.
