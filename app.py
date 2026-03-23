import streamlit as st
import random

st.set_page_config(
    page_title="Frans Methode – A0 naar A1",
    page_icon="🇫🇷",
    layout="centered"
)

# ---------- Data: hoofdstukken & oefeningen ----------

CHAPTERS = [
    {
        "id": 1,
        "title": "1. Basis zinsbouw (S–V–O)",
        "theory": """
### Doel van dit hoofdstuk

Je leert hoe een **eenvoudige Franse zin** is opgebouwd:

- Onderwerp (wie?)  
- Werkwoord (wat doet die persoon?)  
- Rest van de zin (wat / waar / wanneer)

**In het Frans is de basis volgorde net als in het Nederlands:**  
**Onderwerp – Werkwoord – Rest (S–V–O)**

Voorbeelden:

- **Je parle français.** → Ik spreek Frans.  
- **Tu habites à Paris.** → Jij woont in Parijs.  
- **Il travaille à la maison.** → Hij werkt thuis.
""",
        "examples": [
            ("Je parle français.", "Ik spreek Frans."),
            ("Tu habites à Paris.", "Jij woont in Parijs."),
            ("Elle travaille à Londres.", "Zij werkt in Londen."),
        ],
        "exercises": [
            {
                "type": "order",
                "instruction_nl": "Zet de delen in de goede Franse volgorde (S–V–O).",
                "parts": ["français", "je", "parle"],
                "correct": ["je", "parle", "français"],
                "explanation": "In het Frans komt het onderwerp (je) eerst, dan het werkwoord (parle), dan de rest (français)."
            },
            {
                "type": "order",
                "instruction_nl": "Zet de delen in de goede Franse volgorde (S–V–O).",
                "parts": ["à Paris", "tu", "habites"],
                "correct": ["tu", "habites", "à Paris"],
                "explanation": "Onderwerp **tu**, werkwoord **habites**, rest **à Paris**."
            },
        ],
    },
    {
        "id": 2,
        "title": "2. Persoonlijke voornaamwoorden",
        "theory": """
### Doel van dit hoofdstuk

Je leert de **persoonlijke voornaamwoorden** in het Frans:

- je → ik  
- tu → jij (informeel)  
- il → hij  
- elle → zij  
- nous → wij  
- vous → jullie / u  
- ils → zij (mannelijk of gemengd)  
- elles → zij (vrouwelijke groep)

Voorbeeldzinnen:

- **Je parle.** → Ik spreek.  
- **Nous habitons à Amsterdam.** → Wij wonen in Amsterdam.  
- **Elles travaillent à Rotterdam.** → Zij werken in Rotterdam (vrouwelijke groep).
""",
        "examples": [
            ("je", "ik"),
            ("nous", "wij"),
            ("vous", "jullie / u"),
        ],
        "exercises": [
            {
                "type": "mc",
                "question_nl": "Welk Frans voornaamwoord hoort bij: \"zij (vrouwelijke groep)\"?",
                "options": ["ils", "elles", "elle", "vous"],
                "answer": "elles",
                "explanation": "Voor een vrouwelijke meervoudsgroep gebruik je **elles**."
            },
            {
                "type": "mc",
                "question_nl": "Welk Frans voornaamwoord hoort bij: \"wij\"?",
                "options": ["tu", "vous", "nous", "ils"],
                "answer": "nous",
                "explanation": "Voor \"wij\" gebruik je **nous**."
            },
        ],
    },
    {
        "id": 3,
        "title": "3. Lidwoorden en gender",
        "theory": """
### Doel van dit hoofdstuk

Je leert de **bepaald lidwoord** en **onbepaald lidwoord** in het Frans.

- **Bepaald lidwoord (de / het):**  
  - le → de/het (mannelijk enkelvoud)  
  - la → de/het (vrouwelijk enkelvoud)  
  - les → de (meervoud)

- **Onbepaald lidwoord (een):**  
  - un → een (mannelijk)  
  - une → een (vrouwelijk)

Voorbeelden:

- **le livre** → het boek  
- **la maison** → het huis  
- **un livre** → een boek  
- **une maison** → een huis
""",
        "examples": [
            ("le livre", "het boek"),
            ("la maison", "het huis"),
            ("les tables", "de tafels"),
        ],
        "exercises": [
            {
                "type": "mc",
                "question_nl": "Kies het juiste lidwoord: ___ maison (huis, vrouwelijk).",
                "options": ["le", "la", "un", "une"],
                "answer": "la",
                "explanation": "Maison is vrouwelijk, dus **la maison**."
            },
            {
                "type": "mc",
                "question_nl": "Kies het juiste lidwoord: ___ livre (boek, mannelijk).",
                "options": ["le", "la", "un", "une"],
                "answer": "le",
                "explanation": "Livre is mannelijk, dus **le livre**."
            },
        ],
    },
    {
        "id": 4,
        "title": "4. Présent van -er werkwoorden",
        "theory": """
### Doel van dit hoofdstuk

Je leert de **tegenwoordige tijd (présent)** van **reguliere -er werkwoorden** zoals *parler* (spreken), *aimer* (houden van) en *habiter* (wonen).

Voorbeeld met **parler**:

- je parle  
- tu parles  
- il/elle parle  
- nous parlons  
- vous parlez  
- ils/elles parlent

Zelfde patroon voor *aimer*, *habiter*, etc.
""",
        "examples": [
            ("Je parle français.", "Ik spreek Frans."),
            ("Nous habitons aux Pays-Bas.", "Wij wonen in Nederland."),
        ],
        "exercises": [
            {
                "type": "input",
                "question_nl": "Vul in: \"Ik spreek\" → \"Je ____\" (werkwoord: parler).",
                "answer": "parle",
                "explanation": "Je + parler → **je parle**."
            },
            {
                "type": "input",
                "question_nl": "Vul in: \"Wij spreken\" → \"Nous ____\" (werkwoord: parler).",
                "answer": "parlons",
                "explanation": "Nous + parler → **nous parlons**."
            },
        ],
    },
    {
        "id": 5,
        "title": "5. Être, avoir, aller",
        "theory": """
### Doel van dit hoofdstuk

Je leert de onregelmatige werkwoorden **être (zijn)**, **avoir (hebben)** en **aller (gaan)** in de présent.

**Être**

- je suis  
- tu es  
- il/elle est  
- nous sommes  
- vous êtes  
- ils/elles sont  

**Avoir**

- j'ai  
- tu as  
- il/elle a  
- nous avons  
- vous avez  
- ils/elles ont  

**Aller**

- je vais  
- tu vas  
- il/elle va  
- nous allons  
- vous allez  
- ils/elles vont  
""",
        "examples": [
            ("Je suis néerlandais.", "Ik ben Nederlands."),
            ("Nous avons une voiture.", "Wij hebben een auto."),
            ("Ils vont à Paris.", "Zij gaan naar Parijs."),
        ],
        "exercises": [
            {
                "type": "mc",
                "question_nl": "Kies de juiste vorm: \"Wij zijn\" → \"Nous ____\" (être).",
                "options": ["sommes", "somment", "sont", "êtes"],
                "answer": "sommes",
                "explanation": "Nous + être → **nous sommes**."
            },
            {
                "type": "input",
                "question_nl": "Vul in: \"Ik heb\" → \"J'____\" (avoir).",
                "answer": "ai",
                "explanation": "Je + avoir → **j'ai**."
            },
        ],
    },
    {
        "id": 6,
        "title": "6. Ontkenning en vragen",
        "theory": """
### Doel van dit hoofdstuk

Je leert:

- **Ontkenning:** ne ... pas  
- **Ja/nee-vragen:** est-ce que + zin

**Ontkenning**

- **Je parle français.** → **Je ne parle pas français.**  
- **Nous habitons ici.** → **Nous n'habitons pas ici.**

**Vragen met est-ce que**

- **Tu parles français.** → **Est-ce que tu parles français ?**  
- **Vous habitez à Paris.** → **Est-ce que vous habitez à Paris ?**
""",
        "examples": [
            ("Je ne parle pas français.", "Ik spreek geen Frans."),
            ("Est-ce que tu parles anglais ?", "Spreek jij Engels?"),
        ],
        "exercises": [
            {
                "type": "input",
                "question_nl": "Maak ontkennend: \"Je parle français.\" → \"Je ____ parle ____ français.\"",
                "answer": "ne pas",
                "explanation": "Ontkenning: **ne** vóór het werkwoord en **pas** erna: *Je ne parle pas français.*"
            },
            {
                "type": "mc",
                "question_nl": "Maak een vraag van: \"Tu parles français.\"",
                "options": [
                    "Est-ce que tu parles français ?",
                    "Est-ce que parle tu français ?",
                    "Tu est-ce que parles français ?",
                    "Parles-tu est-ce que français ?"
                ],
                "answer": "Est-ce que tu parles français ?",
                "explanation": "Zet **est-ce que** vóór de gewone zin: *Est-ce que tu parles français ?*"
            },
        ],
    },
]

