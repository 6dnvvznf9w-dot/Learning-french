import streamlit as st
from gtts import gTTS
import io
import random

# ---------------------------------------------------------
# Basisconfiguratie
# ---------------------------------------------------------

st.set_page_config(
    page_title="Frans voor Cargo Operations",
    page_icon="🇫🇷",
    layout="centered"
)

# ---------------------------------------------------------
# TTS helper (tekst -> audio)
# ---------------------------------------------------------

@st.cache_data
def tts_bytes(text: str, lang: str = "fr") -> bytes:
    """Genereer mp3-audio uit Franse tekst."""
    tts = gTTS(text, lang=lang)
    buf = io.BytesIO()
    tts.write_to_fp(buf)
    buf.seek(0)
    return buf.read()

# ---------------------------------------------------------
# Data: cursus-hoofdstukken (grammatica / zinnen)
# ---------------------------------------------------------

CHAPTERS = [
    {
        "id": 1,
        "title": "1. Kennismaking en hallo zeggen",
        "goal_nl": "Na dit hoofdstuk kun je jezelf kort voorstellen en iemand begroeten.",
        "theory": """
### Doel

Je leert hoe je in het Frans:

- hallo zegt  
- jezelf voorstelt (naam, rol, bedrijf)  
- heel kort uitlegt wat je doet

### Kernzinnen

- Bonjour → Goedendag / hallo  
- Salut → Hoi (informeel)  
- Je m'appelle Toon. → Ik heet Toon.  
- Je suis opérateur cargo. → Ik ben cargobediener.  
- Je travaille chez Equinor. → Ik werk bij Equinor.  
""",
        "examples": [
            ("Bonjour, je m'appelle Toon.", "Goedendag, ik heet Toon."),
            ("Je suis responsable des opérations cargo.", "Ik ben verantwoordelijk voor de cargo-operaties."),
            ("Je travaille chez Equinor.", "Ik werk bij Equinor."),
        ],
        "exercises": [
            {
                "type": "mc",
                "question_nl": "Wat betekent: « Bonjour, je m'appelle Pierre. »?",
                "options": [
                    "Goedemorgen, ik werk bij Pierre.",
                    "Goedendag, ik heet Pierre.",
                    "Hoi, ik kom uit Pierre.",
                ],
                "answer": "Goedendag, ik heet Pierre.",
                "explanation": "Bonjour = goedendag / hallo, je m'appelle Pierre = ik heet Pierre."
            },
            {
                "type": "input",
                "question_nl": "Schrijf in het Frans: \"Ik werk bij Equinor.\"",
                "answer": "je travaille chez equinor",
                "explanation": "Je travaille chez Equinor."
            },
        ],
    },
    {
        "id": 2,
        "title": "2. Over jou en je werk (FR UI)",
        "goal_nl": "Na dit hoofdstuk kun je in het Frans vertellen wat je functie is.",
        "theory": """
### Objectif

Dans ce chapitre, l'interface est en **français**.  
Tu apprends à parler de ton travail.

### Phrases utiles

- Je suis opérateur cargo.  
- Je suis responsable des opérations cargo.  
- Je travaille au terminal LPG.  
- Je travaille à Stavanger.  
- Je travaille de jour / de nuit.  
""",
        "examples": [
            ("Je suis opérateur cargo.", "Ik ben cargobediener."),
            ("Je suis responsable des opérations cargo.", "Ik ben verantwoordelijk voor de cargo-operaties."),
            ("Je travaille au terminal LPG à Stavanger.", "Ik werk op de LPG-terminal in Stavanger."),
        ],
        "exercises": [
            {
                "type": "mc",
                "question_nl": "Wat betekent: « Je travaille au terminal LPG. »?",
                "options": [
                    "Ik woon op de LPG-terminal.",
                    "Ik werk op de LPG-terminal.",
                    "Ik vaar naar de LPG-terminal."
                ],
                "answer": "Ik werk op de LPG-terminal.",
                "explanation": "Travailler = werken, donc: ik werk op de LPG-terminal."
            },
            {
                "type": "input",
                "question_nl": "Schrijf in het Frans: \"Ik ben verantwoordelijk voor de cargo-operaties.\"",
                "answer": "je suis responsable des opérations cargo",
                "explanation": "Je suis responsable des opérations cargo."
            },
        ],
    },
    {
        "id": 3,
        "title": "3. Smalltalk: hoe gaat het en het weer",
        "goal_nl": "Na dit hoofdstuk kun je vragen hoe het gaat en kort over het weer praten.",
        "theory": """
### Doel

Je leert:

- vragen hoe het gaat  
- vertellen hoe het gaat  
- iets zeggen over het weer

### Kernzinnen

- Ça va ? → Hoe gaat het?  
- Ça va bien, merci. → Het gaat goed, dank je.  
- Comme ci, comme ça. → Gaat wel.  
- Il fait froid. → Het is koud.  
- Il fait chaud. → Het is warm.  
- Il fait beau. → Het is mooi weer.  
""",
        "examples": [
            ("Salut, ça va ?", "Hoi, hoe gaat het?"),
            ("Ça va bien, merci.", "Het gaat goed, dank je."),
            ("Il fait très froid aujourd'hui.", "Het is heel koud vandaag."),
        ],
        "exercises": [
            {
                "type": "mc",
                "question_nl": "Wat zeg je in het Frans: \"Het is mooi weer.\"?",
                "options": [
                    "Il est beau.",
                    "Il fait beau.",
                    "Il va beau."
                ],
                "answer": "Il fait beau.",
                "explanation": "Voor weer zeg je in het Frans vaak \"Il fait ...\" + bijvoeglijk naamwoord."
            },
            {
                "type": "input",
                "question_nl": "Schrijf in het Frans: \"Hoe gaat het?\"",
                "answer": "ça va ?",
                "explanation": "Ça va ? met vraagteken is de standaard manier om te vragen hoe het gaat."
            },
        ],
    },
    {
        "id": 4,
        "title": "4. Werkdruk en planning",
        "goal_nl": "Na dit hoofdstuk kun je zeggen of het druk of rustig is en iets over je planning.",
        "theory": """
### Doel

Je leert:

- zeggen dat het druk of rustig is  
- heel kort de planning te beschrijven

### Kernzinnen

- Aujourd'hui, c'est très chargé. → Vandaag is het erg druk.  
- Aujourd'hui, c'est calme. → Vandaag is het rustig.  
- Nous avons trois navires. → We hebben drie schepen.  
- Nous avons beaucoup de camions. → We hebben veel trucks.  
- Il y a un petit problème. → Er is een klein probleem.  
""",
        "examples": [
            ("Aujourd'hui, c'est très chargé pour moi.", "Vandaag is het erg druk voor mij."),
            ("Aujourd'hui, c'est calme.", "Vandaag is het rustig."),
            ("Nous avons trois navires et beaucoup de camions.", "We hebben drie schepen en veel trucks."),
        ],
        "exercises": [
            {
                "type": "mc",
                "question_nl": "Wat betekent: « Aujourd'hui, c'est calme. »?",
                "options": [
                    "Vandaag is het druk.",
                    "Vandaag is het rustig.",
                    "Vandaag is het slecht weer."
                ],
                "answer": "Vandaag is het rustig.",
                "explanation": "Calme = rustig."
            },
            {
                "type": "input",
                "question_nl": "Schrijf in het Frans: \"We hebben drie schepen.\"",
                "answer": "nous avons trois navires",
                "explanation": "Nous avons trois navires."
            },
        ],
    },
    {
        "id": 5,
        "title": "5. Zinsbouw en voornaamwoorden",
        "goal_nl": "Na dit hoofdstuk herken en gebruik je de basis-zinsvolgorde (S–V–O) en persoonlijke voornaamwoorden.",
        "theory": """
### Doel

Je leert:

- de basis-zinsvolgorde in het Frans (S–V–O)  
- de belangrijkste persoonlijke voornaamwoorden

### Persoonlijke voornaamwoorden

- je → ik  
- tu → jij  
- il / elle → hij / zij  
- nous → wij  
- vous → jullie / u  
- ils / elles → zij (mannelijk/vrouwelijk meervoud)

### Voorbeelden (S–V–O)

- Je parle français. → Ik spreek Frans.  
- Nous travaillons au terminal. → Wij werken op de terminal.  
""",
        "examples": [
            ("Je parle français.", "Ik spreek Frans."),
            ("Nous travaillons au terminal LPG.", "Wij werken op de LPG-terminal."),
        ],
        "exercises": [
            {
                "type": "order",
                "instruction_nl": "Zet de delen in de goede volgorde (S–V–O):",
                "parts": ["français", "je", "parle"],
                "correct": ["je", "parle", "français"],
                "explanation": "Eerst onderwerp (je), dan werkwoord (parle), dan rest (français)."
            },
            {
                "type": "mc",
                "question_nl": "Welk persoonlijk voornaamwoord hoort bij \"wij\"?",
                "options": ["je", "tu", "nous", "ils"],
                "answer": "nous",
                "explanation": "Voor \"wij\" gebruik je nous."
            },
        ],
    },
    {
        "id": 6,
        "title": "6. Werkwoorden: présent en ontkenning",
        "goal_nl": "Na dit hoofdstuk kun je eenvoudige zinnen maken in de tegenwoordige tijd en ze ontkennend maken.",
        "theory": """
### Doel

Je leert:

- de tegenwoordige tijd (présent) van een paar kernwerkwoorden  
- ontkenning met **ne ... pas**

### Kernwerkwoorden (ik-vorm)

- je suis → ik ben  
- j'ai → ik heb  
- je vais → ik ga  
- je travaille → ik werk  

### Ontkenning

- Je parle français. → Je **ne** parle **pas** français.  
- Je travaille aujourd'hui. → Je **ne** travaille **pas** aujourd'hui.  
""",
        "examples": [
            ("Je suis opérateur cargo.", "Ik ben cargobediener."),
            ("Je ne travaille pas aujourd'hui.", "Ik werk vandaag niet."),
        ],
        "exercises": [
            {
                "type": "input",
                "question_nl": "Vul aan: \"Ik ben\" → \"Je ____\" (être).",
                "answer": "suis",
                "explanation": "Je suis."
            },
            {
                "type": "input",
                "question_nl": "Maak ontkennend: \"Je travaille aujourd'hui.\" (kernwoorden, zonder hoofdletters/punten)",
                "answer": "je ne travaille pas aujourd'hui",
                "explanation": "Je ne travaille pas aujourd'hui."
            },
        ],
    },
]

