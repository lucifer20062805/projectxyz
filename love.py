# love.py
# Run: python -m streamlit run love.py

import os
import random
import streamlit as st
import psycopg2
import bcrypt

SCREEN_LOGIN = 1
SCREEN_BUILDUP = 2
SCREEN_PROPOSAL = 3
SCREEN_CELEBRATION = 4
SCREEN_GALLERY = 5
SCREEN_ENVELOPE = 6
SCREEN_LETTER = 7
SCREEN_FINAL = 8

PINK_SOFT = "#fce4ec"
PINK_ROSE = "#e8b4bc"
PINK_MAIN = "#c48b9f"
ROSE_DEEP = "#9e6b7a"
LAVENDER = "#d4c4d0"
WHITE_WARM = "#fef9fb"
TEXT_PRIMARY = "#5c4349"
TEXT_ACCENT = "#7d5a65"
SHADOW = "rgba(158, 107, 122, 0.2)"


def get_connection():
    try:
        conn = psycopg2.connect(
            host=st.secrets["neon"]["host"],
            database=st.secrets["neon"]["database"],
            user=st.secrets["neon"]["user"],
            password=st.secrets["neon"]["password"],
        )
        return conn
    except Exception:
        st.error("Could not connect to the database. Please try again later.")
        return None


def verify_user(username: str, password: str) -> bool:
    if not username.strip() or not password.strip():
        return False
    conn = get_connection()
    if not conn:
        return False
    try:
        cur = conn.cursor()
        cur.execute("SELECT password_hash FROM users WHERE username = %s", (username.strip(),))
        row = cur.fetchone()
        cur.close()
        if row is None:
            return False
        stored_hash = row[0]
        return bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode("utf-8"))
    except Exception:
        return False
    finally:
        if conn:
            conn.close()


def asset_path(*parts):
    base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, "assets", *parts)


def init_session_state():
    if "screen" not in st.session_state:
        st.session_state.screen = SCREEN_LOGIN
    if "no_button_col" not in st.session_state:
        st.session_state.no_button_col = random.randint(0, 4)
    if "envelope_opened" not in st.session_state:
        st.session_state.envelope_opened = False
    if "photos_flipped" not in st.session_state:
        st.session_state.photos_flipped = []


