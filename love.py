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


def get_connection():
    try:
        conn = psycopg2.connect(
            host=st.secrets["neon"]["host"],
            database=st.secrets["neon"]["database"],
            user=st.secrets["neon"]["user"],
            password=st.secrets["neon"]["password"],
        )
        return conn
    except Exception as e:
        st.error(f"Could not connect to the database. Please try again later.")
        return None


def signup_user(username: str, password: str) -> bool:
    if not username.strip() or not password.strip():
        return False
    conn = get_connection()
    if not conn:
        return False
    try:
        cur = conn.cursor()
        password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        cur.execute(
            "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
            (username.strip(), password_hash),
        )
        conn.commit()
        cur.close()
        return True
    except psycopg2.IntegrityError:
        conn.rollback()
        return False
    except Exception:
        if conn:
            conn.rollback()
        return False
    finally:
        if conn:
            conn.close()


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
    if "show_signup" not in st.session_state:
        st.session_state.show_signup = False


def apply_theme():
    st.markdown(
        """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=Quicksand:wght@400;500;600&display=swap');
    .stApp { background: linear-gradient(165deg, #fff5f8 0%, #ffe8f0 35%, #ffdde8 100%); }
    h1, h2, h3 { font-family: 'Cormorant Garamond', serif !important; color: #8b3a5c !important; font-weight: 600 !important; }
    p, .stMarkdown { font-family: 'Quicksand', sans-serif !important; color: #5c3a4a !important; }
    .stButton > button {
        font-family: 'Quicksand', sans-serif !important;
        background: linear-gradient(135deg, #d4567a 0%, #b83a5e 100%) !important;
        color: #fff !important;
        border: none !important;
        border-radius: 999px !important;
        padding: 0.6rem 1.8rem !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease !important;
    }
    .stButton > button:hover {
        transform: scale(1.03) !important;
        box-shadow: 0 6px 20px rgba(184, 58, 94, 0.35) !important;
    }
    .heart-emoji { font-size: 2.5rem; margin: 0.25rem; }
    .letter-box {
        font-family: 'Cormorant Garamond', serif;
        font-size: 1.15rem;
        line-height: 1.85;
        color: #4a3545;
        max-width: 42rem;
        margin: 2rem auto;
        padding: 2rem;
        background: rgba(255,255,255,0.7);
        border-radius: 12px;
        box-shadow: 0 4px 24px rgba(139, 58, 92, 0.12);
        animation: fadeIn 1.2s ease-out;
    }
    @keyframes fadeIn { from { opacity: 0; transform: translateY(12px); } to { opacity: 1; transform: translateY(0); } }
    .final-message {
        font-family: 'Cormorant Garamond', serif;
        font-size: clamp(1.8rem, 5vw, 2.8rem);
        font-weight: 600;
        color: #8b3a5c;
        text-align: center;
        margin: 3rem auto;
        padding: 2rem;
        animation: fadeIn 1s ease-out;
    }
    div[data-testid="stVerticalBlock"] > div { padding: 0.5rem 0; }
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
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Login", key="btn_login"):
            if verify_user(username, password):
                st.session_state.screen = SCREEN_BUILDUP
                st.rerun()
            else:
                st.error("Invalid credentials. Try again.")
    with col2:
        if st.button("First time? Create access", key="btn_signup_link"):
            st.session_state.show_signup = True
            st.rerun()

    if st.session_state.get("show_signup"):
        st.divider()
        st.markdown("**Create your access**")
        su_user = st.text_input("Choose username", key="signup_username", placeholder="Username")
        su_pass = st.text_input("Choose password", type="password", key="signup_password", placeholder="Password")
        if st.button("Create", key="btn_signup"):
            if signup_user(su_user, su_pass):
                st.success("Account created. You can log in now.")
                st.session_state.show_signup = False
                st.rerun()
            else:
                st.error("Username may already exist or fields are invalid.")


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