# ---------------------------------------------------------
# Data: dialogen voor lezen + luisteren
# ---------------------------------------------------------

DIALOGUES = [
    {
        "id": "intro",
        "title": "Introductie op het werk",
        "description_nl": "Je stelt jezelf voor aan een Franse collega op de LPG-terminal.",
        "turns": [
            ("Toon", "Bonjour, je m'appelle Toon. Je travaille chez Equinor, au terminal LPG à Stavanger.",
             "Hallo, ik heet Toon. Ik werk bij Equinor, op de LPG-terminal in Stavanger."),
            ("Pierre", "Enchanté, je suis Pierre. Je suis opérateur cargo.",
             "Aangenaam, ik ben Pierre. Ik ben cargobediener."),
            ("Toon", "Je suis responsable des opérations cargo. Je veux que la cargaison arrive en sécurité et à l'heure.",
             "Ik ben verantwoordelijk voor de cargo-operaties. Ik wil dat de lading veilig en op tijd aankomt."),
        ],
        "question_nl": "Wat is de functie van Toon?",
        "options": [
            "Hij is kapitein.",
            "Hij is verantwoordelijk voor de cargo-operaties.",
            "Hij is vrachtwagenchauffeur."
        ],
        "correct": "Hij is verantwoordelijk voor de cargo-operaties."
    },
    {
        "id": "meteo",
        "title": "Weer en werkdruk",
        "description_nl": "Je praat over het weer en hoe druk je dag is.",
        "turns": [
            ("Toon", "Salut Pierre, ça va ? Il fait très froid aujourd'hui.",
             "Hoi Pierre, alles goed? Het is erg koud vandaag."),
            ("Pierre", "Oui, ça va. Il fait froid mais le temps est stable, c'est bien pour les opérations.",
             "Ja, gaat goed. Het is koud maar het weer is stabiel, dat is goed voor de operaties."),
            ("Toon", "Aujourd'hui, c'est très chargé pour moi. Nous avons trois navires et beaucoup de camions.",
             "Vandaag is het erg druk voor mij. We hebben drie schepen en veel trucks."),
        ],
        "question_nl": "Waarom is het goed dat het weer stabiel is?",
        "options": [
            "Omdat het dan mooi weer is.",
            "Omdat dat goed is voor de operaties.",
            "Omdat er dan geen vrachtwagens zijn."
        ],
        "correct": "Omdat dat goed is voor de operaties."
    },
]

