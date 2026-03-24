import streamlit as st
from gtts import gTTS
import io
from sqlalchemy import text

# ---------------------------------------------------------
# DB-verbinding (Supabase / Postgres)
# ---------------------------------------------------------

# Naam moet overeenkomen met [connections.frans_db] in Streamlit secrets
conn = st.connection("frans_db", type="sql")

# ---------------------------------------------------------
# Basisconfiguratie
# ---------------------------------------------------------

st.set_page_config(
    page_title="Frans voor Cargo Operations",
    page_icon="🇫🇷",
    layout="centered",
)

# ---------------------------------------------------------
# TTS helper
# ---------------------------------------------------------

@st.cache_data
def tts_bytes(text: str, lang: str = "fr") -> bytes:
    """Genereer mp3-audio uit tekst (standaard Frans)."""
    tts = gTTS(text, lang=lang)
    buf = io.BytesIO()
    tts.write_to_fp(buf)
    buf.seek(0)
    return buf.read()


def normalize_answer(s: str) -> str:
    return s.strip().lower().replace("’", "'")


# ---------------------------------------------------------
# Progress + logging helpers
# ---------------------------------------------------------

if "user_id" not in st.session_state:
    st.session_state.user_id = "David"  # jouw standaard gebruiker

if "progress" not in st.session_state:
    # {(user_id, chapter_id): {"reading_done": ..., "ex_done": ...}}
    st.session_state.progress = {}


def load_progress(user_id: str, chapter_id: int):
    query = text(
        """
        select reading_done, reading_correct, ex_done, ex_correct
        from progress
        where user_id = :user_id and chapter_id = :chapter_id
        """
    )
    with conn.session as s:
        row = s.execute(
            query,
            {"user_id": user_id, "chapter_id": chapter_id},
        ).fetchone()
    if row:
        return dict(row._mapping)
    else:
        return {
            "reading_done": 0,
            "reading_correct": 0,
            "ex_done": 0,
            "ex_correct": 0,
        }


def save_progress(user_id: str, chapter_id: int, prog: dict):
    query = text(
        """
        insert into progress (user_id, chapter_id, reading_done, reading_correct, ex_done, ex_correct)
        values (:user_id, :chapter_id, :reading_done, :reading_correct, :ex_done, :ex_correct)
        on conflict (user_id, chapter_id) do update set
          reading_done    = excluded.reading_done,
          reading_correct = excluded.reading_correct,
          ex_done         = excluded.ex_done,
          ex_correct      = excluded.ex_correct,
          updated_at      = now()
        """
    )
    with conn.session as s:
        s.execute(
            query,
            {
                "user_id": user_id,
                "chapter_id": chapter_id,
                "reading_done": prog["reading_done"],
                "reading_correct": prog["reading_correct"],
                "ex_done": prog["ex_done"],
                "ex_correct": prog["ex_correct"],
            },
        )
        s.commit()


def get_progress(chapter_id: int):
    key = (st.session_state.user_id, chapter_id)
    if key not in st.session_state.progress:
        st.session_state.progress[key] = load_progress(
            st.session_state.user_id, chapter_id
        )
    return st.session_state.progress[key]


def update_progress(chapter_id: int, kind: str, correct: bool):
    """
    kind: "reading" of "ex"
    """
    key = (st.session_state.user_id, chapter_id)
    prog = get_progress(chapter_id)

    if kind == "reading":
        prog["reading_done"] += 1
        if correct:
            prog["reading_correct"] += 1
    elif kind == "ex":
        prog["ex_done"] += 1
        if correct:
            prog["ex_correct"] += 1

    st.session_state.progress[key] = prog
    save_progress(st.session_state.user_id, chapter_id, prog)


def log_exercise_answer(
    user_id: str,
    chapter_id: int,
    exercise_key: str,
    answer_text: str,
    is_correct: bool | None,
):
    """
    Sla elk individueel antwoord op in exercise_answers.
    """
    query = text(
        """
        insert into exercise_answers (user_id, chapter_id, exercise_key, answer_text, is_correct)
        values (:user_id, :chapter_id, :exercise_key, :answer_text, :is_correct)
        """
    )
    with conn.session as s:
        s.execute(
            query,
            {
                "user_id": user_id,
                "chapter_id": chapter_id,
                "exercise_key": exercise_key,
                "answer_text": answer_text,
                "is_correct": is_correct,
            },
        )
        s.commit()


# ---------------------------------------------------------
# Schrijf-antwoorden per hoofdstuk
# ---------------------------------------------------------

def load_writing_answer(user_id: str, chapter_id: int) -> str:
    """
    Haal de laatste opgeslagen schrijftekst voor een hoofdstuk op.
    """
    query = text(
        """
        select answer_text
        from writing_answers
        where user_id = :user_id and chapter_id = :chapter_id
        order by updated_at desc
        limit 1
        """
    )
    with conn.session as s:
        row = s.execute(
            query,
            {"user_id": user_id, "chapter_id": chapter_id},
        ).fetchone()
    if row:
        return row[0]
    return ""


def save_writing_answer(user_id: str, chapter_id: int, answer_text: str):
    """
    Sla de (laatste) schrijftekst per hoofdstuk op.
    """
    query = text(
        """
        insert into writing_answers (user_id, chapter_id, answer_text)
        values (:user_id, :chapter_id, :answer_text)
        on conflict (user_id, chapter_id) do update set
          answer_text = excluded.answer_text,
          updated_at  = now()
        """
    )
    with conn.session as s:
        s.execute(
            query,
            {
                "user_id": user_id,
                "chapter_id": chapter_id,
                "answer_text": answer_text,
            },
        )
        s.commit()
# ---------------------------------------------------------
# Cursusdata per hoofdstuk
# ---------------------------------------------------------

