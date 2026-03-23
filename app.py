import streamlit as st
from gtts import gTTS
import io

# ---------------------------------------------------------
# Basisconfiguratie
# ---------------------------------------------------------

st.set_page_config(
    page_title="Frans voor Cargo Operations",
    page_icon="🇫🇷",
    layout="centered"
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
# Cursusdata per hoofdstuk
# ---------------------------------------------------------

CHAPTERS = [
    {
        "id": 1,
        "title": "1. Kennismaking en hallo zeggen",
        "goal_nl": "Je kunt jezelf kort voorstellen en iemand begroeten.",
        "intro_audio_fr": "Bonjour, je m'appelle Toon. Dans ce chapitre, tu apprends à te présenter et à dire bonjour.",
        "theory": """
### Doel

Je leert hoe je in het Frans:

- hallo zegt  
- jezelf voorstelt (naam, rol, bedrijf)  
- kort uitlegt wat je doet

### Kernzinnen

- Bonjour → Goedendag / hallo  
- Salut → Hoi (informeel)  
- Je m'appelle Toon. → Ik heet Toon.  
- Je suis opérateur cargo. → Ik ben cargobediener.  
- Je travaille chez Equinor. → Ik werk bij Equinor.  
""",
        "examples": [
            ("Bonjour, je m'appelle Toon.", "Goedendag, ik heet Toon."),
            ("Je suis opérateur cargo.", "Ik ben cargobediener."),
            ("Je travaille chez Equinor.", "Ik werk bij Equinor."),
        ],
        "dialogue": {
            "title": "Dialoog: eerste kennismaking",
            "turns": [
                ("Piril", "Bonjour, je m'appelle Piril. Je travaille chez Equinor.", "Hallo, ik heet Piril. Ik werk bij Equinor."),
                ("David", "Enchanté, je suis David. Je suis opérateur cargo.", "Aangenaam, ik ben David. Ik ben cargobediener."),
                ("Piril", "Je travaille au terminal LPG à Stavanger.", "Ik werk op de LPG-terminal in Stavanger."),
            ]
        },
        "reading": {
            "text_fr": "Bonjour, je m'appelle Toon. Je suis responsable des opérations cargo chez Equinor. "
                        "Je travaille au terminal LPG à Stavanger.",
            "question_nl": "Wat doet Toon bij Equinor?",
            "options": [
                "Hij is kapitein.",
                "Hij is verantwoordelijk voor de cargo-operaties.",
                "Hij is vrachtwagenchauffeur."
            ],
            "correct": "Hij is verantwoordelijk voor de cargo-operaties."
        },
        "write_hint": (
            "Schrijf 3–5 zinnen waarin je jezelf voorstelt.\n"
            "- je m'appelle ...\n"
            "- je suis ... (functie)\n"
            "- je travaille ... (bedrijf/plaats)\n"
        ),
        "write_example": """Bonjour, je m'appelle Toon.
Je suis opérateur cargo.
Je travaille chez Equinor, au terminal LPG à Stavanger.""",
        "exercises": [
            # 1
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
            # 2
            {
                "type": "input",
                "question_nl": "Schrijf in het Frans: \"Ik werk bij Equinor.\"",
                "answer": "je travaille chez equinor",
                "explanation": "Je travaille chez Equinor."
            },
            # 3
            {
                "type": "input",
                "question_nl": "Schrijf in het Frans: \"Ik heet Toon.\"",
                "answer": "je m'appelle toon",
                "explanation": "Je m'appelle Toon."
            },
            # 4
            {
                "type": "mc",
                "question_nl": "Welke Franse zin past bij: \"Ik ben cargobediener.\"?",
                "options": [
                    "Je travaille cargobediener.",
                    "Je suis opérateur cargo.",
                    "Je cargo suis opérateur.",
                    "Je suis Equinor.",
                    "Je m'appelle opérateur cargo.",
                    "Je travaille cargo."
                ],
                "answer": "Je suis opérateur cargo.",
                "explanation": "Je suis + functie: je suis opérateur cargo."
            },
            # 5
            {
                "type": "order",
                "instruction_nl": "Zet de delen in de goede volgorde:",
                "parts": ["je", "m'appelle", "Toon"],
                "correct": ["je", "m'appelle", "Toon"],
                "explanation": "Franse volgorde: je m'appelle Toon."
            },
            # 6
            {
                "type": "order",
                "instruction_nl": "Zet de delen in de goede volgorde:",
                "parts": ["Equinor", "je", "travaille", "chez"],
                "correct": ["je", "travaille", "chez", "Equinor"],
                "explanation": "Je travaille chez Equinor."
            },
            # 7
            {
                "type": "mc",
                "question_nl": "Welke begroeting is informeel?",
                "options": ["Bonjour", "Salut", "Bonsoir", "Au revoir", "Merci", "Pardon"],
                "answer": "Salut",
                "explanation": "Salut gebruik je informeel, bonjour is neutraler."
            },
            # 8
            {
                "type": "input",
                "question_nl": "Vul aan: \"Bonjour, je ____ Piril.\" (ik ben Piril)",
                "answer": "suis",
                "explanation": "Je suis Piril."
            },
            # 9
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
                "explanation": "Bij eerste begroeting praat je meestal niet direct over werkdruk."
            },
            # 10
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
        "goal_nl": "Je kunt in het Frans heel kort uitleggen wat je werk is.",
        "intro_audio_fr": "Dans ce chapitre, tu apprends à parler de ton travail comme opérateur cargo chez Equinor.",
        "theory": """
### Objectif (FR)

Dans ce chapitre, l'interface est **en français**.  
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
        "dialogue": {
            "title": "Dialogue: parler du travail",
            "turns": [
                ("Piril", "Je suis responsable des opérations cargo.", "Ik ben verantwoordelijk voor de cargo-operaties."),
                ("David", "Je suis opérateur cargo au terminal LPG.", "Ik ben cargobediener op de LPG-terminal."),
                ("Piril", "Je travaille surtout de jour, et toi ?", "Ik werk vooral overdag, en jij?"),
                ("David", "Je travaille de nuit cette semaine.", "Ik werk 's nachts deze week."),
            ]
        },
        "reading": {
            "text_fr": "Je suis David. Je travaille au terminal LPG à Stavanger. "
                        "Je suis opérateur cargo chez Equinor.",
            "question_nl": "Wat doet David?",
            "options": [
                "Hij is kapitein op een schip.",
                "Hij is operator op de LPG-terminal.",
                "Hij is planner in het kantoor."
            ],
            "correct": "Hij is operator op de LPG-terminal."
        },
        "write_hint": (
            "Schrijf 3–5 zinnen over je werk.\n"
            "- je suis ... (functie)\n"
            "- je travaille ... (plaats/bedrijf)\n"
            "- je travaille de jour / de nuit\n"
        ),
        "write_example": """Je suis opérateur cargo.
Je suis responsable des opérations cargo.
Je travaille au terminal LPG à Stavanger.
Je travaille surtout de jour.""",
        "exercises": [
            # 1
            {
                "type": "mc",
                "question_nl": "Wat betekent: « Je suis responsable des opérations cargo. »?",
                "options": [
                    "Ik ben verantwoordelijk voor de cargo-operaties.",
                    "Ik werk soms met cargo.",
                    "Ik ben vrachtwagenchauffeur.",
                    "Ik controleer het weer.",
                    "Ik ben kapitein op een schip.",
                    "Ik ben planner in Oslo."
                ],
                "answer": "Ik ben verantwoordelijk voor de cargo-operaties.",
                "explanation": "Responsable des opérations cargo = verantwoordelijk voor de cargo-operaties."
            },
            # 2
            {
                "type": "input",
                "question_nl": "Schrijf in het Frans: \"Ik ben operator cargo.\"",
                "answer": "je suis opérateur cargo",
                "explanation": "Je suis opérateur cargo."
            },
            # 3
            {
                "type": "input",
                "question_nl": "Schrijf in het Frans: \"Ik werk op de LPG-terminal.\"",
                "answer": "je travaille au terminal lpg",
                "explanation": "Je travaille au terminal LPG."
            },
            # 4
            {
                "type": "mc",
                "question_nl": "Welke zin past bij \"Ik werk 's nachts\"?",
                "options": [
                    "Je travaille de jour.",
                    "Je travaille de nuit.",
                    "Je travaille toujours le week-end.",
                    "Je suis de nuit Equinor.",
                    "Je travaille chez nuit.",
                    "Je vais de nuit."
                ],
                "answer": "Je travaille de nuit.",
                "explanation": "De nuit = 's nachts."
            },
            # 5
            {
                "type": "order",
                "instruction_nl": "Zet de delen in de goede volgorde:",
                "parts": ["je", "suis", "responsable", "des", "opérations", "cargo"],
                "correct": ["je", "suis", "responsable", "des", "opérations", "cargo"],
                "explanation": "Je suis responsable des opérations cargo."
            },
            # 6
            {
                "type": "order",
                "instruction_nl": "Zet de delen in de goede volgorde:",
                "parts": ["Equinor", "je", "travaille", "chez"],
                "correct": ["je", "travaille", "chez", "Equinor"],
                "explanation": "Je travaille chez Equinor."
            },
            # 7
            {
                "type": "mc",
                "question_nl": "Welke zin gebruik je om te zeggen waar je werkt?",
                "options": [
                    "Je suis Equinor.",
                    "Je travaille chez Equinor.",
                    "Je vais Equinor.",
                    "Je cargo Equinor.",
                    "Je nuit Equinor.",
                    "Je fais Equinor."
                ],
                "answer": "Je travaille chez Equinor.",
                "explanation": "Travailler chez + bedrijf."
            },
            # 8
            {
                "type": "input",
                "question_nl": "Vul aan: \"Je ____ surtout de jour.\" (ik werk vooral overdag)",
                "answer": "travaille",
                "explanation": "Je travaille surtout de jour."
            },
            # 9
            {
                "type": "mc",
                "question_nl": "Wat betekent: « Je travaille surtout de jour. »?",
                "options": [
                    "Ik werk alleen 's nachts.",
                    "Ik werk vooral overdag.",
                    "Ik werk nooit overdag.",
                    "Ik werk soms in het weekend.",
                    "Ik werk alleen op kantoor.",
                    "Ik werk vooral op zee."
                ],
                "answer": "Ik werk vooral overdag.",
                "explanation": "Surtout de jour = vooral overdag."
            },
            # 10
            {
                "type": "input",
                "question_nl": "Schrijf in het Frans: \"Ik ben operator bij Equinor.\"",
                "answer": "je suis opérateur chez equinor",
                "explanation": "Je suis opérateur chez Equinor."
            },
        ],
    },
    {
        "id": 3,
        "title": "3. Smalltalk: hoe gaat het en het weer",
        "goal_nl": "Je kunt vragen hoe het gaat en over het weer praten.",
        "intro_audio_fr": "Ici, tu apprends à demander comment ça va et à parler du temps.",
        "theory": """
### Doel

Je leert:

- vragen hoe het gaat  
- antwoorden hoe het gaat  
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
        "dialogue": {
            "title": "Dialoog: weer en hoe het gaat",
            "turns": [
                ("Piril", "Salut David, ça va ?", "Hoi David, alles goed?"),
                ("David", "Oui, ça va bien, merci. Il fait très froid aujourd'hui.", "Ja, gaat goed, dank je. Het is heel koud vandaag."),
                ("Piril", "Oui, il fait froid mais il fait beau.", "Ja, het is koud maar het is mooi weer."),
            ]
        },
        "reading": {
            "text_fr": "Salut, ça va ? Il fait très froid aujourd'hui, mais le temps est stable. "
                        "C'est bien pour les opérations.",
            "question_nl": "Wat is goed voor de operaties?",
            "options": [
                "Dat het heel koud is.",
                "Dat het weer stabiel is.",
                "Dat het regent."
            ],
            "correct": "Dat het weer stabiel is."
        },
        "write_hint": (
            "Schrijf 3–5 zinnen smalltalk.\n"
            "- salut / bonjour + ça va ?\n"
            "- ça va bien / comme ci, comme ça\n"
            "- il fait froid / chaud / beau\n"
        ),
        "write_example": """Salut, ça va ?
Ça va bien, merci.
Il fait froid aujourd'hui, mais il fait beau.""",
        "exercises": [
            # 1
            {
                "type": "mc",
                "question_nl": "Wat betekent: « Ça va ? »?",
                "options": [
                    "Gaat het regenen?",
                    "Hoe gaat het?",
                    "Waar ga je naartoe?",
                    "Hoe heet je?",
                    "Waar werk je?",
                    "Is het druk?"
                ],
                "answer": "Hoe gaat het?",
                "explanation": "Ça va ? = hoe gaat het?"
            },
            # 2
            {
                "type": "input",
                "question_nl": "Schrijf in het Frans: \"Het gaat goed, dank je.\"",
                "answer": "ça va bien, merci",
                "explanation": "Ça va bien, merci."
            },
            # 3
            {
                "type": "mc",
                "question_nl": "Welke zin betekent: \"Het is mooi weer.\"?",
                "options": [
                    "Il est beau.",
                    "Il fait beau.",
                    "Il va beau.",
                    "Il fait très chaud.",
                    "Il est froid.",
                    "Il est bien."
                ],
                "answer": "Il fait beau.",
                "explanation": "Il fait beau = het is mooi weer."
            },
            # 4
            {
                "type": "input",
                "question_nl": "Schrijf in het Frans: \"Het is warm.\"",
                "answer": "il fait chaud",
                "explanation": "Il fait chaud."
            },
            # 5
            {
                "type": "order",
                "instruction_nl": "Zet de delen in de goede volgorde:",
                "parts": ["froid", "il", "fait"],
                "correct": ["il", "fait", "froid"],
                "explanation": "Il fait froid."
            },
            # 6
            {
                "type": "mc",
                "question_nl": "Wat betekent: « Comme ci, comme ça. »?",
                "options": [
                    "Heel goed.",
                    "Heel slecht.",
                    "Gaat wel.",
                    "Misschien.",
                    "Ik ben moe.",
                    "Ik werk vandaag."
                ],
                "answer": "Gaat wel.",
                "explanation": "Comme ci, comme ça = gaat wel."
            },
            # 7
            {
                "type": "input",
                "question_nl": "Vul aan: \"Il fait très ____ aujourd'hui.\" (koud)",
                "answer": "froid",
                "explanation": "Il fait très froid aujourd'hui."
            },
            # 8
            {
                "type": "mc",
                "question_nl": "Welke zin past NIET bij smalltalk over het weer?",
                "options": [
                    "Il fait froid aujourd'hui.",
                    "Il fait beau.",
                    "Il fait chaud.",
                    "Je suis un navire.",
                    "Il pleut beaucoup.",
                    "Il fait très gris."
                ],
                "answer": "Je suis un navire.",
                "explanation": "Je suis un navire = ik ben een schip, dat zeg je niet over het weer."
            },
            # 9
            {
                "type": "input",
                "question_nl": "Schrijf in het Frans: \"Het is heel koud vandaag.\"",
                "answer": "il fait très froid aujourd'hui",
                "explanation": "Il fait très froid aujourd'hui."
            },
            # 10
            {
                "type": "order",
                "instruction_nl": "Zet de delen in de goede volgorde:",
                "parts": ["ça", "?", "va"],
                "correct": ["ça", "va", "?"],
                "explanation": "Ça va ?"
            },
        ],
    },
    {
        "id": 4,
        "title": "4. Werkdruk en planning",
        "goal_nl": "Je kunt zeggen of het druk of rustig is en kort je planning beschrijven.",
        "intro_audio_fr": "Dans ce chapitre, tu apprends à dire si la journée est calme ou très chargée, et à parler de la planification.",
        "theory": """
### Doel

Je leert:

- zeggen dat het druk of rustig is  
- kort je planning beschrijven

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
        "dialogue": {
            "title": "Dialoog: werkdruk bespreken",
            "turns": [
                ("Piril", "Aujourd'hui, c'est très chargé pour moi.", "Vandaag is het erg druk voor mij."),
                ("David", "Ah bon ? Pour moi, c'est plutôt calme.", "Oh ja? Voor mij is het eerder rustig."),
                ("Piril", "Nous avons deux navires et beaucoup de camions.", "We hebben twee schepen en veel trucks."),
            ]
        },
        "reading": {
            "text_fr": "Aujourd'hui, c'est très chargé. Nous avons trois navires et beaucoup de camions. "
                        "Il y a un petit problème avec un navire.",
            "question_nl": "Wat is er vandaag aan de hand?",
            "options": [
                "Het is rustig, er zijn geen schepen.",
                "Het is druk en er is een klein probleem met een schip.",
                "Het is rustig maar er zijn veel trucks."
            ],
            "correct": "Het is druk en er is een klein probleem met een schip."
        },
        "write_hint": (
            "Schrijf 3–5 zinnen over je werkdruk.\n"
            "- aujourd'hui, c'est calme / très chargé\n"
            "- nous avons ... navires / camions\n"
            "- il y a un petit problème (optioneel)\n"
        ),
        "write_example": """Aujourd'hui, c'est très chargé.
Nous avons trois navires et beaucoup de camions.
Il y a un petit problème avec un navire, mais c'est sous contrôle.""",
        "exercises": [
            # 1
            {
                "type": "mc",
                "question_nl": "Wat betekent: « Aujourd'hui, c'est très chargé. »?",
                "options": [
                    "Vandaag is het erg druk.",
                    "Vandaag is het rustig.",
                    "Vandaag is het mooi weer.",
                    "Vandaag is er geen werk.",
                    "Vandaag is het erg koud.",
                    "Vandaag is het gevaarlijk."
                ],
                "answer": "Vandaag is het erg druk.",
                "explanation": "Très chargé = erg druk."
            },
            # 2
            {
                "type": "input",
                "question_nl": "Schrijf in het Frans: \"Vandaag is het rustig.\"",
                "answer": "aujourd'hui, c'est calme",
                "explanation": "Aujourd'hui, c'est calme."
            },
            # 3
            {
                "type": "mc",
                "question_nl": "Welke zin betekent: \"We hebben drie schepen.\"?",
                "options": [
                    "Nous sommes trois navires.",
                    "Nous avons trois navires.",
                    "Ils ont trois navires.",
                    "Nous faisons trois navires.",
                    "Nous navires avons trois.",
                    "Nous avons trois camions."
                ],
                "answer": "Nous avons trois navires.",
                "explanation": "Nous avons trois navires."
            },
            # 4
            {
                "type": "input",
                "question_nl": "Schrijf in het Frans: \"We hebben veel trucks.\"",
                "answer": "nous avons beaucoup de camions",
                "explanation": "Nous avons beaucoup de camions."
            },
            # 5
            {
                "type": "order",
                "instruction_nl": "Zet de delen in de goede volgorde:",
                "parts": ["un", "il", "y", "a", "petit", "problème"],
                "correct": ["il", "y", "a", "un", "petit", "problème"],
                "explanation": "Il y a un petit problème."
            },
            # 6
            {
                "type": "mc",
                "question_nl": "Wat betekent: « Il y a un petit problème. »?",
                "options": [
                    "Er is geen probleem.",
                    "Er is een klein probleem.",
                    "Er is een groot probleem.",
                    "Er is rustig werk.",
                    "Er zijn geen schepen.",
                    "Er zijn drie schepen."
                ],
                "answer": "Er is een klein probleem.",
                "explanation": "Un petit problème = een klein probleem."
            },
            # 7
            {
                "type": "input",
                "question_nl": "Vul aan: \"Nous ____ deux navires aujourd'hui.\" (we hebben)",
                "answer": "avons",
                "explanation": "Nous avons deux navires aujourd'hui."
            },
            # 8
            {
                "type": "mc",
                "question_nl": "Welke zin gebruik je voor \"Vandaag is rustig voor mij.\"?",
                "options": [
                    "Aujourd'hui, c'est très chargé pour moi.",
                    "Aujourd'hui, c'est calme pour moi.",
                    "Aujourd'hui, je suis navire.",
                    "Aujourd'hui, je suis froid.",
                    "Aujourd'hui, c'est camion.",
                    "Aujourd'hui, je suis petit problème."
                ],
                "answer": "Aujourd'hui, c'est calme pour moi.",
                "explanation": "Calme = rustig."
            },
            # 9
            {
                "type": "input",
                "question_nl": "Schrijf in het Frans: \"Er is een klein probleem met een schip.\"",
                "answer": "il y a un petit problème avec un navire",
                "explanation": "Il y a un petit problème avec un navire."
            },
            # 10
            {
                "type": "order",
                "instruction_nl": "Zet de delen in de goede volgorde:",
                "parts": ["c'est", "aujourd'hui,", "chargé", "très"],
                "correct": ["aujourd'hui,", "c'est", "très", "chargé"],
                "explanation": "Aujourd'hui, c'est très chargé."
            },
        ],
    },
    {
        "id": 5,
        "title": "5. Zinsbouw en voornaamwoorden",
        "goal_nl": "Je herkent en gebruikt S–V–O en persoonlijke voornaamwoorden.",
        "intro_audio_fr": "Ici, tu révises les pronoms personnels et l'ordre sujet-verbe-objet.",
        "theory": """
### Doel

Je leert:

- de basis-zinsvolgorde (S–V–O)  
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
        "dialogue": {
            "title": "Dialoog: wie doet wat?",
            "turns": [
                ("Piril", "Nous travaillons au terminal LPG.", "Wij werken op de LPG-terminal."),
                ("David", "Ils vérifient la cargaison.", "Zij controleren de lading."),
                ("Piril", "Je parle avec le capitaine.", "Ik spreek met de kapitein."),
            ]
        },
        "reading": {
            "text_fr": "Nous travaillons au terminal LPG. Ils vérifient la cargaison. "
                        "Je parle avec le capitaine.",
            "question_nl": "Wat doet \"je\" in deze tekst?",
            "options": [
                "Hij/zij controleert de lading.",
                "Hij/zij spreekt met de kapitein.",
                "Hij/zij werkt op kantoor in Oslo."
            ],
            "correct": "Hij/zij spreekt met de kapitein."
        },
        "write_hint": (
            "Schrijf 3–5 zinnen met verschillende voornaamwoorden.\n"
            "- je / nous / ils / elles\n"
            "- gebruik duidelijke werkwoorden (travailler, vérifier, parler)\n"
        ),
        "write_example": """Je travaille au terminal LPG.
Nous vérifions la cargaison.
Ils parlent avec le capitaine.""",
        "exercises": [
            # 1
            {
                "type": "mc",
                "question_nl": "Welk persoonlijk voornaamwoord hoort bij \"wij\"?",
                "options": ["je", "tu", "nous", "ils", "elles", "vous"],
                "answer": "nous",
                "explanation": "Nous = wij."
            },
            # 2
            {
                "type": "mc",
                "question_nl": "Welke zin heeft de volgorde S–V–O?",
                "options": [
                    "Parle je français.",
                    "Je parle français.",
                    "Français je parle.",
                    "Parle français je.",
                    "Français parle je.",
                    "Je français parle."
                ],
                "answer": "Je parle français.",
                "explanation": "S–V–O: Je (S) parle (V) français (O)."
            },
            # 3
            {
                "type": "order",
                "instruction_nl": "Zet de delen in de goede volgorde:",
                "parts": ["nous", "travaillons", "au terminal"],
                "correct": ["nous", "travaillons", "au terminal"],
                "explanation": "Nous travaillons au terminal."
            },
            # 4
            {
                "type": "input",
                "question_nl": "Schrijf in het Frans: \"Zij werken op de terminal.\" (mannelijk/meervoud)",
                "answer": "ils travaillent au terminal",
                "explanation": "Ils travaillent au terminal."
            },
            # 5
            {
                "type": "mc",
                "question_nl": "Welke zin gebruikt \"vous\" als onderwerp?",
                "options": [
                    "Vous travaillez au terminal.",
                    "Ils travaillent au terminal.",
                    "Je travaille au terminal.",
                    "Nous travaillons au terminal.",
                    "Tu travailles au terminal.",
                    "Elle travaille au terminal."
                ],
                "answer": "Vous travaillez au terminal.",
                "explanation": "Vous travaillez ... = jullie/u werkt ..."
            },
            # 6
            {
                "type": "input",
                "question_nl": "Vul aan: \"Ils ____ la cargaison.\" (controleren)",
                "answer": "vérifient",
                "explanation": "Ils vérifient la cargaison."
            },
            # 7
            {
                "type": "order",
                "instruction_nl": "Zet de delen in de goede volgorde:",
                "parts": ["parlent", "ils", "avec le capitaine"],
                "correct": ["ils", "parlent", "avec le capitaine"],
                "explanation": "Ils parlent avec le capitaine."
            },
            # 8
            {
                "type": "mc",
                "question_nl": "Welke combinatie is correct?",
                "options": [
                    "Je travaillent",
                    "Tu travaille",
                    "Nous travaillons",
                    "Ils travaillez",
                    "Vous travailles",
                    "Elles travaille"
                ],
                "answer": "Nous travaillons",
                "explanation": "Nous travaillons is de juiste combinatie."
            },
            # 9
            {
                "type": "input",
                "question_nl": "Schrijf in het Frans: \"Ik spreek met de kapitein.\"",
                "answer": "je parle avec le capitaine",
                "explanation": "Je parle avec le capitaine."
            },
            # 10
            {
                "type": "mc",
                "question_nl": "Wat is het onderwerp in: « Nous vérifions la cargaison. »?",
                "options": ["Nous", "vérifions", "la cargaison", "Nous vérifions", "vérifions la cargaison", "la"],
                "answer": "Nous",
                "explanation": "Nous is het onderwerp (wij)."
            },
        ],
    },
    {
        "id": 6,
        "title": "6. Werkwoorden: présent en ontkenning",
        "goal_nl": "Je maakt eenvoudige zinnen in de tegenwoordige tijd en ontkent ze.",
        "intro_audio_fr": "Dans ce chapitre, tu utilises je suis, j'ai, je travaille et la négation ne ... pas.",
        "theory": """
### Doel

Je leert:

- de tegenwoordige tijd van een paar kernwerkwoorden  
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
        "dialogue": {
            "title": "Dialoog: iets ontkennen",
            "turns": [
                ("Piril", "Je travaille aujourd'hui, et toi ?", "Ik werk vandaag, en jij?"),
                ("David", "Je ne travaille pas aujourd'hui. Je suis en repos.", "Ik werk vandaag niet. Ik heb vrij."),
                ("Piril", "D'accord, j'ai beaucoup de travail.", "Oké, ik heb veel werk."),
            ]
        },
        "reading": {
            "text_fr": "Je suis opérateur cargo. Aujourd'hui, je ne travaille pas. "
                        "Demain, je travaille au terminal LPG.",
            "question_nl": "Werkt de spreker vandaag?",
            "options": [
                "Ja, hij werkt vandaag.",
                "Nee, hij werkt vandaag niet.",
                "Hij werkt alleen 's nachts."
            ],
            "correct": "Nee, hij werkt vandaag niet."
        },
        "write_hint": (
            "Schrijf 3–5 zinnen met ontkenning.\n"
            "- je ne travaille pas aujourd'hui\n"
            "- je n'ai pas de problème\n"
        ),
        "write_example": """Je suis opérateur cargo.
Aujourd'hui, je ne travaille pas.
Demain, je travaille au terminal LPG.
Je n'ai pas de problème avec la cargaison.""",
        "exercises": [
            # 1
            {
                "type": "mc",
                "question_nl": "Wat betekent: « Je ne travaille pas aujourd'hui. »?",
                "options": [
                    "Ik werk vandaag.",
                    "Ik werk vandaag niet.",
                    "Ik werk altijd vandaag.",
                    "Ik heb vandaag veel werk.",
                    "Ik ben vandaag vrij druk.",
                    "Ik ben vandaag erg moe."
                ],
                "answer": "Ik werk vandaag niet.",
                "explanation": "Ne ... pas = ontkenning."
            },
            # 2
            {
                "type": "input",
                "question_nl": "Schrijf in het Frans: \"Ik ben operator cargo.\"",
                "answer": "je suis opérateur cargo",
                "explanation": "Je suis opérateur cargo."
            },
            # 3
            {
                "type": "input",
                "question_nl": "Maak ontkennend: \"Je travaille aujourd'hui.\" (zonder hoofdletters/punten)",
                "answer": "je ne travaille pas aujourd'hui",
                "explanation": "Je ne travaille pas aujourd'hui."
            },
            # 4
            {
                "type": "mc",
                "question_nl": "Welke zin betekent: \"Ik heb geen probleem.\"?",
                "options": [
                    "J'ai un problème.",
                    "Je n'ai pas de problème.",
                    "Je ne suis pas problème.",
                    "Je ne travaille pas de problème.",
                    "Je ne problème pas.",
                    "Je n'ai problème."
                ],
                "answer": "Je n'ai pas de problème.",
                "explanation": "Je n'ai pas de problème = ik heb geen probleem."
            },
            # 5
            {
                "type": "order",
                "instruction_nl": "Zet de delen in de goede volgorde:",
                "parts": ["je", "ne", "parle", "pas", "français"],
                "correct": ["je", "ne", "parle", "pas", "français"],
                "explanation": "Je ne parle pas français."
            },
            # 6
            {
                "type": "input",
                "question_nl": "Vul aan: \"Je ____ beaucoup de travail.\" (ik heb veel werk)",
                "answer": "ai",
                "explanation": "J'ai beaucoup de travail."
            },
            # 7
            {
                "type": "mc",
                "question_nl": "Welke zin is de juiste ontkenning van \"Je suis opérateur cargo.\"?",
                "options": [
                    "Je ne suis opérateur cargo pas.",
                    "Je ne suis pas opérateur cargo.",
                    "Je suis ne pas opérateur cargo.",
                    "Je ne pas suis opérateur cargo.",
                    "Je ne travaille pas opérateur cargo.",
                    "Je ne suis pas Equinor."
                ],
                "answer": "Je ne suis pas opérateur cargo.",
                "explanation": "Ne ... pas rond het werkwoord: je ne suis pas ..."
            },
            # 8
            {
                "type": "input",
                "question_nl": "Schrijf in het Frans: \"Ik ga niet naar het werk vandaag.\" (werk = au travail)",
                "answer": "je ne vais pas au travail aujourd'hui",
                "explanation": "Je ne vais pas au travail aujourd'hui."
            },
            # 9
            {
                "type": "order",
                "instruction_nl": "Zet de delen in de goede volgorde:",
                "parts": ["je", "suis", "aujourd'hui", "en repos"],
                "correct": ["je", "suis", "en repos", "aujourd'hui"],
                "explanation": "Je suis en repos aujourd'hui."
            },
            # 10
            {
                "type": "mc",
                "question_nl": "Wat is de ik-vorm van \"aller\" (gaan)?",
                "options": ["je vais", "j'ai", "je suis", "je va", "je allé", "je allez"],
                "answer": "je vais",
                "explanation": "Je vais = ik ga."
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
    "Studieplan"
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
    st.markdown(f"**Doel (NL):** {chapter['goal_nl']}")
    st.markdown("---")

    tab_theory, tab_dialogue, tab_exercises = st.tabs(
        ["Uitleg & voorbeelden", "Dialoog & lezen", "Oefeningen & schrijfopdracht"]
    )

    # ---------- Theorie ----------
    with tab_theory:
        if "intro_audio_fr" in chapter:
            if st.button("▶ Luister hoofdstuk-intro (FR)", key=f"intro_{chapter['id']}"):
                audio_data = tts_bytes(chapter["intro_audio_fr"], lang="fr")
                st.audio(audio_data, format="audio/mp3")

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

    # ---------- Dialoog & lezen ----------
    with tab_dialogue:
        dlg = chapter["dialogue"]
        st.markdown(f"### {dlg['title']}")
        for speaker, fr, nl in dlg["turns"]:
            st.markdown(f"**{speaker} – FR:** {fr}")
            st.markdown(f"*NL:* {nl}")
            if st.button(f"▶ Luister ({speaker})", key=f"dlg_{chapter['id']}_{speaker}_{fr}"):
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

        ans = st.radio(
            reading["question_nl"],
            reading["options"],
            key=f"read_q_{chapter['id']}"
        )
        if ans:
            if ans == reading["correct"]:
                st.success("✅ Klopt!")
            else:
                st.error("❌ Niet helemaal, lees/luister de tekst nog een keer.")

    # ---------- Oefeningen & schrijfopdracht ----------
    with tab_exercises:
        st.markdown("### Oefeningen")
        for idx, ex in enumerate(chapter["exercises"], start=1):
            st.markdown(f"#### Oefening {idx}")
            key = f"ch{chapter['id']}_ex{idx}"

            if ex["type"] == "mc":
                st.write(ex["question_nl"])
                choice = st.radio("Kies het beste antwoord:", ex["options"], key=key)
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
                user = st.text_input("Jouw antwoord (Frans):", key=key)
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
                    key=key
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

        st.markdown("---")
        st.markdown("### Schrijfopdracht bij dit hoofdstuk")
        st.markdown(chapter["write_hint"])
        text_key = f"write_{chapter['id']}"
        tekst = st.text_area("Jouw tekst (Frans):", height=220, key=text_key)

        if st.button("Analyseer tekst", key=f"analyse_{chapter['id']}"):
            if not tekst.strip():
                st.warning("Schrijf eerst iets in het tekstvak.")
            else:
                lower = tekst.lower()
                hints = []

                # heel simpele checks op kernpatronen per hoofdstuk
                if chapter["id"] == 1:
                    if "je m'appelle" not in lower:
                        hints.append("Probeer een zin met **je m'appelle ...**.")
                    if "je travaille" not in lower:
                        hints.append("Voeg een zin toe met **je travaille ...**.")
                elif chapter["id"] == 2:
                    if "je suis" not in lower:
                        hints.append("Gebruik **je suis ...** om je functie te noemen.")
                    if "je travaille" not in lower:
                        hints.append("Gebruik **je travaille ...** om te zeggen waar je werkt.")
                elif chapter["id"] == 3:
                    if "ça va" not in lower:
                        hints.append("Probeer een zin met **ça va**.")
                    if "il fait" not in lower:
                        hints.append("Voeg een zin toe met **il fait ...** over het weer.")
                elif chapter["id"] == 4:
                    if "aujourd'hui" not in lower:
                        hints.append("Noem **aujourd'hui** om over vandaag te praten.")
                    if "c'est" not in lower:
                        hints.append("Gebruik **c'est calme / c'est très chargé** voor drukte.")
                elif chapter["id"] == 5:
                    if not any(pr in lower for pr in ["je ", "nous ", "ils ", "elles "]):
                        hints.append("Gebruik verschillende voornaamwoorden zoals **je / nous / ils / elles**.")
                elif chapter["id"] == 6:
                    if "ne" not in lower or "pas" not in lower:
                        hints.append("Gebruik minstens één ontkennende zin met **ne ... pas**.")

                if hints:
                    st.error("Een paar verbeterpunten:")
                    for h in hints:
                        st.markdown(f"- {h}")
                else:
                    st.success("Mooi! Je gebruikt de belangrijkste structuren voor dit hoofdstuk.")

                st.markdown("#### Voorbeeldtekst")
                st.code(chapter["write_example"], language="markdown")

# ---------------------------------------------------------
# Modus: Schrijven (vrije teksten)
# ---------------------------------------------------------

elif mode == "Schrijven (vrije teksten)":
    st.title("Schrijven – vrije teksten over je werk")

    st.markdown("""
Gebruik dit scherm om langere teksten te schrijven, bijvoorbeeld:

- een korte mail aan een Franse collega  
- een beschrijving van je werkdag  
- een korte uitleg van een incident (eenvoudig)  
""")

    tekst = st.text_area("Jouw tekst (Frans):", height=260)

    if st.button("Eenvoudige analyse"):
        if not tekst.strip():
            st.warning("Schrijf eerst iets in het tekstvak.")
        else:
            lower = tekst.lower()
            hints = []
            if "je m'appelle" not in lower and "je suis" not in lower:
                hints.append("Noem jezelf met **je m'appelle ...** of **je suis ...**.")
            if "je travaille" not in lower:
                hints.append("Vertel waar je werkt met **je travaille ...**.")
            if "cargo" not in lower and "terminal" not in lower and "navire" not in lower:
                hints.append("Probeer woorden als **cargo / terminal / navire** toe te voegen.")
            if "aujourd'hui" not in lower and "demain" not in lower:
                hints.append("Noem een tijdsaanduiding zoals **aujourd'hui / demain**.")

            if hints:
                st.error("Suggesties voor verbetering:")
                for h in hints:
                    st.markdown(f"- {h}")
            else:
                st.success("Je tekst bevat al veel nuttige elementen voor jouw doel.")

# ---------------------------------------------------------
# Modus: Studieplan
# ---------------------------------------------------------

elif mode == "Studieplan":
    st.title("Studieplan – 20–30 minuten per dag")

    st.markdown("""
### Aanpak volgens de 20-uur-methode

- **Deelvaardigheden**: kennismaking, over werk praten, smalltalk, werkdruk, zinsbouw, ontkenning.  
- **Leer genoeg om jezelf te corrigeren**: gebruik de uitleg + voorbeeldzinnen.  
- **Verwijder drempels**: open direct de app, zet notificaties uit, plan een vast moment.  
- **20 uur gefocust oefenen**: 20–30 minuten per dag, ~4 weken.[web:62][web:72]

### Voorstel per week

**Week 1**  
- Dag 1–2: Hoofdstuk 1 (kennismaking)  
- Dag 3–4: Hoofdstuk 2 (over jouw werk, FR UI)  
- Dag 5: Herhalen + korte schrijfopdracht (hoofdstuk 1 of 2)

**Week 2**  
- Dag 1–2: Hoofdstuk 3 (smalltalk + weer)  
- Dag 3–4: Hoofdstuk 4 (werkdruk en planning)  
- Dag 5: Lees- en luistertab per hoofdstuk + korte vrije tekst

**Week 3**  
- Dag 1–2: Hoofdstuk 5 (zinsbouw en voornaamwoorden)  
- Dag 3–4: Hoofdstuk 6 (werkwoorden + ontkenning)  
- Dag 5: Schrijven-modus (vrije tekst over je week)

**Week 4 en verder**  
- Herhaal hoofdstukken waar je fouten maakt in de oefeningen.  
- Mix elke sessie:
  - 10 min uitleg + dialoog/leesopdracht  
  - 10–20 min oefeningen + schrijfopdracht  

Na ~20 uur ben je klaar om een **korte, werkgerelateerde conversatie** te voeren met een Franse collega:
jezelf voorstellen, hoe het gaat, over het weer praten en aangeven hoe druk of rustig je werk is.
    """)
    st.caption("Gebruik altijd een koptelefoon en spreek zinnen hardop na voor maximaal effect.")