# ---------------------------------------------------------
# Data: schrijftaken
# ---------------------------------------------------------

WRITING_TASKS = [
    {
        "id": "intro",
        "label": "Stel jezelf voor aan een Franse collega",
        "hint": (
            "Gebruik 3–5 zinnen met:\n"
            "- je m'appelle ...\n"
            "- je suis ... (functie)\n"
            "- je travaille ... (bedrijf/plaats)\n"
        ),
        "example": """Bonjour, je m'appelle Toon.
Je suis responsable des opérations cargo.
Je travaille chez Equinor, au terminal LPG à Stavanger.
Aujourd'hui, c'est assez chargé pour moi."""
    },
    {
        "id": "workload",
        "label": "Beschrijf hoe druk je dag is",
        "hint": (
            "Gebruik 3–5 zinnen met:\n"
            "- aujourd'hui, c'est ... (calme / très chargé)\n"
            "- nous avons ... (navires / camions)\n"
            "- il y a un petit problème (optioneel)\n"
        ),
        "example": """Aujourd'hui, c'est très chargé.
Nous avons trois navires et beaucoup de camions.
Il y a un petit problème avec un navire, mais c'est sous contrôle."""
    },
    {
        "id": "responsibility",
        "label": "Leg kort uit wat jouw verantwoordelijkheid is",
        "hint": (
            "Gebruik 3–5 zinnen met:\n"
            "- je suis responsable de ...\n"
            "- je veux que ... (la cargaison arrive en sécurité, et à l'heure)\n"
        ),
        "example": """Je suis responsable des opérations cargo.
Je veux que la cargaison arrive en sécurité et à l'heure.
Je travaille avec l'équipe pour éviter les problèmes."""
    },
]