CHAPTERS = [
    {
        "id": 1,
        "title": "1. Kennismaking en hallo zeggen",
        "goal_nl": "Je kunt jezelf kort voorstellen en iemand begroeten.",
        "intro_audio_fr": "Bonjour, je m'appelle David. Dans ce chapitre, tu apprends à te présenter et à dire bonjour au travail.",
        "theory": """
### Doel

Je leert hoe je in het Frans:

- hallo zegt  
- jezelf voorstelt (naam, land)  
- kort uitlegt dat je net begint op het werk

### Kernzinnen

- Bonjour → Goedendag / hallo  
- Salut → Hoi (informeel)  
- Je m'appelle David. → Ik heet David.  
- Je suis néerlandais. → Ik ben Nederlands.  
- Je suis graduate. → Ik ben starter / pas afgestudeerd.  
""",
        "examples": [
            ("Bonjour, je m'appelle David.", "Goedendag, ik heet David."),
            ("Je suis néerlandais.", "Ik ben Nederlands."),
            ("Je suis graduate chez Equinor.", "Ik ben graduate bij Equinor."),
        ],
        "dialogue": {
            "title": "Dialoog: eerste werkdag",
            "turns": [
                (
                    "Piril",
                    "Bonjour, je m'appelle Piril. Je suis turque et je suis graduate.",
                    "Hallo, ik heet Piril. Ik ben Turks en ik ben graduate."
                ),
                (
                    "David",
                    "Bonjour, je suis David. Je suis néerlandais et je suis aussi graduate.",
                    "Hallo, ik ben David. Ik ben Nederlands en ik ben ook graduate."
                ),
                (
                    "Piril",
                    "C'est notre premier jour de travail ici.",
                    "Het is onze eerste werkdag hier."
                ),
                (
                    "David",
                    "Oui, je suis un peu nerveux, mais content.",
                    "Ja, ik ben een beetje nerveus, maar blij."
                ),
            ]
        },
        "reading": {
            "text_fr": (
                "Je m'appelle David. Je suis néerlandais et je suis graduate. "
                "Aujourd'hui, c'est mon premier jour de travail à Stavanger. "
                "Je commence dans une grande entreprise d'énergie. "
                "Je suis un peu nerveux, mais je suis aussi très content.\n\n"
                "Le matin, j'arrive au bureau. Je rencontre une nouvelle collègue. "
                "Elle s'appelle Piril. Elle est turque et elle est aussi graduate. "
                "Nous disons bonjour et nous parlons un peu. "
                "Nous travaillons dans le même bâtiment, mais pas dans la même équipe."
            ),
            "vocab": [
                ("je m'appelle", "ik heet"),
                ("néerlandais", "Nederlands (bijv. van nationaliteit)"),
                ("graduate", "starter / pas afgestudeerde"),
                ("premier jour", "eerste dag"),
                ("entreprise", "bedrijf"),
                ("nerveux / nerveuse", "nerveus"),
                ("content(e)", "blij / tevreden"),
                ("collègue", "collega"),
                ("bâtiment", "gebouw"),
                ("équipe", "team")
            ],
            "questions": [
                {
                    "type": "mc",
                    "question_nl": "Waar is David op zijn eerste werkdag?",
                    "options": [
                        "In Nice.",
                        "In Stavanger.",
                        "In Oslo.",
                        "In Parijs."
                    ],
                    "answer": "In Stavanger.",
                    "explanation": "Hij zegt: « Aujourd'hui, c'est mon premier jour de travail à Stavanger. »"
                },
                {
                    "type": "mc",
                    "question_nl": "Wat is Davids nationaliteit?",
                    "options": [
                        "Hij is Frans.",
                        "Hij is Turks.",
                        "Hij is Nederlands.",
                        "Hij is Italiaans."
                    ],
                    "answer": "Hij is Nederlands.",
                    "explanation": "Hij zegt: « Je suis néerlandais. »"
                },
                {
                    "type": "mc",
                    "question_nl": "Hoe voelt David zich op zijn eerste dag?",
                    "options": [
                        "Alleen boos.",
                        "Een beetje nerveus maar blij.",
                        "Heel verdrietig.",
                        "Hij voelt niets."
                    ],
                    "answer": "Een beetje nerveus maar blij.",
                    "explanation": "« Je suis un peu nerveux, mais je suis aussi très content. »"
                },
                {
                    "type": "mc",
                    "question_nl": "Wie is Piril?",
                    "options": [
                        "Een Franse klant.",
                        "Een nieuwe collega en ook graduate.",
                        "De baas van David.",
                        "De kapitein van een schip."
                    ],
                    "answer": "Een nieuwe collega en ook graduate.",
                    "explanation": "« Elle est turque et elle est aussi graduate. »"
                },
                {
                    "type": "input",
                    "question_nl": "Schrijf in het Frans: \"Het is mijn eerste werkdag.\" (kort)",
                    "answer": "c'est mon premier jour de travail",
                    "explanation": "C'est mon premier jour de travail."
                },
                {
                    "type": "mc",
                    "question_nl": "Wat betekent \"collègue\"?",
                    "options": [
                        "Vriend(in).",
                        "Collega.",
                        "Kapitein.",
                        "Leraar."
                    ],
                    "answer": "Collega.",
                    "explanation": "Une collègue = een collega."
                },
                {
                    "type": "mc",
                    "question_nl": "Wat betekent \"entreprise\"?",
                    "options": [
                        "School.",
                        "Bedrijf.",
                        "Treinstation.",
                        "Ziekenhuis."
                    ],
                    "answer": "Bedrijf.",
                    "explanation": "Une entreprise = een bedrijf."
                },
                {
                    "type": "input",
                    "question_nl": "Schrijf in het Frans: \"Ik ben starter.\" (graduate)",
                    "answer": "je suis graduate",
                    "explanation": "Je suis graduate."
                },
                {
                    "type": "mc",
                    "question_nl": "In welke zin past het woord \"équipe\"?",
                    "options": [
                        "Je suis une équipe.",
                        "Je travaille dans une équipe.",
                        "Je mange une équipe.",
                        "Je bois une équipe."
                    ],
                    "answer": "Je travaille dans une équipe.",
                    "explanation": "In een team werken → travailler dans une équipe."
                },
                {
                    "type": "input",
                    "question_nl": "Schrijf in het Frans: \"Ik ben een beetje nerveus.\"",
                    "answer": "je suis un peu nerveux",
                    "explanation": "Je suis un peu nerveux. (voor een man; nerveuse voor een vrouw)"
                },
            ]
        },
        "write_hint": (
            "Schrijf 3–5 zinnen waarin je jezelf voorstelt.\n"
            "- je m'appelle ...\n"
            "- je suis ... (land / graduate)\n"
            "- aujourd'hui, c'est mon premier jour de travail\n"
        ),
        "write_example": """Bonjour, je m'appelle David.
Je suis néerlandais et je suis graduate.
Aujourd'hui, c'est mon premier jour de travail à Stavanger.""",
        "exercises": [
            {
                "type": "mc",
                "question_nl": "Wat betekent: « Bonjour, je m'appelle Pierre. »?",
                "options": [
                    "Goedemorgen, ik werk bij Pierre.",
                    "Goedendag, ik heet Pierre.",
                    "Hoi, ik kom uit Pierre.",
                    "Ik ben Pierre en ik woon in Parijs.",
                    "Tot ziens, ik ben Pierre.",
                    "Ik ben verantwoordelijk voor de cargo."
                ],
                "answer": "Goedendag, ik heet Pierre.",
                "explanation": "Bonjour = goedendag, je m'appelle Pierre = ik heet Pierre."
            },
            {
                "type": "input",
                "question_nl": "Schrijf in het Frans: \"Ik werk bij Equinor.\"",
                "answer": "je travaille chez equinor",
                "explanation": "Je travaille chez Equinor."
            },
            {
                "type": "input",
                "question_nl": "Schrijf in het Frans: \"Ik heet David.\"",
                "answer": "je m'appelle david",
                "explanation": "Je m'appelle David."
            },
            {
                "type": "mc",
                "question_nl": "Welke Franse zin past bij: \"Ik ben graduate.\"?",
                "options": [
                    "Je travaille graduate.",
                    "Je suis graduate.",
                    "Je m'appelle graduate.",
                    "Je vais graduate.",
                    "Je suis travail graduate.",
                    "Je suis nouveau graduate Equinor."
                ],
                "answer": "Je suis graduate.",
                "explanation": "Je suis + rol: je suis graduate."
            },
            {
                "type": "order",
                "instruction_nl": "Zet de delen in de goede volgorde:",
                "parts": ["je", "m'appelle", "David"],
                "correct": ["je", "m'appelle", "David"],
                "explanation": "Je m'appelle David."
            },
            {
                "type": "order",
                "instruction_nl": "Zet de delen in de goede volgorde:",
                "parts": ["je", "travaille", "chez", "Equinor"],
                "correct": ["je", "travaille", "chez", "Equinor"],
                "explanation": "Je travaille chez Equinor."
            },
            {
                "type": "mc",
                "question_nl": "Welke begroeting is informeel?",
                "options": ["Bonjour", "Salut", "Bonsoir", "Au revoir", "Merci", "Pardon"],
                "answer": "Salut",
                "explanation": "Salut gebruik je informeel, bonjour is neutraler."
            },
            {
                "type": "input",
                "question_nl": "Vul aan: \"Bonjour, je ____ Piril.\" (ik ben Piril)",
                "answer": "suis",
                "explanation": "Je suis Piril."
            },
            {
                "type": "mc",
                "question_nl": "Wat zeg je NIET bij een eerste begroeting?",
                "options": [
                    "Bonjour",
                    "Salut",
                    "Je m'appelle Toon.",
                    "Je suis très chargé aujourd'hui.",
                    "Enchanté.",
                    "Je travaille chez Equinor."
                ],
                "answer": "Je suis très chargé aujourd'hui.",
                "explanation": "Over werkdruk praten komt meestal later in het gesprek."
            },
            {
                "type": "input",
                "question_nl": "Schrijf in het Frans: \"Aangenaam, ik ben David.\"",
                "answer": "enchanté, je suis david",
                "explanation": "Enchanté, je suis David."
            },
        ],
    },
    {
        "id": 2,
        "title": "2. Parler de ton travail (FR UI)",
        "goal_nl": "Je kunt in het Frans uitleggen wat je werk is.",
        "intro_audio_fr": "Dans ce chapitre, Piril et David parlent de leur travail comme charterer et market analyst.",
        "theory": """
### Objectif (FR)

Dans ce chapitre, l'interface est **en français**.  
Tu apprends à parler de ton travail et de ton premier projet.

### Phrases utiles

- Je suis market analyst chez GEA.  
- Je suis charterer.  
- Mon premier projet était un résumé d'un article.  
- J'ai donné un nom à un navire.  
- Nous avons déjeuné ensemble.  
""",
        "examples": [
            ("Je suis market analyst chez GEA.", "Ik ben market analyst bij GEA."),
            ("Je suis charterer.", "Ik ben charterer."),
            ("Mon premier projet était un résumé d'un article de presse.", "Mijn eerste project was een samenvatting van een nieuwsbericht."),
        ],
        "dialogue": {
            "title": "Dialogue: parler du travail et du premier projet",
            "turns": [
                (
                    "David",
                    "Je suis market analyst chez GEA. Mon premier projet était un résumé d'un article de presse.",
                    "Ik ben market analyst bij GEA. Mijn eerste project was een samenvatting van een nieuwsbericht."
                ),
                (
                    "Piril",
                    "Moi, je suis charterer. Mon premier jour, j'ai cherché un nom pour un navire.",
                    "Ik ben charterer. Op mijn eerste dag zocht ik een naam voor een schip."
                ),
                (
                    "David",
                    "Comment s'appelle le navire ?",
                    "Hoe heet het schip?"
                ),
                (
                    "Piril",
                    "Le navire s'appelle Stubben. Après ça, nous avons déjeuné ensemble.",
                    "Het schip heet Stubben. Daarna hebben we samen geluncht."
                ),
            ]
        },
        "reading": {
            "text_fr": (
                "Piril et David travaillent tous les deux à Stavanger. "
                "David est market analyst chez GEA. Il lit beaucoup de nouvelles sur le marché du gaz. "
                "Son premier projet était un résumé d'un article de presse important. "
                "Il a présenté son résumé à son équipe.\n\n"
                "Piril est charterer. Elle s'occupe des navires et des cargaisons. "
                "Le premier jour, elle a dû choisir un nom pour un nouveau navire. "
                "Elle a choisi le nom Stubben. Après le travail, Piril et David ont déjeuné ensemble "
                "et ont parlé de leurs premiers projets."
            ),
            "vocab": [
                ("travailler", "werken"),
                ("market analyst", "marktanalist"),
                ("nouvelles", "nieuws(berichten)"),
                ("résumé", "samenvatting"),
                ("équipe", "team"),
                ("charterer", "charterer (schepen inhuren)"),
                ("navire", "schip"),
                ("cargaison", "lading"),
                ("nom", "naam"),
                ("déjeuner", "lunchen / lunch")
            ],
            "questions": [
                {
                    "type": "mc",
                    "question_nl": "Waar werkt David?",
                    "options": [
                        "Bij Equinor.",
                        "Bij GEA.",
                        "Bij een bank.",
                        "Bij een school."
                    ],
                    "answer": "Bij GEA.",
                    "explanation": "« David est market analyst chez GEA. »"
                },
                {
                    "type": "mc",
                    "question_nl": "Wat was Davids eerste project?",
                    "options": [
                        "Een nieuwe naam zoeken voor een schip.",
                        "Een samenvatting maken van een nieuwsartikel.",
                        "Een schip naar Oslo sturen.",
                        "Een presentatie over auto's geven."
                    ],
                    "answer": "Een samenvatting maken van een nieuwsartikel.",
                    "explanation": "« Son premier projet était un résumé d'un article de presse important. »"
                },
                {
                    "type": "mc",
                    "question_nl": "Wat doet Piril als charterer?",
                    "options": [
                        "Ze schrijft alleen e-mails.",
                        "Ze maakt alleen tekeningen van schepen.",
                        "Ze houdt zich bezig met schepen en ladingen.",
                        "Ze werkt alleen in de kantine."
                    ],
                    "answer": "Ze houdt zich bezig met schepen en ladingen.",
                    "explanation": "« Elle s'occupe des navires et des cargaisons. »"
                },
                {
                    "type": "input",
                    "question_nl": "Hoe heet het nieuwe schip? Schrijf alleen de naam.",
                    "answer": "stubben",
                    "explanation": "Le navire s'appelle Stubben."
                },
                {
                    "type": "mc",
                    "question_nl": "Wat doen Piril en David na het werk?",
                    "options": [
                        "Ze gaan naar Oslo.",
                        "Ze gaan samen lunchen.",
                        "Ze gaan naar huis zonder te praten.",
                        "Ze gaan allebei sporten."
                    ],
                    "answer": "Ze gaan samen lunchen.",
                    "explanation": "« Après le travail, Piril et David ont déjeuné ensemble. »"
                },
                {
                    "type": "mc",
                    "question_nl": "Wat betekent \"cargaison\"?",
                    "options": [
                        "Scheepsnaam.",
                        "Lading.",
                        "Haven.",
                        "Motor."
                    ],
                    "answer": "Lading.",
                    "explanation": "La cargaison = de lading."
                },
                {
                    "type": "mc",
                    "question_nl": "Wat betekent \"résumé\"?",
                    "options": [
                        "Een volledig rapport.",
                        "Een samenvatting.",
                        "Een boek.",
                        "Een vakantie."
                    ],
                    "answer": "Een samenvatting.",
                    "explanation": "Un résumé = een samenvatting."
                },
                {
                    "type": "input",
                    "question_nl": "Schrijf in het Frans: \"Een schip\" (met lidwoord).",
                    "answer": "un navire",
                    "explanation": "Un navire."
                },
                {
                    "type": "mc",
                    "question_nl": "In welke zin past het woord \"déjeuner\"?",
                    "options": [
                        "Je déjeuner à neuf heures.",
                        "Nous déjeunons ensemble à midi.",
                        "Il déjeuner un navire.",
                        "Je déjeune un marché."
                    ],
                    "answer": "Nous déjeunons ensemble à midi.",
                    "explanation": "Déjeuner = lunchen."
                },
                {
                    "type": "input",
                    "question_nl": "Schrijf in het Frans: \"Ik werk met een team.\" (je ...)",
                    "answer": "je travaille avec une équipe",
                    "explanation": "Je travaille avec une équipe."
                },
            ]
        },
        "write_hint": (
            "Schrijf 3–5 zinnen over jouw werk.\n"
            "- je suis ... (functie)\n"
            "- je travaille ... (bedrijf / plaats)\n"
            "- mon premier projet était ...\n"
        ),
        "write_example": """Je suis market analyst.
Je travaille chez GEA à Stavanger.
Mon premier projet était un résumé d'un article de presse.""",
        "exercises": [
            {
                "type": "mc",
                "question_nl": "Wat betekent: « Je suis market analyst chez GEA. »?",
                "options": [
                    "Ik ben kapitein bij GEA.",
                    "Ik ben market analyst bij GEA.",
                    "Ik ben charterer bij GEA.",
                    "Ik ben student bij GEA."
                ],
                "answer": "Ik ben market analyst bij GEA.",
                "explanation": "Je suis market analyst chez GEA."
            },
            {
                "type": "input",
                "question_nl": "Schrijf in het Frans: \"Ik ben charterer.\"",
                "answer": "je suis charterer",
                "explanation": "Je suis charterer."
            },
            {
                "type": "input",
                "question_nl": "Schrijf in het Frans: \"Mijn eerste project was een samenvatting.\" (korte versie)",
                "answer": "mon premier projet était un résumé",
                "explanation": "Mon premier projet était un résumé."
            },
            {
                "type": "mc",
                "question_nl": "Welke zin betekent: \"Ik werk bij GEA.\"?",
                "options": [
                    "Je suis GEA.",
                    "Je travaille chez GEA.",
                    "Je vais GEA.",
                    "Je fais GEA."
                ],
                "answer": "Je travaille chez GEA.",
                "explanation": "Travailler chez + bedrijf."
            },
            {
                "type": "order",
                "instruction_nl": "Zet de delen in de goede volgorde:",
                "parts": ["je", "travaille", "chez", "GEA"],
                "correct": ["je", "travaille", "chez", "GEA"],
                "explanation": "Je travaille chez GEA."
            },
            {
                "type": "order",
                "instruction_nl": "Zet de delen in de goede volgorde:",
                "parts": ["mon", "premier", "projet", "était", "un", "résumé"],
                "correct": ["mon", "premier", "projet", "était", "un", "résumé"],
                "explanation": "Mon premier projet était un résumé."
            },
            {
                "type": "mc",
                "question_nl": "Wat betekent \"navire\"?",
                "options": ["Vliegtuig.", "Schip.", "Trein.", "Truck."],
                "answer": "Schip.",
                "explanation": "Un navire = een schip."
            },
            {
                "type": "input",
                "question_nl": "Schrijf in het Frans: \"Het schip heet Stubben.\"",
                "answer": "le navire s'appelle stubben",
                "explanation": "Le navire s'appelle Stubben."
            },
            {
                "type": "mc",
                "question_nl": "Welke zin kun je gebruiken na het werk?",
                "options": [
                    "Nous déjeunons ensemble.",
                    "Nous dormons ensemble au bureau.",
                    "Nous nageons dans le navire.",
                    "Nous lisons un camion."
                ],
                "answer": "Nous déjeunons ensemble.",
                "explanation": "Samen lunchen = nous déjeunons ensemble."
            },
            {
                "type": "input",
                "question_nl": "Schrijf in het Frans: \"Ik lees nieuws.\" (je ... des nouvelles)",
                "answer": "je lis des nouvelles",
                "explanation": "Je lis des nouvelles."
            },
        ],
    },
    {
        "id": 3,
        "title": "3. Smalltalk: hoe gaat het in Stavanger?",
        "goal_nl": "Je kunt praten over hoe het met je gaat in Stavanger.",
        "intro_audio_fr": "Un mois plus tard, Piril et David se voient à Stavanger et parlent de leur vie.",
        "theory": """
### Doel

Je leert:

- vragen hoe het gaat na een tijdje  
- zeggen dat het goed of slecht gaat  
- kort praten over emoties en privéleven

### Kernzinnen

- Ça va ? → Hoe gaat het?  
- Ça va bien. → Het gaat goed.  
- Je suis un peu déprimé. → Ik ben een beetje depressief.  
- Je sors avec quelqu'un. → Ik ben aan het daten.  
""",
        "examples": [
            ("Salut, ça va à Stavanger ?", "Hoi, hoe gaat het in Stavanger?"),
            ("Je suis un peu déprimé.", "Ik ben een beetje depressief."),
            ("Je sors avec quelqu'un.", "Ik ben met iemand aan het daten."),
        ],
        "dialogue": {
            "title": "Dialoog: een maand later in Stavanger",
            "turns": [
                (
                    "Piril",
                    "Salut David, ça va ? Ça fait un mois à Stavanger.",
                    "Hoi David, hoe gaat het? We zijn nu een maand in Stavanger."
                ),
                (
                    "David",
                    "Honnêtement, je suis un peu déprimé. Le temps est difficile pour moi.",
                    "Eerlijk gezegd ben ik een beetje depressief. Het weer is moeilijk voor mij."
                ),
                (
                    "Piril",
                    "Je comprends. Pour moi, ça va bien. Je sors avec quelqu'un et je découvre la ville.",
                    "Ik begrijp het. Met mij gaat het goed. Ik ben aan het daten en ik ontdek de stad."
                ),
            ]
        },
        "reading": {
            "text_fr": (
                "Un mois après leur premier jour de travail, Piril et David restent à Stavanger. "
                "Stavanger est une petite ville au bord de la mer. Il pleut souvent et il fait parfois très froid.\n\n"
                "Pour David, la vie est un peu difficile. Il vient des Pays-Bas, et il trouve le temps très sombre. "
                "Il dit souvent qu'il est un peu déprimé. Il travaille beaucoup et il ne connaît pas beaucoup de gens.\n\n"
                "Pour Piril, la situation est différente. Elle aime la ville et la nature autour de Stavanger. "
                "Elle a commencé à sortir avec quelqu'un. Elle découvre des cafés, des restaurants et des parcs. "
                "Elle se sent plus à l'aise ici."
            ),
            "vocab": [
                ("au bord de la mer", "aan zee"),
                ("il pleut", "het regent"),
                ("sombre", "donker"),
                ("déprimé(e)", "depressief"),
                ("travailler beaucoup", "veel werken"),
                ("connaître", "kennen"),
                ("sortir avec quelqu'un", "met iemand daten"),
                ("découvrir", "ontdekken"),
                ("café", "café"),
                ("à l'aise", "op zijn/haar gemak")
            ],
            "questions": [
                {
                    "type": "mc",
                    "question_nl": "Hoeveel tijd is er ongeveer voorbij sinds de eerste werkdag?",
                    "options": [
                        "Een dag.",
                        "Een week.",
                        "Een maand.",
                        "Een jaar."
                    ],
                    "answer": "Een maand.",
                    "explanation": "« Un mois après leur premier jour de travail... »"
                },
                {
                    "type": "mc",
                    "question_nl": "Hoe gaat het met David in Stavanger?",
                    "options": [
                        "Heel goed, hij is blij.",
                        "Hij is een beetje depressief.",
                        "Hij is boos op iedereen.",
                        "Hij is op vakantie."
                    ],
                    "answer": "Hij is een beetje depressief.",
                    "explanation": "Hij zegt dat hij « un peu déprimé » is."
                },
                {
                    "type": "mc",
                    "question_nl": "Waarom vindt David het moeilijk?",
                    "options": [
                        "Omdat hij geen werk heeft.",
                        "Omdat hij het weer heel donker vindt.",
                        "Omdat hij te veel vrienden heeft.",
                        "Omdat hij te veel kaas eet."
                    ],
                    "answer": "Omdat hij het weer heel donker vindt.",
                    "explanation": "« Il trouve le temps très sombre. »"
                },
                {
                    "type": "mc",
                    "question_nl": "Hoe voelt Piril zich in Stavanger?",
                    "options": [
                        "Ze voelt zich slecht.",
                        "Ze is bang voor de stad.",
                        "Ze voelt zich meer op haar gemak.",
                        "Ze wil meteen weg."
                    ],
                    "answer": "Ze voelt zich meer op haar gemak.",
                    "explanation": "« Elle se sent plus à l'aise ici. »"
                },
                {
                    "type": "input",
                    "question_nl": "Schrijf in het Frans: \"Ik ben een beetje depressief.\"",
                    "answer": "je suis un peu déprimé",
                    "explanation": "Je suis un peu déprimé."
                },
                {
                    "type": "mc",
                    "question_nl": "Wat betekent \"au bord de la mer\"?",
                    "options": [
                        "In de bergen.",
                        "Aan zee.",
                        "In de woestijn.",
                        "In het centrum."
                    ],
                    "answer": "Aan zee.",
                    "explanation": "Au bord de la mer = aan zee."
                },
                {
                    "type": "mc",
                    "question_nl": "Wat betekent \"sortir avec quelqu'un\"?",
                    "options": [
                        "Met iemand werken.",
                        "Met iemand daten.",
                        "Met iemand ruzie hebben.",
                        "Met iemand bellen."
                    ],
                    "answer": "Met iemand daten.",
                    "explanation": "Sortir avec quelqu'un = met iemand uitgaan / daten."
                },
                {
                    "type": "input",
                    "question_nl": "Schrijf in het Frans: \"Ik ontdek cafés en parken.\" (je ... cafés et des parcs)",
                    "answer": "je découvre des cafés et des parcs",
                    "explanation": "Je découvre des cafés et des parcs."
                },
                {
                    "type": "mc",
                    "question_nl": "In welke zin past \"à l'aise\" het beste?",
                    "options": [
                        "Je suis très à l'aise ici.",
                        "Je mange à l'aise un navire.",
                        "Je voyage à l'aise un camion.",
                        "Je dors à l'aise une pluie."
                    ],
                    "answer": "Je suis très à l'aise ici.",
                    "explanation": "Zich op zijn gemak voelen = être à l'aise."
                },
                {
                    "type": "input",
                    "question_nl": "Schrijf in het Frans: \"Het regent vaak.\"",
                    "answer": "il pleut souvent",
                    "explanation": "Il pleut souvent."
                },
            ]
        },
        "write_hint": (
            "Schrijf 3–5 zinnen over hoe het met jou gaat in Stavanger.\n"
            "- ça va bien / je suis un peu déprimé\n"
            "- j'aime / je n'aime pas le temps\n"
        ),
        "write_example": """Ça va un peu difficile pour moi.
Je suis un peu déprimé parce qu'il pleut souvent.
Mais j'aime la ville et je découvre des cafés.""",
        "exercises": [
            {
                "type": "mc",
                "question_nl": "Wat betekent: « Ça va ? »?",
                "options": [
                    "Gaat het regenen?",
                    "Hoe gaat het?",
                    "Waar ga je naartoe?",
                    "Hoe heet je?"
                ],
                "answer": "Hoe gaat het?",
                "explanation": "Ça va ? = hoe gaat het?"
            },
            {
                "type": "input",
                "question_nl": "Schrijf in het Frans: \"Het gaat goed, dank je.\"",
                "answer": "ça va bien, merci",
                "explanation": "Ça va bien, merci."
            },
            {
                "type": "mc",
                "question_nl": "Welke zin betekent: \"Ik ben een beetje depressief.\"?",
                "options": [
                    "Je suis très content.",
                    "Je suis un peu déprimé.",
                    "Je suis très calme.",
                    "Je suis un peu chaud."
                ],
                "answer": "Je suis un peu déprimé.",
                "explanation": "Un peu déprimé = een beetje depressief."
            },
            {
                "type": "input",
                "question_nl": "Schrijf in het Frans: \"Ik ben aan het daten.\"",
                "answer": "je sors avec quelqu'un",
                "explanation": "Je sors avec quelqu'un."
            },
            {
                "type": "order",
                "instruction_nl": "Zet de delen in de goede volgorde:",
                "parts": ["ça", "?", "va"],
                "correct": ["ça", "va", "?"],
                "explanation": "Ça va ?"
            },
            {
                "type": "mc",
                "question_nl": "Wat betekent \"sombre\"?",
                "options": [
                    "Licht.",
                    "Donker.",
                    "Warm.",
                    "Rustig."
                ],
                "answer": "Donker.",
                "explanation": "Sombre = donker."
            },
            {
                "type": "input",
                "question_nl": "Schrijf in het Frans: \"Ik werk veel.\" (je ... beaucoup)",
                "answer": "je travaille beaucoup",
                "explanation": "Je travaille beaucoup."
            },
            {
                "type": "mc",
                "question_nl": "Welke zin past NIET bij smalltalk over hoe het gaat?",
                "options": [
                    "Ça va bien.",
                    "Je suis un peu déprimé.",
                    "Je sors avec quelqu'un.",
                    "Je mange un navire."
                ],
                "answer": "Je mange un navire.",
                "explanation": "Een schip eten past niet in het gesprek."
            },
            {
                "type": "input",
                "question_nl": "Schrijf in het Frans: \"Ik ken niet veel mensen.\" (je ne ... pas beaucoup de gens)",
                "answer": "je ne connais pas beaucoup de gens",
                "explanation": "Je ne connais pas beaucoup de gens."
            },
            {
                "type": "mc",
                "question_nl": "Welke combinatie klopt?",
                "options": [
                    "Je déprime ça va.",
                    "Je suis déprimé.",
                    "Je déprimé suis.",
                    "Je suis sombre moi."
                ],
                "answer": "Je suis déprimé.",
                "explanation": "Je suis + bijvoeglijk naamwoord."
            },
        ],
    },
    {
        "id": 4,
        "title": "4. Werkdruk en reizen naar Oslo",
        "goal_nl": "Je kunt praten over werkdruk en reizen voor je werk.",
        "intro_audio_fr": "David et Piril parlent de la charge de travail et des voyages à Oslo.",
        "theory": """
### Doel

Je leert:

- zeggen dat je het druk hebt  
- vertellen dat je moet reizen voor werk  
- kort iets over werkplezier en relatie

### Kernzinnen

- J'ai beaucoup de travail. → Ik heb veel werk.  
- Je vais souvent à Oslo pour le travail. → Ik ga vaak naar Oslo voor werk.  
- J'aime beaucoup mon travail. → Ik vind mijn werk erg leuk.  
- Ma relation va bien. → Het gaat goed met mijn relatie.  
""",
        "examples": [
            ("J'ai beaucoup de travail en ce moment.", "Ik heb veel werk op dit moment."),
            ("Je vais souvent à Oslo pour le travail.", "Ik ga vaak naar Oslo voor werk."),
            ("J'aime beaucoup mon travail.", "Ik vind mijn werk erg leuk."),
        ],
        "dialogue": {
            "title": "Dialoog: werkdruk en toekomst",
            "turns": [
                (
                    "David",
                    "En ce moment, j'ai beaucoup de travail. Je vais souvent à Oslo pour le travail.",
                    "Op dit moment heb ik veel werk. Ik ga vaak naar Oslo voor werk."
                ),
                (
                    "Piril",
                    "Tu aimes ton travail ?",
                    "Vind je je werk leuk?"
                ),
                (
                    "David",
                    "Oui, j'aime beaucoup mon travail, et ma relation va bien aussi.",
                    "Ja, ik vind mijn werk erg leuk en het gaat ook goed met mijn relatie."
                ),
                (
                    "Piril",
                    "Moi aussi, j'aime mon travail. Je regarde les possibilités pour rester ici.",
                    "Ik vind mijn werk ook leuk. Ik kijk naar mogelijkheden om hier te blijven."
                ),
            ]
        },
        "reading": {
            "text_fr": (
                "Après quelques mois, David a une charge de travail très importante. "
                "Il doit analyser beaucoup de données de marché et préparer des rapports. "
                "Il va souvent à Oslo pour des réunions avec d'autres équipes. "
                "Les voyages sont fatigants, mais il aime beaucoup son travail.\n\n"
                "Sa relation va bien. Il parle souvent avec son/sa partenaire par téléphone "
                "quand il est en voyage. Ils planifient leurs week-ends ensemble.\n\n"
                "Piril, de son côté, aime aussi beaucoup son travail de charterer. "
                "Elle regarde les possibilités pour rester plus longtemps à Stavanger. "
                "Elle parle avec son manager de son futur contrat."
            ),
            "vocab": [
                ("charge de travail", "werkdruk"),
                ("analyser", "analyseren"),
                ("réunion", "vergadering"),
                ("fatigant(e)", "vermoeiend"),
                ("relation", "relatie"),
                ("téléphone", "telefoon"),
                ("planifier", "plannen"),
                ("possibilités", "mogelijkheden"),
                ("rester", "blijven"),
                ("contrat", "contract")
            ],
            "questions": [
                {
                    "type": "mc",
                    "question_nl": "Wat doet David vaak voor zijn werk?",
                    "options": [
                        "Hij gaat vaak naar Oslo.",
                        "Hij gaat vaak naar Parijs.",
                        "Hij gaat vaak naar school.",
                        "Hij gaat vaak naar huis."
                    ],
                    "answer": "Hij gaat vaak naar Oslo.",
                    "explanation": "« Il va souvent à Oslo pour des réunions. »"
                },
                {
                    "type": "mc",
                    "question_nl": "Hoe voelt David zich over zijn werk?",
                    "options": [
                        "Hij vindt het niet leuk.",
                        "Hij heeft geen mening.",
                        "Hij vindt zijn werk erg leuk.",
                        "Hij wil direct stoppen."
                    ],
                    "answer": "Hij vindt zijn werk erg leuk.",
                    "explanation": "« il aime beaucoup son travail. »"
                },
                {
                    "type": "mc",
                    "question_nl": "Hoe gaat het met Davids relatie?",
                    "options": [
                        "Slecht.",
                        "Hij zegt er niets over.",
                        "Het gaat goed.",
                        "Hij heeft geen relatie."
                    ],
                    "answer": "Het gaat goed.",
                    "explanation": "« Sa relation va bien. »"
                },
                {
                    "type": "input",
                    "question_nl": "Schrijf in het Frans: \"Ik heb veel werkdruk.\" (j'ai ...)",
                    "answer": "j'ai une grande charge de travail",
                    "explanation": "J'ai une grande charge de travail."
                },
                {
                    "type": "mc",
                    "question_nl": "Wat doet Piril met betrekking tot de toekomst?",
                    "options": [
                        "Ze zoekt een andere stad.",
                        "Ze kijkt naar mogelijkheden om in Stavanger te blijven.",
                        "Ze wil direct stoppen met werken.",
                        "Ze wil naar school gaan."
                    ],
                    "answer": "Ze kijkt naar mogelijkheden om in Stavanger te blijven.",
                    "explanation": "« Elle regarde les possibilités pour rester plus longtemps à Stavanger. »"
                },
                {
                    "type": "mc",
                    "question_nl": "Wat betekent \"réunion\"?",
                    "options": [
                        "Reis.",
                        "Vergadering.",
                        "Vakantie.",
                        "Opleiding."
                    ],
                    "answer": "Vergadering.",
                    "explanation": "Une réunion = een vergadering."
                },
                {
                    "type": "mc",
                    "question_nl": "Wat betekent \"contrat\"?",
                    "options": [
                        "Contract.",
                        "Weekend.",
                        "Reis.",
                        "Relatie."
                    ],
                    "answer": "Contract.",
                    "explanation": "Un contrat = een contract."
                },
                {
                    "type": "input",
                    "question_nl": "Schrijf in het Frans: \"De reizen zijn vermoeiend.\" (les voyages ...)",
                    "answer": "les voyages sont fatigants",
                    "explanation": "Les voyages sont fatigants."
                },
                {
                    "type": "mc",
                    "question_nl": "In welke zin past \"planifier\" goed?",
                    "options": [
                        "Je planifie mon contrat.",
                        "Je planifie nos week-ends.",
                        "Je planifie le téléphone.",
                        "Je planifie une fatigue."
                    ],
                    "answer": "Je planifie nos week-ends.",
                    "explanation": "Weekenden plannen = planifier nos week-ends."
                },
                {
                    "type": "input",
                    "question_nl": "Schrijf in het Frans: \"Ik praat met mijn manager.\" (je ... avec mon manager)",
                    "answer": "je parle avec mon manager",
                    "explanation": "Je parle avec mon manager."
                },
            ]
        },
        "write_hint": (
            "Schrijf 3–5 zinnen over jouw werkdruk en reizen.\n"
            "- j'ai beaucoup de travail\n"
            "- je vais souvent à ... pour le travail\n"
            "- j'aime / je n'aime pas voyager\n"
        ),
        "write_example": """En ce moment, j'ai beaucoup de travail.
Je vais parfois à Oslo pour des réunions.
J'aime mon travail, mais les voyages sont fatigants.""",
        "exercises": [
            {
                "type": "mc",
                "question_nl": "Wat betekent: « J'ai beaucoup de travail. »?",
                "options": [
                    "Ik heb veel werk.",
                    "Ik heb weinig werk.",
                    "Ik heb geen werk.",
                    "Ik ben op vakantie."
                ],
                "answer": "Ik heb veel werk.",
                "explanation": "Beaucoup de travail = veel werk."
            },
            {
                "type": "input",
                "question_nl": "Schrijf in het Frans: \"Ik ga vaak naar Oslo voor werk.\"",
                "answer": "je vais souvent à oslo pour le travail",
                "explanation": "Je vais souvent à Oslo pour le travail."
            },
            {
                "type": "mc",
                "question_nl": "Welke zin betekent: \"Het gaat goed met mijn relatie.\"?",
                "options": [
                    "Ma relation est froide.",
                    "Ma relation va bien.",
                    "Ma relation ne va pas.",
                    "Je n'ai pas de relation."
                ],
                "answer": "Ma relation va bien.",
                "explanation": "Ma relation va bien."
            },
            {
                "type": "input",
                "question_nl": "Schrijf in het Frans: \"Ik praat vaak met mijn partner.\" (je ... souvent)",
                "answer": "je parle souvent avec mon partenaire",
                "explanation": "Je parle souvent avec mon partenaire."
            },
            {
                "type": "order",
                "instruction_nl": "Zet de delen in de goede volgorde:",
                "parts": ["je", "vais", "souvent", "à Oslo"],
                "correct": ["je", "vais", "souvent", "à Oslo"],
                "explanation": "Je vais souvent à Oslo."
            },
            {
                "type": "mc",
                "question_nl": "Wat betekent \"fatigant\"?",
                "options": [
                    "Leuk.",
                    "Rustig.",
                    "Vermoeiend.",
                    "Gevaarlijk."
                ],
                "answer": "Vermoeiend.",
                "explanation": "Fatigant = vermoeiend."
            },
            {
                "type": "input",
                "question_nl": "Schrijf in het Frans: \"Ik hou veel van mijn werk.\" (j'aime ...)",
                "answer": "j'aime beaucoup mon travail",
                "explanation": "J'aime beaucoup mon travail."
            },
            {
                "type": "mc",
                "question_nl": "Welke combinatie is correct?",
                "options": [
                    "J'ai vais beaucoup de travail.",
                    "Je vais beaucoup de travail.",
                    "J'ai beaucoup de travail.",
                    "Je beaucoup de travail vais."
                ],
                "answer": "J'ai beaucoup de travail.",
                "explanation": "J'ai + beaucoup de travail."
            },
            {
                "type": "input",
                "question_nl": "Schrijf in het Frans: \"Ik wil hier blijven.\" (je veux ...)",
                "answer": "je veux rester ici",
                "explanation": "Je veux rester ici."
            },
            {
                "type": "mc",
                "question_nl": "Wat betekent \"possibilités\"?",
                "options": [
                    "Problemen.",
                    "Mogelijkheden.",
                    "Schepen.",
                    "Cargolijsten."
                ],
                "answer": "Mogelijkheden.",
                "explanation": "Des possibilités = mogelijkheden."
            },
        ],
    },
    {
        "id": 5,
        "title": "5. Een korte dialoog over de toekomst",
        "goal_nl": "Je oefent een vrije dialoog over plannen en toekomst.",
        "intro_audio_fr": "Piril et David parlent de leurs plans pour l'avenir et du week-end.",
        "theory": """
### Doel

Je leert:

- in eenvoudige zinnen praten over toekomstplannen  
- woorden als morgen, volgend jaar, later gebruiken

### Kernzinnen

- Demain, je travaille au terminal. → Morgen werk ik op de terminal.  
- Plus tard, je veux rester à Stavanger. → Later wil ik in Stavanger blijven.  
- L'année prochaine, je veux apprendre plus de français. → Volgend jaar wil ik meer Frans leren.  
""",
        "examples": [
            ("Demain, je travaille au terminal.", "Morgen werk ik op de terminal."),
            ("Plus tard, je veux rester à Stavanger.", "Later wil ik in Stavanger blijven."),
        ],
        "dialogue": {
            "title": "Dialoog: plannen voor de toekomst (zelf verzonnen)",
            "turns": [
                (
                    "David",
                    "Demain, je travaille au terminal, mais le week-end je veux me reposer.",
                    "Morgen werk ik op de terminal, maar in het weekend wil ik uitrusten."
                ),
                (
                    "Piril",
                    "Moi, je veux visiter un fjord ce week-end.",
                    "Ik wil dit weekend een fjord bezoeken."
                ),
                (
                    "David",
                    "Plus tard, je veux rester à Stavanger et parler mieux français.",
                    "Later wil ik in Stavanger blijven en beter Frans spreken."
                ),
                (
                    "Piril",
                    "L'année prochaine, je veux faire un grand voyage.",
                    "Volgend jaar wil ik een grote reis maken."
                ),
            ]
        },
        "reading": {
            "text_fr": (
                "Piril et David parlent souvent de leurs projets pour l'avenir. "
                "David veut rester à Stavanger au moins deux ans. "
                "Il veut apprendre plus de français et comprendre mieux ses collègues. "
                "Il pense aussi à un nouveau poste plus tard.\n\n"
                "Piril aime voyager. Elle veut faire un grand voyage en Norvège l'année prochaine. "
                "Elle regarde des photos de fjords et de montagnes. "
                "Elle veut aussi continuer à travailler dans le domaine du shipping. "
                "Pour le moment, elle reste concentrée sur son travail actuel."
            ),
            "vocab": [
                ("projets", "plannen"),
                ("au moins", "minstens"),
                ("poste", "functie / baan"),
                ("voyager", "reizen"),
                ("fjord", "fjord"),
                ("montagne", "berg"),
                ("domaine", "domein / vakgebied"),
                ("shipping", "shipping / scheepvaart"),
                ("pour le moment", "voor nu"),
                ("concentré(e)", "geconcentreerd")
            ],
            "questions": [
                {
                    "type": "mc",
                    "question_nl": "Hoe lang wil David minstens in Stavanger blijven?",
                    "options": [
                        "Een maand.",
                        "Een jaar.",
                        "Twee jaar.",
                        "Tien jaar."
                    ],
                    "answer": "Twee jaar.",
                    "explanation": "« Il veut rester à Stavanger au moins deux ans. »"
                },
                {
                    "type": "mc",
                    "question_nl": "Wat wil David verbeteren?",
                    "options": [
                        "Zijn Engels.",
                        "Zijn Frans.",
                        "Zijn Noors.",
                        "Zijn Duits."
                    ],
                    "answer": "Zijn Frans.",
                    "explanation": "Hij wil meer Frans leren."
                },
                {
                    "type": "mc",
                    "question_nl": "Wat wil Piril volgend jaar doen?",
                    "options": [
                        "Ze wil in Frankrijk wonen.",
                        "Ze wil een grote reis in Noorwegen maken.",
                        "Ze wil in Nederland studeren.",
                        "Ze wil stoppen met werken."
                    ],
                    "answer": "Ze wil een grote reis in Noorwegen maken.",
                    "explanation": "« Elle veut faire un grand voyage en Norvège l'année prochaine. »"
                },
                {
                    "type": "input",
                    "question_nl": "Schrijf in het Frans: \"Ik wil blijven in Stavanger.\" (je veux ...)",
                    "answer": "je veux rester à stavanger",
                    "explanation": "Je veux rester à Stavanger."
                },
                {
                    "type": "mc",
                    "question_nl": "Wat betekent \"projets\"?",
                    "options": [
                        "Problemen.",
                        "Plannen.",
                        "Contracten.",
                        "Cargolijsten."
                    ],
                    "answer": "Plannen.",
                    "explanation": "Des projets = plannen."
                },
                {
                    "type": "mc",
                    "question_nl": "Wat betekent \"domaine du shipping\"?",
                    "options": [
                        "Domein van auto's.",
                        "Domein van scheepvaart.",
                        "Domein van sport.",
                        "Domein van muziek."
                    ],
                    "answer": "Domein van scheepvaart.",
                    "explanation": "Domaine du shipping = scheepvaartdomein."
                },
                {
                    "type": "input",
                    "question_nl": "Schrijf in het Frans: \"Voor nu blijf ik geconcentreerd.\" (pour le moment, ...)",
                    "answer": "pour le moment, je reste concentré",
                    "explanation": "Pour le moment, je reste concentré."
                },
                {
                    "type": "mc",
                    "question_nl": "In welke zin past \"au moins\" goed?",
                    "options": [
                        "Je vais au moins un navire.",
                        "Je reste au moins deux ans ici.",
                        "Je mange au moins un téléphone.",
                        "Je travaille au moins une montagne."
                    ],
                    "answer": "Je reste au moins deux ans ici.",
                    "explanation": "Minstens twee jaar blijven."
                },
                {
                    "type": "input",
                    "question_nl": "Schrijf in het Frans: \"Ik kijk naar foto's van fjorden.\" (je ... des photos de fjords)",
                    "answer": "je regarde des photos de fjords",
                    "explanation": "Je regarde des photos de fjords."
                },
                {
                    "type": "mc",
                    "question_nl": "Wat betekent \"pour le moment\"?",
                    "options": [
                        "Voor altijd.",
                        "Voor nu.",
                        "Voor gisteren.",
                        "Voor later."
                    ],
                    "answer": "Voor nu.",
                    "explanation": "Pour le moment = voor nu."
                },
            ]
        },
        "write_hint": (
            "Schrijf 3–5 zinnen over jouw toekomstplannen.\n"
            "- l'année prochaine, je veux ...\n"
            "- plus tard, je veux ...\n"
        ),
        "write_example": """L'année prochaine, je veux apprendre plus de français.
Plus tard, je veux rester dans le domaine du gaz.
Je veux aussi visiter les fjords en Norvège.""",
        "exercises": [
            {
                "type": "mc",
                "question_nl": "Wat betekent: « Demain, je travaille au terminal. »?",
                "options": [
                    "Ik werk vandaag op de terminal.",
                    "Morgen werk ik op de terminal.",
                    "Ik heb morgen vrij.",
                    "Ik ga nooit naar de terminal."
                ],
                "answer": "Morgen werk ik op de terminal.",
                "explanation": "Demain = morgen."
            },
            {
                "type": "input",
                "question_nl": "Schrijf in het Frans: \"Volgend jaar wil ik meer Frans leren.\"",
                "answer": "l'année prochaine, je veux apprendre plus de français",
                "explanation": "L'année prochaine, je veux apprendre plus de français."
            },
            {
                "type": "mc",
                "question_nl": "Welke zin betekent: \"Later wil ik in Stavanger blijven.\"?",
                "options": [
                    "Plus tard, je veux rester à Stavanger.",
                    "Plus tard, je veux quitter Stavanger.",
                    "Plus tard, je veux nager à Stavanger.",
                    "Plus tard, je veux vendre Stavanger."
                ],
                "answer": "Plus tard, je veux rester à Stavanger.",
                "explanation": "Plus tard, je veux rester à Stavanger."
            },
            {
                "type": "input",
                "question_nl": "Schrijf in het Frans: \"Dit weekend wil ik rusten.\" (ce week-end, ...)",
                "answer": "ce week-end, je veux me reposer",
                "explanation": "Ce week-end, je veux me reposer."
            },
            {
                "type": "order",
                "instruction_nl": "Zet de delen in de goede volgorde:",
                "parts": ["je", "veux", "rester", "ici"],
                "correct": ["je", "veux", "rester", "ici"],
                "explanation": "Je veux rester ici."
            },
            {
                "type": "mc",
                "question_nl": "Wat betekent \"voyager\"?",
                "options": [
                    "Werken.",
                    "Reizen.",
                    "Eten.",
                    "Slapen."
                ],
                "answer": "Reizen.",
                "explanation": "Voyager = reizen."
            },
            {
                "type": "input",
                "question_nl": "Schrijf in het Frans: \"Ik wil in het shipping-domein blijven.\" (je veux ...)",
                "answer": "je veux rester dans le domaine du shipping",
                "explanation": "Je veux rester dans le domaine du shipping."
            },
            {
                "type": "mc",
                "question_nl": "Welke combinatie klopt?",
                "options": [
                    "Je veux rester demain ici.",
                    "Je veux ici rester plus tard.",
                    "Je veux rester ici plus tard.",
                    "Plus tard je veux ici rester."
                ],
                "answer": "Je veux rester ici plus tard.",
                "explanation": "Je veux rester ici plus tard."
            },
            {
                "type": "input",
                "question_nl": "Schrijf in het Frans: \"We praten vaak over onze plannen.\" (nous ... souvent de nos projets)",
                "answer": "nous parlons souvent de nos projets",
                "explanation": "Nous parlons souvent de nos projets."
            },
            {
                "type": "mc",
                "question_nl": "Wat betekent \"l'année prochaine\"?",
                "options": [
                    "Volgend jaar.",
                    "Volgende maand.",
                    "Volgende week.",
                    "Volgende dag."
                ],
                "answer": "Volgend jaar.",
                "explanation": "L'année prochaine = volgend jaar."
            },
        ],
    },
    {
        "id": 6,
        "title": "6. Hobby's en voorkeuren",
        "goal_nl": "Je kunt praten over hobby's en dingen die je niet leuk vindt.",
        "intro_audio_fr": "Piril et David parlent de leurs hobbies et de ce qu'ils n'aiment pas.",
        "theory": """
### Doel

Je leert:

- zeggen wat je leuk vindt  
- zeggen wat je niet leuk vindt  
- spreken over hobby's en angsten

### Kernzinnen

- J'aime les voitures. → Ik hou van auto's.  
- Je n'aime pas les motos. → Ik hou niet van motoren.  
- Je n'aime pas le fromage. → Ik vind kaas niet lekker.  
- Je n'aime pas les maisons laides. → Ik hou niet van lelijke huizen.  
- J'ai peur de l'avion. → Ik ben bang om te vliegen.  
""",
        "examples": [
            ("J'aime les voitures.", "Ik hou van auto's."),
            ("Je n'aime pas les motos.", "Ik hou niet van motoren."),
            ("J'ai peur de l'avion.", "Ik ben bang om te vliegen."),
        ],
        "dialogue": {
            "title": "Dialoog: hobby's en wat ze niet leuk vinden",
            "turns": [
                (
                    "David",
                    "J'aime beaucoup les voitures, mais je n'aime pas du tout les motos.",
                    "Ik hou erg van auto's, maar ik hou absoluut niet van motoren."
                ),
                (
                    "David",
                    "Je n'aime pas le fromage non plus.",
                    "Ik vind kaas ook niet lekker."
                ),
                (
                    "Piril",
                    "Moi, je n'aime pas les maisons laides, et j'ai peur de l'avion.",
                    "Ik hou niet van lelijke huizen, en ik ben bang om te vliegen."
                ),
            ]
        },
        "reading": {
            "text_fr": (
                "David et Piril parlent de leurs hobbies. David aime beaucoup les voitures. "
                "Il regarde souvent des vidéos de voitures sur internet. "
                "Il n'aime pas du tout les motos, il trouve que c'est trop dangereux. "
                "Il n'aime pas le fromage non plus.\n\n"
                "Piril, elle, aime marcher en ville et regarder les maisons. "
                "Elle n'aime pas les maisons laides avec beaucoup de béton. "
                "Elle préfère les petites maisons en bois. "
                "Elle a aussi peur de l'avion. Elle n'aime pas voler, même pour les vacances."
            ),
            "vocab": [
                ("aimer", "leuk vinden / houden van"),
                ("voiture", "auto"),
                ("moto", "motor"),
                ("dangereux / dangereuse", "gevaarlijk"),
                ("fromage", "kaas"),
                ("maison", "huis"),
                ("béton", "beton"),
                ("bois", "hout"),
                ("avoir peur de", "bang zijn voor"),
                ("voler", "vliegen")
            ],
            "questions": [
                {
                    "type": "mc",
                    "question_nl": "Wat vindt David leuk?",
                    "options": [
                        "Motoren.",
                        "Auto's.",
                        "Kaas.",
                        "Vliegen."
                    ],
                    "answer": "Auto's.",
                    "explanation": "« David aime beaucoup les voitures. »"
                },
                {
                    "type": "mc",
                    "question_nl": "Wat vindt David absoluut niet leuk?",
                    "options": [
                        "Auto's.",
                        "Motoren.",
                        "Hout.",
                        "Wandelen."
                    ],
                    "answer": "Motoren.",
                    "explanation": "« Il n'aime pas du tout les motos. »"
                },
                {
                    "type": "mc",
                    "question_nl": "Wat vindt David van kaas?",
                    "options": [
                        "Hij vindt kaas lekker.",
                        "Hij vindt kaas niet lekker.",
                        "Hij zegt niets over kaas.",
                        "Hij is bang voor kaas."
                    ],
                    "answer": "Hij vindt kaas niet lekker.",
                    "explanation": "« Il n'aime pas le fromage non plus. »"
                },
                {
                    "type": "mc",
                    "question_nl": "Wat vindt Piril leuk om te doen?",
                    "options": [
                        "In de lucht vliegen.",
                        "In de stad wandelen en naar huizen kijken.",
                        "Motor rijden.",
                        "Kaas eten."
                    ],
                    "answer": "In de stad wandelen en naar huizen kijken.",
                    "explanation": "« Piril, elle, aime marcher en ville et regarder les maisons. »"
                },
                {
                    "type": "mc",
                    "question_nl": "Wat voor soort huizen vindt Piril NIET mooi?",
                    "options": [
                        "Kleine houten huizen.",
                        "Huizen met veel beton.",
                        "Huizen aan zee.",
                        "Huizen in de bergen."
                    ],
                    "answer": "Huizen met veel beton.",
                    "explanation": "« Elle n'aime pas les maisons laides avec beaucoup de béton. »"
                },
                {
                    "type": "input",
                    "question_nl": "Schrijf in het Frans: \"Ik ben bang voor het vliegtuig.\" (j'ai ...)",
                    "answer": "j'ai peur de l'avion",
                    "explanation": "J'ai peur de l'avion."
                },
                {
                    "type": "mc",
                    "question_nl": "Wat betekent \"maison en bois\"?",
                    "options": [
                        "Houten huis.",
                        "Betonnen huis.",
                        "Groot huis.",
                        "Lelijk huis."
                    ],
                    "answer": "Houten huis.",
                    "explanation": "En bois = van hout."
                },
                {
                    "type": "input",
                    "question_nl": "Schrijf in het Frans: \"Ik hou niet van lelijke huizen.\"",
                    "answer": "je n'aime pas les maisons laides",
                    "explanation": "Je n'aime pas les maisons laides."
                },
                {
                    "type": "mc",
                    "question_nl": "In welke zin past \"dangereux\" goed?",
                    "options": [
                        "Les motos sont dangereuses.",
                        "Les motos sont fromage.",
                        "Les motos sont maisons.",
                        "Les motos sont bois."
                    ],
                    "answer": "Les motos sont dangereuses.",
                    "explanation": "Gevaarlijk = dangereux / dangereuses."
                },
                {
                    "type": "input",
                    "question_nl": "Schrijf in het Frans: \"Ik kijk vaak naar video's van auto's.\" (je regarde ...)",
                    "answer": "je regarde souvent des vidéos de voitures",
                    "explanation": "Je regarde souvent des vidéos de voitures."
                },
            ]
        },
        "write_hint": (
            "Schrijf 3–5 zinnen over jouw hobby's en dingen die je niet leuk vindt.\n"
            "- j'aime ... / je n'aime pas ...\n"
            "- j'ai peur de ...\n"
        ),
        "write_example": """J'aime les voitures, mais je n'aime pas le fromage.
Je n'aime pas les maisons laides.
J'ai peur de l'avion.""",
        "exercises": [
            {
                "type": "mc",
                "question_nl": "Wat betekent: « J'aime les voitures. »?",
                "options": [
                    "Ik hou van auto's.",
                    "Ik hou van motoren.",
                    "Ik hou van vliegtuigen.",
                    "Ik hou van huizen."
                ],
                "answer": "Ik hou van auto's.",
                "explanation": "Les voitures = auto's."
            },
            {
                "type": "input",
                "question_nl": "Schrijf in het Frans: \"Ik hou niet van motoren.\"",
                "answer": "je n'aime pas les motos",
                "explanation": "Je n'aime pas les motos."
            },
            {
                "type": "input",
                "question_nl": "Schrijf in het Frans: \"Ik vind kaas niet lekker.\"",
                "answer": "je n'aime pas le fromage",
                "explanation": "Je n'aime pas le fromage."
            },
            {
                "type": "mc",
                "question_nl": "Welke zin betekent: \"Ik ben bang om te vliegen.\"?",
                "options": [
                    "J'aime voler.",
                    "Je n'aime pas voler.",
                    "J'ai peur de l'avion.",
                    "Je n'aime pas les maisons."
                ],
                "answer": "J'ai peur de l'avion.",
                "explanation": "J'ai peur de l'avion."
            },
            {
                "type": "order",
                "instruction_nl": "Zet de delen in de goede volgorde:",
                "parts": ["je", "n'aime", "pas", "les maisons laides"],
                "correct": ["je", "n'aime", "pas", "les maisons laides"],
                "explanation": "Je n'aime pas les maisons laides."
            },
            {
                "type": "mc",
                "question_nl": "Wat betekent \"bois\"?",
                "options": [
                    "Hout.",
                    "Beton.",
                    "Staal.",
                    "Glas."
                ],
                "answer": "Hout.",
                "explanation": "Bois = hout."
            },
            {
                "type": "input",
                "question_nl": "Schrijf in het Frans: \"Ik hou van wandelen in de stad.\" (j'aime ... en ville)",
                "answer": "j'aime marcher en ville",
                "explanation": "J'aime marcher en ville."
            },
            {
                "type": "mc",
                "question_nl": "Welke combinatie klopt?",
                "options": [
                    "Je n'aime pas voitures les.",
                    "Je n'aime pas les voitures.",
                    "Je aime n' pas les voitures.",
                    "Je n'aime voitures pas."
                ],
                "answer": "Je n'aime pas les voitures.",
                "explanation": "Je n'aime pas + lidwoord + zelfstandig naamwoord."
            },
            {
                "type": "input",
                "question_nl": "Schrijf in het Frans: \"Ik hou van kleine houten huizen.\" (j'aime les petites ...)",
                "answer": "j'aime les petites maisons en bois",
                "explanation": "J'aime les petites maisons en bois."
            },
            {
                "type": "mc",
                "question_nl": "Wat betekent \"avoir peur de\"?",
                "options": [
                    "Houden van.",
                    "Bang zijn voor.",
                    "Werken met.",
                    "Praten over."
                ],
                "answer": "Bang zijn voor.",
                "explanation": "Avoir peur de = bang zijn voor."
            },
        ],
    },
]