# ---------- Helpers voor voortgang ----------

if "progress" not in st.session_state:
    # progress[chapter_id] = {"done": aantal_vragen, "correct": aantal_goed}
    st.session_state.progress = {}

def update_progress(chapter_id: int, correct: bool):
    prog = st.session_state.progress.get(chapter_id, {"done": 0, "correct": 0})
    prog["done"] += 1
    if correct:
        prog["correct"] += 1
    st.session_state.progress[chapter_id] = prog

def render_progress_badge(chapter_id: int):
    prog = st.session_state.progress.get(chapter_id)
    if not prog or prog["done"] == 0:
        st.markdown("**Voortgang:** 0/0 ✅")
    else:
        st.markdown(f"**Voortgang:** {prog['correct']}/{prog['done']} goed ✅")


# ---------- UI: sidebar: hoofdstukselectie ----------

st.sidebar.title("📘 Frans – Methode")
st.sidebar.markdown(
    "Kies een hoofdstuk en werk stap voor stap. "
    "Focus: **grammatica en zinsopbouw**."
)

chapter_titles = [c["title"] for c in CHAPTERS]
choice = st.sidebar.radio("Hoofdstuk:", chapter_titles)

current_chapter = next(c for c in CHAPTERS if c["title"] == choice)

# ---------- Hoofdstukpagina ----------