# ---------------------------------------------------------
# Hulpfuncties
# ---------------------------------------------------------

def normalize_answer(s: str) -> str:
    return s.strip().lower().replace("’", "'")


# ---------------------------------------------------------
# UI: Sidebar – modus kiezen
# ---------------------------------------------------------

st.sidebar.title("📘 Frans – Cargo Operations")
st.sidebar.markdown(
    "Plan: **20–30 minuten per dag**.\n\n"
    "Kies een modus om te oefenen."
)

MODES = [
    "Leercursus (hoofdstukken)",
    "Dialogen (lees & luister)",
    "Schrijven (korte teksten)",
    "Studieplan"
]

mode = st.sidebar.radio("Modus", MODES)

# ---------------------------------------------------------
# Modus 1: Hoofdstukken (grammatica / zinnen)
# ---------------------------------------------------------

if mode == "Leercursus (hoofdstukken)":
    chapter_titles = [c["title"] for c in CHAPTERS]
    selected_title = st.selectbox("Kies een hoofdstuk:", chapter_titles)
    chapter = next(c for c in CHAPTERS if c["title"] == selected_title)

    st.title(chapter["title"])
    st.markdown(f"**Doel (NL):** {chapter['goal_nl']}")
    st.markdown("---")

    tab_theory, tab_exercises = st.tabs(["Uitleg & voorbeelden", "Oefeningen"])

    with tab_theory:
        st.markdown(chapter["theory"])
        st.markdown("#### Voorbeelden")
        for fr, nl in chapter["examples"]:
            cols = st.columns([3, 1])
            with cols[0]:
                st.markdown(f"**FR:** {fr}")
                if st.button("▶ Luister", key=f"ex_audio_{chapter['id']}_{fr}"):
                    audio_data = tts_bytes(fr, lang="fr")
                    st.audio(audio_data, format="audio/mp3")
            with cols[1]:
                st.markdown(f"*NL:* {nl}")

    with tab_exercises:
        st.markdown("### Oefeningen")
        for idx, ex in enumerate(chapter["exercises"], start=1):
            st.markdown(f"#### Oefening {idx}")
            ex_key = f"ch{chapter['id']}_ex{idx}"

            if ex["type"] == "mc":
                st.write(ex["question_nl"])
                choice = st.radio(
                    "Kies het beste antwoord:",
                    ex["options"],
                    key=ex_key
                )
                if choice:
                    if choice == ex["answer"]:
                        st.success("✅ Klopt!")
                    else:
                        st.error(f"❌ Niet helemaal. Juist antwoord: **{ex['answer']}**.")
                    if "explanation" in ex:
                        with st.expander("Uitleg"):
                            st.write(ex["explanation"])

            elif ex["type"] == "input":
                st.write(ex["question_nl"])
                user = st.text_input("Jouw antwoord (Frans):", key=ex_key)
                if user:
                    if normalize_answer(user) == normalize_answer(ex["answer"]):
                        st.success("✅ Klopt!")
                    else:
                        st.error(f"❌ Niet helemaal. Verwacht (kern): **{ex['answer']}**.")
                    if "explanation" in ex:
                        with st.expander("Uitleg"):
                            st.write(ex["explanation"])

            elif ex["type"] == "order":
                st.write(ex["instruction_nl"])
                parts = ex["parts"]
                user_order = st.multiselect(
                    "Klik de delen in de juiste volgorde:",
                    options=list(range(len(parts))),
                    format_func=lambda i, parts=parts: parts[i],
                    key=ex_key
                )
                if user_order and len(user_order) == len(parts):
                    user_seq = [parts[i] for i in user_order]
                    if user_seq == ex["correct"]:
                        st.success("✅ Klopt: " + " ".join(user_seq))
                    else:
                        st.error(
                            "❌ Niet helemaal.\n\n"
                            f"Jouw zin: {' '.join(user_seq)}\n\n"
                            f"Correct: {' '.join(ex['correct'])}"
                        )
                    if "explanation" in ex:
                        with st.expander("Uitleg"):
                            st.write(ex["explanation"])

    st.caption("Tip: kies elke dag één hoofdstuk en werk 20–30 minuten aan uitleg + oefeningen.")