def apply_theme():
    st.markdown(
        f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=Quicksand:wght@400;500;600&display=swap');
    .stApp {{
        background: linear-gradient(160deg, {WHITE_WARM} 0%, {PINK_SOFT} 40%, {LAVENDER} 100%) !important;
    }}
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(160deg, {WHITE_WARM} 0%, {PINK_SOFT} 40%, {LAVENDER} 100%) !important;
    }}
    h1, h2, h3 {{
        font-family: 'Cormorant Garamond', serif !important;
        color: {ROSE_DEEP} !important;
        font-weight: 600 !important;
        letter-spacing: 0.02em !important;
    }}
    p, .stMarkdown, [data-testid="stMarkdown"] {{
        font-family: 'Quicksand', sans-serif !important;
        color: {TEXT_PRIMARY} !important;
    }}
    .stButton > button {{
        font-family: 'Quicksand', sans-serif !important;
        background: linear-gradient(135deg, {PINK_MAIN} 0%, {ROSE_DEEP} 100%) !important;
        color: {WHITE_WARM} !important;
        border: none !important;
        border-radius: 999px !important;
        padding: 0.65rem 1.9rem !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease !important;
        box-shadow: 0 4px 14px {SHADOW} !important;
    }}
    .stButton > button:hover {{
        transform: scale(1.04) !important;
        box-shadow: 0 6px 22px {SHADOW} !important;
        color: {WHITE_WARM} !important;
        border: none !important;
    }}
    [data-testid="stTextInput"] input {{
        background: rgba(255,255,255,0.85) !important;
        color: {TEXT_PRIMARY} !important;
        border: 1px solid {PINK_ROSE} !important;
        border-radius: 10px !important;
        font-family: 'Quicksand', sans-serif !important;
    }}
    [data-testid="stTextInput"] input:focus {{
        border-color: {PINK_MAIN} !important;
        box-shadow: 0 0 0 2px {SHADOW} !important;
    }}
    [data-testid="stAlert"] {{
        background: rgba(255,255,255,0.9) !important;
        border: 1px solid {PINK_ROSE} !important;
        border-radius: 10px !important;
        color: {TEXT_PRIMARY} !important;
        font-family: 'Quicksand', sans-serif !important;
    }}
    .heart-emoji {{ font-size: 2.5rem; margin: 0.35rem 0; }}
    .letter-box {{
        font-family: 'Cormorant Garamond', serif;
        font-size: 1.15rem;
        line-height: 1.9;
        color: {TEXT_PRIMARY};
        max-width: 42rem;
        margin: 2rem auto;
        padding: 2.25rem;
        background: rgba(254, 249, 251, 0.92);
        border: 1px solid {PINK_ROSE};
        border-radius: 14px;
        box-shadow: 0 6px 28px {SHADOW};
        animation: fadeIn 1.2s ease-out;
    }}
    @keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(14px); }} to {{ opacity: 1; transform: translateY(0); }} }}
    .final-message {{
        font-family: 'Cormorant Garamond', serif;
        font-size: clamp(1.85rem, 5vw, 2.9rem);
        font-weight: 600;
        color: {ROSE_DEEP};
        text-align: center;
        margin: 3rem auto;
        padding: 2rem;
        animation: fadeIn 1s ease-out;
        letter-spacing: 0.02em;
    }}
    div[data-testid="stVerticalBlock"] > div {{ padding: 0.5rem 0; }}
    .stCaption {{
        font-family: 'Quicksand', sans-serif !important;
        color: {TEXT_ACCENT} !important;
    }}
    </style>
    """,
        unsafe_allow_html=True,
    )


def screen_login():
    st.markdown('<p class="heart-emoji" style="text-align:center;">💖</p>', unsafe_allow_html=True)
    st.markdown("### Welcome to My Heart")
    st.markdown("Enter your details to begin this journey.")
    username = st.text_input("Username", key="login_username", placeholder="Your name")
    password = st.text_input("Password", type="password", key="login_password", placeholder="Your secret")
    if st.button("Login", key="btn_login"):
        if verify_user(username, password):
            st.session_state.screen = SCREEN_BUILDUP
            st.rerun()
        else:
            st.error("Invalid credentials. Try again.")


def screen_buildup():
    st.markdown('<p class="heart-emoji" style="text-align:center;">💕</p>', unsafe_allow_html=True)
    st.markdown("### I wanna ask you something…")
    st.markdown("Take a breath. Something special is waiting for you.")
    if st.button("I'm ready", key="btn_buildup"):
        st.session_state.screen = SCREEN_PROPOSAL
        st.rerun()


def screen_proposal():
    st.markdown('<p class="heart-emoji" style="text-align:center;">💘</p>', unsafe_allow_html=True)
    st.markdown("### Will you be my Valentine?")
    cols = st.columns(5)
    yes_col = 0
    no_col = st.session_state.no_button_col
    if no_col == yes_col:
        st.session_state.no_button_col = (no_col + 1) % 5
        no_col = st.session_state.no_button_col
    for i in range(5):
        with cols[i]:
            if i == yes_col:
                if st.button("YES 💖", key="btn_yes"):
                    st.session_state.screen = SCREEN_CELEBRATION
                    st.rerun()
            elif i == no_col:
                if st.button("NO", key="btn_no"):
                    prev = st.session_state.no_button_col
                    st.session_state.no_button_col = random.randint(0, 4)
                    while st.session_state.no_button_col == prev or st.session_state.no_button_col == yes_col:
                        st.session_state.no_button_col = random.randint(0, 4)
                    st.rerun()


def screen_celebration():
    st.balloons()
    st.markdown("### You said yes!")
    st.markdown("Thank you for making me the happiest. Let's keep going.")
    gif_path = asset_path("celebration.gif")
    if os.path.isfile(gif_path):
        st.image(gif_path, use_container_width=True)
    if st.button("Next", key="btn_celebration"):
        st.session_state.screen = SCREEN_GALLERY
        if not st.session_state.photos_flipped:
            st.session_state.photos_flipped = [False] * 5
        st.rerun()


def screen_gallery():
    st.markdown("### A little gallery just for you")
    memories = [
        ("photo1.jpg", "Memory 1: Our first date was magical."),
        ("photo2.jpg", "Memory 2: You make me smile every day."),
        ("photo3.jpg", "Your laugh is my favorite sound."),
        ("photo4.jpg", "Together, we're unstoppable."),
        ("photo5.jpg", "I love you more than words can say."),
    ]
    while len(st.session_state.photos_flipped) < len(memories):
        st.session_state.photos_flipped.append(False)
    cols = st.columns(min(5, len(memories)))
    for i, (img_name, caption) in enumerate(memories):
        with cols[i]:
            path = asset_path("photos", img_name)
            if st.button(f"Photo {i + 1}", key=f"gal_btn_{i}"):
                st.session_state.photos_flipped[i] = not st.session_state.photos_flipped[i]
                st.rerun()
            if st.session_state.photos_flipped[i]:
                st.caption(caption)
            else:
                if os.path.isfile(path):
                    st.image(path, use_container_width=True)
                else:
                    st.caption(f"Photo {i + 1}")

    if st.button("Ready for the final surprise", key="btn_gallery"):
        st.session_state.screen = SCREEN_ENVELOPE
        st.rerun()


def screen_envelope():
    st.markdown("### The final surprise")
    if not st.session_state.envelope_opened:
        env_path = asset_path("envelope.png")
        if os.path.isfile(env_path):
            st.image(env_path, use_container_width=True)
        if st.button("Open envelope", key="btn_open_env"):
            st.session_state.envelope_opened = True
            st.rerun()
    else:
        open_path = asset_path("envelope_open.png")
        if os.path.isfile(open_path):
            st.image(open_path, use_container_width=True)
        if st.button("Read letter", key="btn_read_letter"):
            st.session_state.screen = SCREEN_LETTER
            st.rerun()


def screen_letter():
    letter = """