st.title(current_chapter["title"])
render_progress_badge(current_chapter["id"])

st.markdown("---")
st.markdown(current_chapter["theory"])

st.markdown("#### Voorbeelden")
for fr, nl in current_chapter["examples"]:
    st.markdown(f"- **{fr}** → {nl}")

st.markdown("---")
st.markdown("### Oefeningen")

for idx, ex in enumerate(current_chapter["exercises"], start=1):
    st.markdown(f"#### Oefening {idx}")

    if ex["type"] == "mc":
        st.write(ex["question_nl"])
        key = f"mc_{current_chapter['id']}_{idx}"
        choice = st.radio(
            "Kies een antwoord:",
            ex["options"],
            key=key,
            index=None
        )
        if choice is not None:
            if choice == ex["answer"]:
                st.success("✅ Klopt!")
                update_progress(current_chapter["id"], True)
            else:
                st.error(f"❌ Niet helemaal. Juist antwoord: **{ex['answer']}**.")
                update_progress(current_chapter["id"], False)
            if "explanation" in ex:
                with st.expander("Uitleg"):
                    st.write(ex["explanation"])

    elif ex["type"] == "input":
        st.write(ex["question_nl"])
        key = f"in_{current_chapter['id']}_{idx}"
        user_input = st.text_input("Antwoord (Frans):", key=key)
        if user_input:
            normalized = user_input.strip().lower().replace("’", "'")
            answer_norm = ex["answer"].strip().lower()
            correct = False

            # speciaal geval: "ne pas" in losse velden toestaan
            if answer_norm == "ne pas":
                if "ne" in normalized and "pas" in normalized:
                    correct = True
            else:
                if normalized == answer_norm:
                    correct = True

            if correct:
                st.success("✅ Klopt!")
                update_progress(current_chapter["id"], True)
            else:
                st.error(f"❌ Niet helemaal. Verwacht (kern): **{ex['answer']}**.")
                update_progress(current_chapter["id"], False)
            if "explanation" in ex:
                with st.expander("Uitleg"):
                    st.write(ex["explanation"])

    elif ex["type"] == "order":
        st.write(ex["instruction_nl"])
        parts = ex["parts"]
        default_order = list(range(len(parts)))
        key = f"order_{current_chapter['id']}_{idx}"
        user_order = st.multiselect(
            "Klik de delen in de juiste volgorde:",
            options=list(range(len(parts))),
            format_func=lambda i: parts[i],
            key=key,
        )

        if user_order and len(user_order) == len(parts):
            user_seq = [parts[i] for i in user_order]
            if user_seq == ex["correct"]:
                st.success("✅ Klopt: " + " ".join(user_seq))
                update_progress(current_chapter["id"], True)
            else:
                st.error(
                    "❌ Niet helemaal. Jouw zin: "
                    + " ".join(user_seq)
                    + "\n\nCorrect: "
                    + " ".join(ex["correct"])
                )
                update_progress(current_chapter["id"], False)
            if "explanation" in ex:
                with st.expander("Uitleg"):
                    st.write(ex["explanation"])

st.markdown("---")
st.caption(
    "Tip: werk de hoofdstukken in volgorde door, en herhaal oudere hoofdstukken "
    "tot je zinnen zelf kunt maken zonder na te denken."
)