# ---------------------------------------------------------
# Sidebar – modus kiezen
# ---------------------------------------------------------

st.sidebar.title("📘 Frans – Cargo Operations")
st.sidebar.markdown(
    "Plan: **20–30 minuten per dag**.\n\n"
    "Kies een modus om te oefenen."
)

MODES = [
    "Leercursus (hoofdstukken)",
    "Schrijven (vrije teksten)",
    "Studieplan",
]

mode = st.sidebar.radio("Modus", MODES)

# ---------------------------------------------------------
# Modus: Leercursus
# ---------------------------------------------------------

if mode == "Leercursus (hoofdstukken)":
    chapter_titles = [c["title"] for c in CHAPTERS]
    selected_title = st.selectbox("Kies een hoofdstuk:", chapter_titles)
    chapter = next(c for c in CHAPTERS if c["title"] == selected_title)

    st.title(chapter["title"])

    # Voortgang uit DB tonen
    prog = get_progress(chapter["id"])
    st.markdown(
        f"**Voortgang {st.session_state.user_id}:** "
        f"lees {prog['reading_correct']}/{prog['reading_done']}, "
        f"oefeningen {prog['ex_correct']}/{prog['ex_done']} ✅"
    )

    st.markdown(f"**Doel (NL):** {chapter['goal_nl']}")
    st.markdown("---")

    tab_theory, tab_dialogue, tab_exercises = st.tabs(
        ["Uitleg & voorbeelden", "Dialoog & lezen", "Oefeningen & schrijfopdracht"]
    )

    # ---------- Theorie ----------
    with tab_theory:
        if "intro_audio_fr" in chapter:
            if st.button(
                "▶ Luister hoofdstuk-intro (FR)",
                key=f"intro_{chapter['id']}",
            ):
                audio_data = tts_bytes(chapter["intro_audio_fr"], lang="fr")
                st.audio(audio_data, format="audio/mp3")

        st.markdown(chapter["theory"])

        st.markdown("#### Voorbeelden")
        for fr, nl in chapter["examples"]:
            cols = st.columns([3, 1])
            with cols[0]:
                st.markdown(f"**FR:** {fr}")
                if st.button(
                    "▶ Luister",
                    key=f"ex_audio_{chapter['id']}_{fr}",
                ):
                    audio_data = tts_bytes(fr, lang="fr")
                    st.audio(audio_data, format="audio/mp3")
            with cols[1]:
                st.markdown(f"*NL:* {nl}")

    # ---------- Dialoog & lezen ----------
    with tab_dialogue:
        dlg = chapter["dialogue"]
        st.markdown(f"### {dlg['title']}")
        for speaker, fr, nl in dlg["turns"]:
            st.markdown(f"**{speaker} – FR:** {fr}")
            st.markdown(f"*NL:* {nl}")
            if st.button(
                f"▶ Luister ({speaker})",
                key=f"dlg_{chapter['id']}_{speaker}_{fr}",
            ):
                audio_data = tts_bytes(fr, lang="fr")
                st.audio(audio_data, format="audio/mp3")
            st.markdown("")

        st.markdown("### Leesopdracht")
        reading = chapter["reading"]
        st.markdown("**Tekst (FR):**")
        st.markdown(reading["text_fr"])
        if st.button("▶ Luister tekst", key=f"read_{chapter['id']}"):
            audio_data = tts_bytes(reading["text_fr"], lang="fr")
            st.audio(audio_data, format="audio/mp3")

        st.markdown("#### Woordenschat (10 begrippen)")
        for fr, nl in reading["vocab"]:
            cols = st.columns([3, 1])
            with cols[0]:
                st.markdown(f"- **{fr}**")
            with cols[1]:
                st.markdown(f"*{nl}*")

        st.markdown("### Lees- en vocab-oefeningen (10)")
        for idx, q in enumerate(reading["questions"], start=1):
            st.markdown(f"#### Oefening {idx}")
            key = f"read_{chapter['id']}_{idx}"
            exercise_key = f"ch{chapter['id']}_read_q{idx}"
            logged_flag = f"{key}_logged"

            if q["type"] == "mc":
                st.write(q["question_nl"])
                choice = st.radio(
                    "Kies het beste antwoord:",
                    q["options"],
                    key=key,
                )
                if choice:
                    correct = choice == q["answer"]

                    # Alleen de eerste keer loggen / progress updaten
                    if not st.session_state.get(logged_flag):
                        update_progress(chapter["id"], "reading", correct)
                        log_exercise_answer(
                            st.session_state.user_id,
                            chapter["id"],
                            exercise_key,
                            choice,
                            correct,
                        )
                        st.session_state[logged_flag] = True

                    if correct:
                        st.success("✅ Klopt!")
                    else:
                        st.error(
                            f"❌ Niet helemaal. Juist antwoord: **{q['answer']}**."
                        )
                    if "explanation" in q:
                        with st.expander("Uitleg"):
                            st.write(q["explanation"])

            elif q["type"] == "input":
                st.write(q["question_nl"])
                ans = st.text_input(
                    "Jouw antwoord (Frans):",
                    key=key,
                )
                if ans:
                    correct = normalize_answer(ans) == normalize_answer(q["answer"])

                    if not st.session_state.get(logged_flag):
                        update_progress(chapter["id"], "reading", correct)
                        log_exercise_answer(
                            st.session_state.user_id,
                            chapter["id"],
                            exercise_key,
                            ans,
                            correct,
                        )
                        st.session_state[logged_flag] = True

                    if correct:
                        st.success("✅ Klopt!")
                    else:
                        st.error(
                            "❌ Niet helemaal. Verwacht (kern): "
                            f"**{q['answer']}**."
                        )
                    if "explanation" in q:
                        with st.expander("Uitleg"):
                            st.write(q["explanation"])

    # ---------- Oefeningen & schrijfopdracht ----------
    with tab_exercises:
        st.markdown("### Grammatica- en zinnen-oefeningen (min. 10)")
        for idx, ex in enumerate(chapter["exercises"], start=1):
            st.markdown(f"#### Oefening {idx}")
            key = f"ch{chapter['id']}_ex{idx}"
            exercise_key = f"ch{chapter['id']}_ex{idx}"
            logged_flag = f"{key}_logged"

            if ex["type"] == "mc":
                st.write(ex["question_nl"])
                choice = st.radio(
                    "Kies het beste antwoord:",
                    ex["options"],
                    key=key,
                )
                if choice:
                    correct = choice == ex["answer"]

                    if not st.session_state.get(logged_flag):
                        update_progress(chapter["id"], "ex", correct)
                        log_exercise_answer(
                            st.session_state.user_id,
                            chapter["id"],
                            exercise_key,
                            choice,
                            correct,
                        )
                        st.session_state[logged_flag] = True

                    if correct:
                        st.success("✅ Klopt!")
                    else:
                        st.error(
                            f"❌ Niet helemaal. Juist antwoord: **{ex['answer']}**."
                        )
                    if "explanation" in ex:
                        with st.expander("Uitleg"):
                            st.write(ex["explanation"])

            elif ex["type"] == "input":
                st.write(ex["question_nl"])
                user = st.text_input("Jouw antwoord (Frans):", key=key)
                if user:
                    correct = normalize_answer(user) == normalize_answer(
                        ex["answer"]
                    )

                    if not st.session_state.get(logged_flag):
                        update_progress(chapter["id"], "ex", correct)
                        log_exercise_answer(
                            st.session_state.user_id,
                            chapter["id"],
                            exercise_key,
                            user,
                            correct,
                        )
                        st.session_state[logged_flag] = True

                    if correct:
                        st.success("✅ Klopt!")
                    else:
                        st.error(
                            "❌ Niet helemaal. Verwacht (kern): "
                            f"**{ex['answer']}**."
                        )
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
                    key=key,
                )
                if user_order and len(user_order) == len(parts):
                    user_seq = [parts[i] for i in user_order]
                    correct = user_seq == ex["correct"]

                    if not st.session_state.get(logged_flag):
                        update_progress(chapter["id"], "ex", correct)
                        log_exercise_answer(
                            st.session_state.user_id,
                            chapter["id"],
                            exercise_key,
                            " ".join(user_seq),
                            correct,
                        )
                        st.session_state[logged_flag] = True

                    if correct:
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

        st.markdown("---")
        st.markdown("### Schrijfopdracht bij dit hoofdstuk")
        st.markdown(chapter["write_hint"])

        text_key = f"write_{chapter['id']}"

        # Bestaande tekst uit DB ophalen en als default invullen
        existing_text = load_writing_answer(
            st.session_state.user_id, chapter["id"]
        )

        tekst = st.text_area(
            "Jouw tekst (Frans):",
            height=220,
            key=text_key,
            value=existing_text,
        )

        if st.button("Analyseer tekst", key=f"analyse_{chapter['id']}"):
            if not tekst.strip():
                st.warning("Schrijf eerst iets in het tekstvak.")
            else:
                # Tekst opslaan in DB
                save_writing_answer(
                    st.session_state.user_id, chapter["id"], tekst
                )

                lower = tekst.lower()
                hints: list[str] = []

                if chapter["id"] == 1:
                    if "je m'appelle" not in lower:
                        hints.append("Probeer een zin met **je m'appelle ...**.")
                    if "aujourd'hui" not in lower:
                        hints.append(
                            "Gebruik **aujourd'hui, c'est mon premier jour de travail**."
                        )
                elif chapter["id"] == 2:
                    if "je suis" not in lower:
                        hints.append(
                            "Gebruik **je suis ...** om je functie te noemen."
                        )
                    if "je travaille" not in lower:
                        hints.append(
                            "Gebruik **je travaille ...** om te zeggen waar je werkt."
                        )
                elif chapter["id"] == 3:
                    if "ça va" not in lower and "je suis" not in lower:
                        hints.append(
                            "Gebruik **ça va ...** of **je suis ...** om te zeggen hoe het gaat."
                        )
                elif chapter["id"] == 4:
                    if "beaucoup de travail" not in lower and "charge de travail" not in lower:
                        hints.append(
                            "Noem je werkdruk met **beaucoup de travail** of **charge de travail**."
                        )
                elif chapter["id"] == 5:
                    if "l'année prochaine" not in lower and "plus tard" not in lower:
                        hints.append(
                            "Gebruik **l'année prochaine** of **plus tard** voor toekomst."
                        )
                elif chapter["id"] == 6:
                    if "j'aime" not in lower and "je n'aime pas" not in lower:
                        hints.append(
                            "Gebruik **j'aime ...** en **je n'aime pas ...** voor voorkeuren."
                        )

                if hints:
                    st.error("Een paar verbeterpunten:")
                    for h in hints:
                        st.markdown(f"- {h}")
                else:
                    st.success(
                        "Mooi! Je gebruikt de belangrijkste structuren voor dit hoofdstuk."
                    )

        st.markdown("#### Voorbeeldtekst")
        st.code(chapter["write_example"], language="markdown")