My Dearest,

From the moment I first saw you, I knew there was something special. Your smile lights up my world. Every time we talk, I feel a warmth I can't explain. You have this way of making me feel alive, cherished, and happy.

I remember our first conversation—how nervous I was, and how you put me at ease. Since then, we've shared so many beautiful moments: laughing until our sides hurt, exploring new places, and just being ourselves. You've shown me what true love feels like. I can't imagine my life without you.

You inspire me every day. Your strength, intelligence, and compassion amaze me. When I'm with you, time seems to stand still and worries fade. You are my rock, my confidant, and my greatest adventure.

I want to be there for you through thick and thin, to support your dreams, and to create a lifetime of memories together. You mean everything to me. I promise to love you with all my heart, forever.

Will you be my Valentine, not just today, but every day?

Forever yours.
"""
    st.markdown(
        f'<div class="letter-box">{letter.replace(chr(10), "<br>")}</div>',
        unsafe_allow_html=True,
    )
    if st.button("Next", key="btn_letter"):
        st.session_state.screen = SCREEN_FINAL
        st.rerun()


def screen_final():
    st.markdown(
        '<p class="final-message">See you on 13th Babe… 💖</p>',
        unsafe_allow_html=True,
    )


def main():
    st.set_page_config(page_title="For You", page_icon="💖", layout="centered", initial_sidebar_state="collapsed")
    init_session_state()
    apply_theme()

    if st.session_state.screen == SCREEN_LOGIN:
        screen_login()
    elif st.session_state.screen == SCREEN_BUILDUP:
        screen_buildup()
    elif st.session_state.screen == SCREEN_PROPOSAL:
        screen_proposal()
    elif st.session_state.screen == SCREEN_CELEBRATION:
        screen_celebration()
    elif st.session_state.screen == SCREEN_GALLERY:
        screen_gallery()
    elif st.session_state.screen == SCREEN_ENVELOPE:
        screen_envelope()
    elif st.session_state.screen == SCREEN_LETTER:
        screen_letter()
    else:
        screen_final()


if __name__ == "__main__":
    main()