# ---------------------------------------------------------
# Modus 2: Dialogen (lees & luister)
# ---------------------------------------------------------

elif mode == "Dialogen (lees & luister)":
    st.title("Dialogen – lezen en luisteren")

    dlg_titles = [d["title"] for d in DIALOGUES]
    dlg_title = st.selectbox("Kies een dialoog:", dlg_titles)
    dlg = next(d for d in DIALOGUES if d["title"] == dlg_title)

    st.markdown(f"**Situatie (NL):** {dlg['description_nl']}")
    st.markdown("---")

    for speaker, fr, nl in dlg["turns"]:
        st.markdown(f"**{speaker} – FR:** {fr}")
        st.markdown(f"*NL:* {nl}")
        if st.button(f"▶ Luister ({speaker})", key=f"dlg_audio_{dlg['id']}_{speaker}_{fr}"):
            audio_data = tts_bytes(fr, lang="fr")
            st.audio(audio_data, format="audio/mp3")
        st.markdown("")

    st.markdown("### Begrijpvraag")
    answer = st.radio(
        dlg["question_nl"],
        dlg["options"],
        key=f"dlg_q_{dlg['id']}"
    )
    if answer:
        if answer == dlg["correct"]:
            st.success("✅ Klopt!")
        else:
            st.error("❌ Niet helemaal, luister de dialoog nog een keer en let op de sleutelzin.")

    st.caption("Tip: speel elke zin meerdere keren af en spreek hardop na voor uitspraak.")