# ---------------------------------------------------------
# Modus: Schrijven (vrije teksten)
# ---------------------------------------------------------

elif mode == "Schrijven (vrije teksten)":
    st.title("Schrijven – vrije teksten over je werk")

    st.markdown(
        """
Gebruik dit scherm om langere teksten te schrijven, bijvoorbeeld:

- een korte mail aan een Franse collega  
- een beschrijving van je werkdag  
- een eenvoudige uitleg van een incident  
        """
    )

    tekst = st.text_area("Jouw tekst (Frans):", height=260)

    if st.button("Eenvoudige analyse"):
        if not tekst.strip():
            st.warning("Schrijf eerst iets in het tekstvak.")
        else:
            lower = tekst.lower()
            hints: list[str] = []

            if "je m'appelle" not in lower and "je suis" not in lower:
                hints.append(
                    "Noem jezelf met **je m'appelle ...** of **je suis ...**."
                )
            if "je travaille" not in lower:
                hints.append("Vertel waar je werkt met **je travaille ...**.")
            if (
                "cargo" not in lower
                and "terminal" not in lower
                and "navire" not in lower
            ):
                hints.append(
                    "Probeer woorden als **cargo / terminal / navire** toe te voegen."
                )
            if "aujourd'hui" not in lower and "demain" not in lower:
                hints.append(
                    "Noem een tijdsaanduiding zoals **aujourd'hui / demain**."
                )

            if hints:
                st.error("Suggesties voor verbetering:")
                for h in hints:
                    st.markdown(f"- {h}")
            else:
                st.success(
                    "Je tekst bevat al veel nuttige elementen voor jouw doel."
                )

# ---------------------------------------------------------
# Modus: Studieplan
# ---------------------------------------------------------

elif mode == "Studieplan":
    st.title("Studieplan – 20–30 minuten per dag")

    st.markdown(
        """
### Aanpak volgens de 20-uur-methode

- **Deelvaardigheden**: kennismaking, werk beschrijven, smalltalk, werkdruk, plannen, hobby's.  
- **Leer genoeg om jezelf te corrigeren**: gebruik uitleg, voorbeelden, lees- en luisterteksten.  
- **Verwijder drempels**: open direct de app, zet notificaties uit, vast moment per dag.  
- **20 uur gefocust oefenen**: 20–30 minuten per dag, ~4 weken.

### Voorstel per week

**Week 1**  
- Dag 1–2: Hoofdstuk 1 (kennismaking)  
- Dag 3–4: Hoofdstuk 2 (over jouw werk)  
- Dag 5: Herhalen + schrijfopdracht  

**Week 2**  
- Dag 1–2: Hoofdstuk 3 (hoe gaat het in Stavanger)  
- Dag 3–4: Hoofdstuk 4 (werkdruk en reizen)  
- Dag 5: Lees- en vocab-oefeningen  

**Week 3**  
- Dag 1–2: Hoofdstuk 5 (toekomstplannen)  
- Dag 3–4: Hoofdstuk 6 (hobby's en voorkeuren)  
- Dag 5: Schrijven-modus (vrije tekst)  

**Week 4 en verder**  
- Herhaal hoofdstukken waar je fouten maakt.  
- Mix elke sessie:  
  - 10 min uitleg + dialoog/leesopdracht  
  - 10–20 min oefeningen + schrijfopdracht  

Na ~20 uur ben je klaar voor een basiswerkgesprek met een Franse collega:
jezelf voorstellen, over werk, weer, drukte, plannen en hobby's praten.
        """
    )
    st.caption(
        "Gebruik een koptelefoon en spreek zinnen hardop na voor maximaal effect."
    )