# ---------------------------------------------------------
# Modus 3: Schrijven (korte teksten)
# ---------------------------------------------------------

elif mode == "Schrijven (korte teksten)":
    st.title("Schrijven – korte teksten over je werk")

    taak_labels = [t["label"] for t in WRITING_TASKS]
    label = st.selectbox("Kies een schrijftaak:", taak_labels)
    task = next(t for t in WRITING_TASKS if t["label"] == label)

    st.markdown("### Instructie")
    st.markdown(task["hint"])

    tekst = st.text_area("Jouw tekst (Frans):", height=220)

    if st.button("Analyseer tekst"):
        if not tekst.strip():
            st.warning("Schrijf eerst iets in het tekstvak.")
        else:
            lower = tekst.lower()
            hints = []

            # heel simpele checks op kernstructuren
            if "je m'appelle" not in lower and "je suis" not in lower:
                hints.append("Overweeg een zin met **je m'appelle** of **je suis**.")
            if "je travaille" not in lower and "je suis responsable" not in lower:
                hints.append("Probeer een zin met **je travaille** of **je suis responsable de ...**.")
            werkwoorden = ["cargo", "terminal", "navire", "camion", "opérations"]
            if not any(w in lower for w in werkwoorden):
                hints.append(
                    "Ik zie geen woorden over je werk (cargo/terminal/navire/camion/opérations). "
                    "Probeer er 1–2 in te voegen."
                )

            if hints:
                st.error("Een paar verbeterpunten:")
                for h in hints:
                    st.markdown(f"- {h}")
            else:
                st.success("Mooi! Je gebruikt de belangrijkste structuren die je in deze fase nodig hebt.")

            st.markdown("#### Voorbeeldtekst")
            st.code(task["example"], language="markdown")

# ---------------------------------------------------------
# Modus 4: Studieplan
# ---------------------------------------------------------

elif mode == "Studieplan":
    st.title("Studieplan – 20 minuten per dag")

    st.markdown("""
Dit is een eenvoudig **20–30 minuten per dag** plan:

### Week 1
- 5 dagen per week  
- Dag 1–2: Hoofdstuk 1 (kennismaking)  
- Dag 3–4: Hoofdstuk 2 (over jouw werk)  
- Dag 5: Dialogen-modus – *Introductie op het werk*

### Week 2
- Hoofdstuk 3 (smalltalk + weer)  
- Hoofdstuk 4 (werkdruk en planning)  
- Dialogen: *Weer en werkdruk*  

### Week 3
- Hoofdstuk 5 (zinsbouw en voornaamwoorden)  
- Hoofdstuk 6 (werkwoorden + ontkenning)  
- Schrijven-modus: elke dag 1 taak

### Week 4 en verder
- Herhaal hoofdstukken waar je moeite mee hebt  
- Mix elke sessie:
  - 10 min lezen/luisteren (dialogen of hoofdstukken-uitleg)
  - 10–20 min oefenen (MC, input, schrijven)

Na ongeveer 20 uur kun je een **korte, werkgerelateerde conversatie** voeren met een Franse collega:
jezelf voorstellen, vragen hoe het gaat, iets over het weer zeggen en uitleggen hoe druk of rustig je dag is.
    """)

    st.caption("Tip: plan vaste momenten (bijv. iedere werkdag om 08:00 of na de lunch).")
