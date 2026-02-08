"""
Cute Love Proposal Website - Single-file Streamlit app with Neon Postgres auth.

Run: streamlit run love.py
  or: python -m streamlit run love.py
Requires: pip install streamlit psycopg2-binary
Env: DATABASE_URL (Neon Postgres connection string). If unset, demo mode accepts any login.
"""
import os
import hashlib
import random
import secrets
import streamlit as st

# -----------------------------------------------------------------------------
# Database (Neon Postgres) - all DB logic in this file
# -----------------------------------------------------------------------------
DATABASE_URL = os.environ.get("DATABASE_URL")
PASSWORD_SALT = os.environ.get("PASSWORD_SALT", "love-demo-salt-change-in-production")


def _hash_password(password: str) -> str:
    return hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), PASSWORD_SALT.encode("utf-8"), 100_000
    ).hex()


def get_conn():
    if not DATABASE_URL:
        return None
    try:
        import psycopg2
        return psycopg2.connect(DATABASE_URL)
    except Exception:
        return None


def init_db():
    conn = get_conn()
    if not conn:
        return
    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    created_at TIMESTAMPTZ DEFAULT NOW()
                )
            """)
        conn.commit()
    finally:
        conn.close()


def verify_user(username: str, password: str) -> bool:
    conn = get_conn()
    if not conn:
        return False
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT password_hash FROM users WHERE username = %s",
                (username.strip(),),
            )
            row = cur.fetchone()
            if not row:
                return False
            return secrets.compare_digest(row[0], _hash_password(password))
    finally:
        conn.close()


def create_user(username: str, password: str) -> bool:
    conn = get_conn()
    if not conn:
        return False
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
                (username.strip(), _hash_password(password)),
            )
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        conn.close()


# -----------------------------------------------------------------------------
# Constants (same layout/colors as original)
# -----------------------------------------------------------------------------
BEAR_IMG = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Cpath fill='%23ec4899' d='M50 85C20 60 5 40 5 25c0-12 10-20 22-20 8 0 15 4 20 10 5-6 12-10 20-10 12 0 22 8 22 20 0 15-15 35-45 60z'/%3E%3Cpath fill='%23f472b6' d='M50 78c-22-18-38-35-38-48 0-9 8-15 18-15 6 0 12 3 16 8 2-1 4-2 6-2 10 0 18 6 18 15 0 13-16 30-38 48z'/%3E%3C/svg%3E"

PHOTO_URLS = [
    "1494790108377-be9c29b29330",
    "1529626455594-4ff0802cfb7e",
    "1516589178581-6cd7833ae3b2",
    "1502139214982-d0ad755818d8",
    "1488426862026-3ee34a7d66df",
]

PHOTOS = [
    "Your smile brightens my darkest days 🌟",
    "Every moment with you is a treasure 💎",
    "You make my heart skip a beat 💓",
    "Your laugh is my favorite sound 🎵",
    "With you, every day feels like magic ✨",
]

LETTER_TEXT = """My Dearest Valentine,

From the moment I met you, my world became brighter and more beautiful. Every smile you share lights up my heart, and every laugh we share together creates memories I treasure forever.

You are the most amazing person I know. Your kindness, your warmth, your incredible spirit - they all make me fall for you more and more each day. When I'm with you, everything feels right, like all the pieces of my life have finally fallen into place.

I love the way you make ordinary moments extraordinary. Whether we're having deep conversations or just enjoying comfortable silence, every second with you is precious. You understand me in ways I never thought possible, and you accept me for who I am.

This Valentine's Day, I want you to know that you mean the world to me. You're not just my Valentine - you're my best friend, my confidant, my happy place. I can't wait to create more beautiful memories with you, to laugh together, to grow together, and to continue this wonderful journey side by side.

Thank you for saying yes. Thank you for being you. Thank you for making my heart so incredibly happy.

Forever yours,
With all my love 💕"""


# -----------------------------------------------------------------------------
# Global CSS (exact same structure, spacing, colors, typography)
# -----------------------------------------------------------------------------
def inject_css():
    st.markdown(
        """
    <style>
    /* Hide Streamlit chrome for full-width layout */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }
    .block-container { padding-top: 1rem; padding-bottom: 1rem; max-width: 100%; }
    /* App layout */
    * { box-sizing: border-box; margin: 0; padding: 0; }
    .love-app { font-family: ui-sans-serif, system-ui, sans-serif; line-height: 1.5; color: #1f2937; }
    .flex-center { display: flex; align-items: center; justify-content: center; flex-wrap: wrap; }
    .flex-col { flex-direction: column; }
    .text-center { text-align: center; }
    .rounded-2xl { border-radius: 1rem; }
    .rounded-3xl { border-radius: 1.5rem; }
    .rounded-full { border-radius: 9999px; }
    .shadow-2xl { box-shadow: 0 25px 50px -12px rgba(0,0,0,0.25); }
    .border-4 { border-width: 4px; border-style: solid; }
    .border-8 { border-width: 8px; border-style: solid; }
    .max-w-md { max-width: 28rem; }
    .max-w-2xl { max-width: 42rem; }
    .max-w-3xl { max-width: 48rem; }
    .max-w-4xl { max-width: 56rem; }
    .mx-auto { margin-left: auto; margin-right: auto; }
    .mb-2 { margin-bottom: 0.5rem; }
    .mb-4 { margin-bottom: 1rem; }
    .mb-6 { margin-bottom: 1.5rem; }
    .mb-8 { margin-bottom: 2rem; }
    .mb-10 { margin-bottom: 2.5rem; }
    .mt-2 { margin-top: 0.5rem; }
    .mt-8 { margin-top: 2rem; }
    .gap-2 { gap: 0.5rem; }
    .gap-3 { gap: 0.75rem; }
    .gap-4 { gap: 1rem; }
    .gap-6 { gap: 1.5rem; }
    .text-gradient { background: linear-gradient(to right, #ec4899, #ef4444, #a855f7); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
    .bg-white-90 { background: rgba(255,255,255,0.9); }
    .bg-white-80 { background: rgba(255,255,255,0.8); }
    .bg-white-95 { background: rgba(255,255,255,0.95); }
    .backdrop-blur { backdrop-filter: blur(8px); }
    @keyframes float { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-20px); } }
    @keyframes pulse { 50% { opacity: 0.7; } }
    @keyframes shake { 0%,100% { transform: translateX(0); } 10%,30%,50%,70%,90% { transform: translateX(-10px); } 20%,40%,60%,80% { transform: translateX(10px); } }
    @keyframes wiggle { 0%,100% { transform: rotate(-5deg); } 50% { transform: rotate(5deg); } }
    @keyframes heartbeat { 0%,100% { transform: scale(1); } 50% { transform: scale(1.1); } }
    @keyframes confetti { 0% { opacity:1; transform: translateY(0) rotate(0); } 100% { opacity:0; transform: translateY(100vh) rotate(360deg); } }
    @keyframes bounce { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-10px); } }
    @keyframes pulse-scale { 0%,100% { transform: scale(1); } 50% { transform: scale(1.05); } }
    @keyframes fade-in { from { opacity:0; transform: translateY(20px); } to { opacity:1; transform: translateY(0); } }
    .animate-float { animation: float 3s ease-in-out infinite; }
    .animate-pulse { animation: pulse 2s ease-in-out infinite; }
    .animate-shake { animation: shake 0.5s; }
    .animate-wiggle { animation: wiggle 1s ease-in-out infinite; }
    .animate-heartbeat { animation: heartbeat 1s ease-in-out infinite; }
    .animate-confetti { animation: confetti linear forwards; }
    .animate-bounce { animation: bounce 1s ease-in-out infinite; }
    .animate-pulse-scale { animation: pulse-scale 2s ease-in-out infinite; }
    .animate-fade-in { animation: fade-in 1s ease-out; }
    .heart-icon { width: 2.5rem; height: 2.5rem; fill: white; }
    .heart-icon-lg { width: 4rem; height: 4rem; fill: white; }
    /* Match Streamlit button to app style */
    .stButton > button { background: linear-gradient(to right, #ec4899, #ef4444, #a855f7) !important; color: white !important; border: none !important; border-radius: 9999px !important; font-weight: 600 !important; padding: 0.75rem 2rem !important; }
    .stButton > button:hover { box-shadow: 0 10px 15px -3px rgba(0,0,0,0.2) !important; }
    </style>
    """,
        unsafe_allow_html=True,
    )


# -----------------------------------------------------------------------------
# Session state init
# -----------------------------------------------------------------------------
def init_session_state():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "user" not in st.session_state:
        st.session_state.user = None
    if "current_tab" not in st.session_state:
        st.session_state.current_tab = 0
    if "no_clicks" not in st.session_state:
        st.session_state.no_clicks = 0
    if "yes_scale" not in st.session_state:
        st.session_state.yes_scale = 1.0
    if "no_col" not in st.session_state:
        st.session_state.no_col = 3
    if "envelope_open" not in st.session_state:
        st.session_state.envelope_open = False
    if "photo_modal" not in st.session_state:
        st.session_state.photo_modal = None
    if "photo_flipped" not in st.session_state:
        st.session_state.photo_flipped = False
    if "login_shake" not in st.session_state:
        st.session_state.login_shake = False


# -----------------------------------------------------------------------------
# Reusable render functions (convert TSX components to Python)
# -----------------------------------------------------------------------------
def render_login_ui():
    """Login screen - same structure, spacing, colors, typography."""
    html = f"""
    <div class="love-app" style="min-height:85vh; display:flex; align-items:center; justify-content:center; padding:1rem; background: linear-gradient(135deg, #fbcfe8, #ffe4e6, #fecaca); position:relative;">
      <div style="position:absolute; inset:0; overflow:hidden; pointer-events:none; opacity:0.2;">
        <img src="{BEAR_IMG}" alt="" style="position:absolute; width:6rem; height:6rem; top:2.5rem; left:2.5rem;" class="animate-float">
        <img src="{BEAR_IMG}" alt="" style="position:absolute; width:6rem; height:6rem; bottom:2.5rem; right:2.5rem; animation-delay:1s;" class="animate-float">
      </div>
      <div style="position:relative; z-index:10;">
        <div class="bg-white-90 backdrop-blur rounded-3xl shadow-2xl p-8 max-w-md border-4 border-pink-200 {'animate-shake' if st.session_state.login_shake else ''}" style="border-color:#f9a8d4;">
          <div class="text-center mb-8">
            <div style="display:inline-flex; align-items:center; justify-content:center; width:5rem; height:5rem; border-radius:9999px; margin-bottom:1rem; background: linear-gradient(135deg, #f472b6, #ef4444);" class="animate-pulse">
              <svg class="heart-icon" viewBox="0 0 24 24" fill="currentColor"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg>
            </div>
            <h1 class="text-4xl font-bold text-gradient mb-2">Something Special 💌</h1>
            <p style="color:#db2777; display:flex; align-items:center; justify-content:center; gap:0.5rem;">✨ Enter to unlock magic ✨</p>
          </div>
        </div>
      </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_ask_permission_ui():
    """Ask Permission screen."""
    html = f"""
    <div class="love-app" style="min-height:85vh; display:flex; align-items:center; justify-content:center; padding:1rem; flex-direction:column; background: linear-gradient(135deg, #e9d5ff, #fce7f3, #fae8ff); position:relative;">
      <div style="position:absolute; inset:0; overflow:hidden; pointer-events:none; opacity:0.15;">
        <img src="{BEAR_IMG}" alt="" style="position:absolute; width:8rem; height:8rem; top:5rem; right:5rem;" class="animate-float">
        <img src="{BEAR_IMG}" alt="" style="position:absolute; width:8rem; height:8rem; bottom:5rem; left:5rem; animation-delay:2s;" class="animate-float">
      </div>
      <div class="text-center max-w-2xl" style="position:relative; z-index:10;">
        <div style="margin-bottom:2rem; display:flex; justify-content:center; gap:1rem;">
          <img src="{BEAR_IMG}" alt="" style="width:5rem; height:5rem;" class="animate-float">
          <span style="font-size:3.75rem; animation-delay:0.5s;" class="animate-float">💖</span>
          <img src="{BEAR_IMG}" alt="" style="width:5rem; height:5rem; animation-delay:1s;" class="animate-float">
        </div>
        <div class="bg-white-80 backdrop-blur rounded-3xl shadow-2xl p-12 border-4 border-pink-300" style="border-color:#f9a8d4;">
          <div class="mb-8">
            <div style="display:inline-flex; align-items:center; justify-content:center; width:6rem; height:6rem; border-radius:9999px; margin-bottom:1.5rem; background: linear-gradient(135deg, #f472b6, #ef4444);" class="animate-pulse-scale">
              <svg class="heart-icon-lg" viewBox="0 0 24 24" fill="currentColor"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg>
            </div>
          </div>
          <h1 class="text-5xl font-bold mb-6 text-gradient animate-fade-in">I Wanna Ask You Something...</h1>
          <p class="text-2xl mb-8 animate-fade-in" style="color:#db2777;">Something really important 💕</p>
          <div style="display:flex; justify-content:center; gap:0.75rem; font-size:2.25rem; margin-bottom:2.5rem;">
            <span class="animate-wiggle">😊</span>
            <span class="animate-wiggle" style="animation-delay:0.2s;">💗</span>
            <span class="animate-wiggle" style="animation-delay:0.4s;">✨</span>
          </div>
        </div>
      </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_valentine_question_ui():
    """Valentine Question screen - YES and No buttons."""
    no_msg = ""
    if st.session_state.no_clicks > 0:
        if st.session_state.no_clicks < 3:
            no_msg = "Come on... give me a chance! 💕"
        elif st.session_state.no_clicks < 6:
            no_msg = "Please? I promise to make you happy! 🥺"
        elif st.session_state.no_clicks < 10:
            no_msg = "You can't catch the NO button! Just say YES! 💝"
        else:
            no_msg = "The YES button is getting bigger for a reason! 😊💖"
    html = f"""
    <div class="love-app" style="min-height:85vh; display:flex; align-items:center; justify-content:center; padding:1rem; flex-direction:column; overflow:hidden; background: linear-gradient(135deg, #fecaca, #fce7f3, #ffedd5); position:relative;">
      <div style="position:absolute; inset:0; overflow:hidden; pointer-events:none; opacity:0.15;">
        <img src="{BEAR_IMG}" alt="" style="position:absolute; width:7rem; height:7rem; left:0%; top:0%;" class="animate-float">
        <img src="{BEAR_IMG}" alt="" style="position:absolute; width:7rem; height:7rem; left:25%; top:30%; animation-delay:1.5s;" class="animate-float">
        <img src="{BEAR_IMG}" alt="" style="position:absolute; width:7rem; height:7rem; left:50%; top:60%; animation-delay:3s;" class="animate-float">
        <img src="{BEAR_IMG}" alt="" style="position:absolute; width:7rem; height:7rem; left:75%; top:20%; animation-delay:4.5s;" class="animate-float">
      </div>
      <div class="text-center max-w-3xl" style="position:relative; z-index:10;">
        <div style="position:absolute; top:-5rem; left:50%; transform:translateX(-50%); display:flex; gap:1rem;">
          <img src="{BEAR_IMG}" alt="" style="width:4rem; height:4rem;">
          <span style="font-size:3.75rem;">❤️</span>
          <img src="{BEAR_IMG}" alt="" style="width:4rem; height:4rem;">
        </div>
        <div class="bg-white-90 backdrop-blur rounded-3xl shadow-2xl p-12 border-4 border-pink-300 relative z-10" style="border-color:#f9a8d4;">
          <div class="mb-8">
            <div style="display:inline-flex; align-items:center; justify-content:center; width:8rem; height:8rem; border-radius:9999px; margin-bottom:1.5rem; background: linear-gradient(135deg, #f472b6, #ef4444, #a855f7);" class="animate-pulse-scale">
              <svg class="heart-icon-lg animate-heartbeat" style="width:4rem;height:4rem;" viewBox="0 0 24 24" fill="currentColor"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg>
            </div>
          </div>
          <h1 class="text-6xl font-bold mb-8 text-gradient">Will You Be My Valentine? 💝</h1>
          <p class="text-2xl mb-12" style="color:#db2777;">Please say yes... 🥺💕</p>
          <div style="position:relative; min-height:200px; display:flex; flex-direction:column; align-items:center; gap:1.5rem;">
            <p class="mt-8 text-pink-500 animate-bounce" style="color:#ec4899;">{no_msg}</p>
          </div>
        </div>
      </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_celebration_ui():
    """Celebration screen."""
    emojis = "💖💕💗💓💝✨⭐🎉"
    confetti_html = "".join(
        f'<div class="absolute animate-confetti" style="left:{i*2}%; top:-20px; animation-delay:{i*0.06}s; animation-duration:{3+i*0.04}s;">{e}</div>'
        for i, e in enumerate(emojis * 7)
    )
    html = f"""
    <div class="love-app" style="min-height:85vh; display:flex; align-items:center; justify-content:center; padding:1rem; position:relative; overflow:hidden; background: linear-gradient(135deg, #fef08a, #fce7f3, #ffe4e6);">
      <div style="position:absolute; inset:0; pointer-events:none;">{confetti_html}</div>
      <div class="text-center max-w-4xl" style="position:relative; z-index:10;">
        <div class="bg-white-90 backdrop-blur rounded-3xl shadow-2xl p-12 border-4 border-pink-300" style="border-color:#f9a8d4;">
          <div class="mb-8 relative">
            <div style="width:16rem; height:16rem; margin:0 auto; border-radius:1.5rem; display:flex; align-items:center; justify-content:center; overflow:hidden; background: linear-gradient(135deg, #fce7f3, #e9d5ff, #fecaca);">
              <img src="{BEAR_IMG}" alt="" style="width:12rem; height:12rem;" class="animate-pulse-scale">
            </div>
            <div style="position:absolute; inset:0; display:flex; align-items:center; justify-content:center; pointer-events:none;">
              <div style="font-size:8rem;" class="animate-float">✨</div>
            </div>
          </div>
          <h1 class="text-6xl font-bold mb-6 text-gradient animate-bounce">Yeeeee You Finally Agreed! 🎊</h1>
          <p class="text-3xl mb-4" style="color:#db2777;">This makes me so happy! 💕</p>
          <div style="display:flex; justify-content:center; gap:0.75rem; font-size:3rem; margin-bottom:2.5rem;">
            <span class="animate-bounce">🥳</span>
            <span class="animate-bounce" style="animation-delay:0.1s;">💝</span>
            <span class="animate-bounce" style="animation-delay:0.2s;">🎉</span>
            <span class="animate-bounce" style="animation-delay:0.3s;">💖</span>
            <span class="animate-bounce" style="animation-delay:0.4s;">✨</span>
          </div>
          <p class="text-2xl mb-8" style="color:#ec4899;">I have something special to show you... 🌸</p>
        </div>
      </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_photo_bouquet_ui():
    """Photo Bouquet screen - flowers + vase."""
    flowers_html = ""
    for i in range(5):
        rot = (i - 2) * 8
        url = f"https://images.unsplash.com/photo-{PHOTO_URLS[i]}?w=200&h=200&fit=crop"
        flowers_html += f"""
        <div style="cursor:pointer; transform: rotate({rot}deg); position:relative;">
          <div style="position:absolute; bottom:0; left:50%; transform:translateX(-50%); width:8px; height:8rem; background:linear-gradient(to bottom, #059669, #047857); z-index:-1;"></div>
          <div style="width:8rem; height:8rem; border-radius:50%; border:8px solid #f472b6; background:white; overflow:hidden; display:flex; align-items:center; justify-content:center;"><img src="{url}" alt="Memory {i+1}" style="width:100%; height:100%; object-fit:cover;"></div>
        </div>
        """
    html = f"""
    <div class="love-app" style="min-height:85vh; display:flex; flex-direction:column; align-items:center; justify-content:center; padding:1rem; padding-top:3rem; padding-bottom:3rem; background: linear-gradient(135deg, #d1fae5, #f0fdfa, #cffafe); position:relative;">
      <div style="position:absolute; inset:0; overflow:hidden; pointer-events:none; opacity:0.15;">
        <img src="{BEAR_IMG}" alt="" style="position:absolute; width:6rem; height:6rem; left:0%; top:0%;" class="animate-float">
        <img src="{BEAR_IMG}" alt="" style="position:absolute; width:6rem; height:6rem; left:22%; top:25%; animation-delay:1.2s;" class="animate-float">
        <img src="{BEAR_IMG}" alt="" style="position:absolute; width:6rem; height:6rem; left:44%; top:50%; animation-delay:2.4s;" class="animate-float">
        <img src="{BEAR_IMG}" alt="" style="position:absolute; width:6rem; height:6rem; left:66%; top:15%; animation-delay:3.6s;" class="animate-float">
        <img src="{BEAR_IMG}" alt="" style="position:absolute; width:6rem; height:6rem; left:88%; top:60%; animation-delay:4.8s;" class="animate-float">
      </div>
      <div class="text-center mb-8" style="position:relative; z-index:10;">
        <h1 class="text-5xl font-bold mb-4 text-gradient">A Bouquet of Memories 💐</h1>
        <p class="text-2xl" style="color:#db2777;">Click on each flower to see a special moment ✨</p>
      </div>
      <div style="position:relative; width:100%; max-width:56rem; margin-bottom:3rem; display:flex; flex-wrap:wrap; justify-content:center; align-items:flex-end; gap:1.5rem;">
        {flowers_html}
      </div>
      <div style="margin-top:2rem; margin-left:auto; margin-right:auto; width:12rem; height:6rem; border-radius:0 0 9999px 9999px; border:4px solid #a855f7; display:flex; align-items:center; justify-content:center; background: linear-gradient(to bottom, #d8b4fe, #c084fc);">
        <span style="font-size:1.5rem;">💕</span>
      </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_final_surprise_ui():
    """Final Surprise - envelope or letter."""
    if st.session_state.envelope_open:
        letter_paras = "".join(
            f'<p style="margin-bottom:1rem; font-size:1.125rem; line-height:1.75; color:#374151;">{p.replace("<", "&lt;").replace(">", "&gt;")}</p>'
            for p in LETTER_TEXT.split("\n\n")
        )
        html = f"""
        <div class="love-app" style="min-height:85vh; display:flex; align-items:center; justify-content:center; padding:1rem; position:relative; overflow:hidden; background: linear-gradient(135deg, #c7d2fe, #e9d5ff, #fce7f3);">
          <div style="position:absolute; inset:0; pointer-events:none; opacity:0.1;">
            <img src="{BEAR_IMG}" alt="" style="position:absolute; width:6rem; height:6rem; left:10%; top:80%;" class="animate-float">
            <img src="{BEAR_IMG}" alt="" style="position:absolute; width:6rem; height:6rem; left:80%; top:20%; animation-delay:2s;" class="animate-float">
          </div>
          <div class="text-center max-w-4xl" style="position:relative; z-index:10;">
            <div class="bg-white-95 backdrop-blur rounded-3xl shadow-2xl p-8 border-4 border-pink-200 max-w-3xl mx-auto text-left" style="border-color:#f9a8d4;">
              <div class="mb-6">
                <div style="font-size:3.75rem; margin-bottom:1rem;">💌</div>
                <h2 class="text-4xl font-bold text-gradient mb-2">A Letter From My Heart</h2>
              </div>
              <div style="max-height:24rem; overflow-y:auto; padding-right:1rem;">
                <div style="margin-bottom:1rem;">{letter_paras}</div>
              </div>
              <div style="margin-top:2rem; display:flex; justify-content:center; gap:0.5rem; font-size:1.875rem;">
                <span>💖</span><span>💖</span><span>💖</span><span>💖</span><span>💖</span><span>💖</span><span>💖</span>
              </div>
            </div>
          </div>
        </div>
        """
    else:
        html = f"""
        <div class="love-app" style="min-height:85vh; display:flex; align-items:center; justify-content:center; padding:1rem; position:relative; overflow:hidden; background: linear-gradient(135deg, #c7d2fe, #e9d5ff, #fce7f3);">
          <div style="position:absolute; inset:0; pointer-events:none; opacity:0.1;">
            <img src="{BEAR_IMG}" alt="" style="position:absolute; width:6rem; height:6rem; left:10%; top:80%;" class="animate-float">
            <img src="{BEAR_IMG}" alt="" style="position:absolute; width:6rem; height:6rem; left:80%; top:20%; animation-delay:2s;" class="animate-float">
          </div>
          <div class="text-center max-w-4xl" style="position:relative; z-index:10;">
            <h1 class="text-5xl font-bold mb-12 text-gradient">Your Final Surprise 💌</h1>
            <div style="width:300px; height:200px; margin:0 auto; background: linear-gradient(135deg, #f87171, #ec4899); border-radius:0.5rem; box-shadow:0 25px 50px -12px rgba(0,0,0,0.25); position:relative; cursor:pointer;">
              <div style="position:absolute; top:3rem; left:50%; transform:translateX(-50%); width:4rem; height:4rem; background:white; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:1.875rem; box-shadow:0 4px 6px -1px rgba(0,0,0,0.1);">💝</div>
              <div style="position:absolute; bottom:3rem; left:2rem; right:2rem;">
                <div style="height:4px; background:#fca5a5; border-radius:4px; opacity:0.5;"></div>
                <div style="height:4px; background:#fca5a5; border-radius:4px; opacity:0.5; width:75%; margin-top:8px;"></div>
              </div>
            </div>
            <p class="mt-12 text-2xl animate-pulse" style="color:#db2777;">Click the button below to open your letter 💕</p>
          </div>
        </div>
        """
    st.markdown(html, unsafe_allow_html=True)


def render_see_you_soon_ui():
    """See You Soon screen."""
    html = f"""
    <div class="love-app" style="min-height:85vh; display:flex; align-items:center; justify-content:center; padding:1rem; position:relative; overflow:hidden; background: linear-gradient(135deg, #ffe4e6, #fee2e2, #fce7f3);">
      <div style="position:absolute; inset:0; pointer-events:none; opacity:0.15;">
        <img src="{BEAR_IMG}" alt="" style="position:absolute; width:7rem; height:7rem; left:10%; top:100%;" class="animate-float">
        <img src="{BEAR_IMG}" alt="" style="position:absolute; width:7rem; height:7rem; left:50%; top:100%; animation-delay:2s;" class="animate-float">
        <img src="{BEAR_IMG}" alt="" style="position:absolute; width:7rem; height:7rem; left:90%; top:100%; animation-delay:4s;" class="animate-float">
      </div>
      <div class="text-center max-w-4xl" style="position:relative; z-index:10;">
        <div class="bg-white-90 backdrop-blur rounded-3xl shadow-2xl p-12 border-4 border-red-300" style="border-color:#fca5a5;">
          <div style="width:8rem; height:8rem; border-radius:50%; background: linear-gradient(135deg, #ef4444, #ec4899, #f43f5e); display:inline-flex; align-items:center; justify-content:center; color:white; margin-bottom:2rem;">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" style="width:4rem; height:4rem;"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
          </div>
          <h1 class="text-6xl font-bold mb-6 text-gradient">February 13th</h1>
          <div class="mb-8">
            <p style="font-size:2.25rem; color:#dc2626; font-weight:600; margin-bottom:1rem; display:flex; justify-content:center; align-items:center; gap:0.75rem;">
              <svg class="heart-icon animate-heartbeat" style="width:2.5rem;height:2.5rem;fill:#ef4444;" viewBox="0 0 24 24" fill="currentColor"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg>
              See You Soon!
              <svg class="heart-icon animate-heartbeat" style="width:2.5rem;height:2.5rem;fill:#ef4444;" viewBox="0 0 24 24" fill="currentColor"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg>
            </p>
            <p class="text-2xl" style="color:#db2777;">I can't wait for our special day together 💕</p>
          </div>
          <div style="display:flex; justify-content:center; align-items:center; gap:1.5rem; margin-bottom:2rem;">
            <img src="{BEAR_IMG}" alt="" style="width:4rem; height:4rem;" class="animate-float">
            <span style="font-size:3rem;">💝</span>
            <img src="{BEAR_IMG}" alt="" style="width:4rem; height:4rem; animation-delay:0.3s;" class="animate-float">
            <span style="font-size:3rem;">✨</span>
            <img src="{BEAR_IMG}" alt="" style="width:4rem; height:4rem; animation-delay:0.6s;" class="animate-float">
          </div>
          <div style="border-radius:1rem; padding:2rem; border:2px solid #fecaca; background: linear-gradient(135deg, #fef2f2, #fce7f3);">
            <p class="text-2xl text-gray-700 mb-4">Mark your calendar! 📅</p>
            <p class="text-xl text-gray-600 leading-relaxed">Get ready for an unforgettable day filled with love, laughter, and beautiful moments together. This is just the beginning of our amazing journey! 💖</p>
          </div>
          <p class="mt-10 text-xl font-semibold animate-pulse" style="color:#ef4444;">✨ Can't wait to see you ✨</p>
        </div>
      </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# Main app
# -----------------------------------------------------------------------------
def main():
    st.set_page_config(
        page_title="Cute Love Proposal Website",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    init_session_state()
    init_db()
    inject_css()

    # Not logged in: show login screen
    if not st.session_state.logged_in:
        render_login_ui()
        with st.form("login_form"):
            username = st.text_input("Your name ✨", key="login_username", placeholder="Your name ✨")
            password = st.text_input("Secret word 🔒", type="password", key="login_password", placeholder="Secret word 🔒")
            submitted = st.form_submit_button("Enter the Love Zone 💕")
        if submitted:
            u, p = (username or "").strip(), (password or "").strip()
            if not u or not p:
                st.session_state.login_shake = True
                st.error("Please enter both name and secret word.")
            else:
                if DATABASE_URL and get_conn():
                    if verify_user(u, p):
                        st.session_state.logged_in = True
                        st.session_state.user = u
                        st.session_state.current_tab = 1
                        st.session_state.login_shake = False
                    else:
                        st.session_state.login_shake = True
                        st.error("Name or secret word not recognized.")
                else:
                    # Demo mode: accept any non-empty login
                    st.session_state.logged_in = True
                    st.session_state.user = u
                    st.session_state.current_tab = 1
                    st.session_state.login_shake = False
            st.rerun()
        # Register (for Neon): create first user
        if DATABASE_URL and get_conn():
            with st.expander("First time? Register"):
                ru = st.text_input("Username", key="reg_username", placeholder="Your name")
                rp = st.text_input("Password", type="password", key="reg_password", placeholder="Secret word")
                if st.button("Register", key="register_btn") and ru and rp:
                    if create_user(ru.strip(), rp):
                        st.success("Registered! You can log in above.")
                    else:
                        st.error("Username may already exist.")
        return

    # Logged in: show screen by current_tab
    tab = st.session_state.current_tab

    if tab == 1:
        render_ask_permission_ui()
        if st.button("ASK!!! 💌"):
            st.session_state.current_tab = 2
            st.rerun()
        return

    if tab == 2:
        render_valentine_question_ui()
        # YES button first (centered), then No in random column
        c1, c2, c3, c4, c5 = st.columns([1, 1, 2, 1, 1])
        with c3:
            if st.button("YES! 💚✨", key="yes_btn"):
                st.session_state.current_tab = 3
                st.rerun()
        cols = st.columns(7)
        with cols[st.session_state.no_col]:
            if st.button("No 😢", key="no_btn"):
                st.session_state.no_clicks += 1
                st.session_state.yes_scale = min(st.session_state.yes_scale + 0.15, 2.5)
                st.session_state.no_col = random.randint(0, 6)
                st.rerun()
        return

    if tab == 3:
        render_celebration_ui()
        if st.button("✨ Next Surprise ✨"):
            st.session_state.current_tab = 4
            st.rerun()
        return

    if tab == 4:
        render_photo_bouquet_ui()
        # Flower buttons (click to "view" - we show message in expander or next run with modal state)
        c0, c1, c2, c3, c4 = st.columns(5)
        for i, col in enumerate([c0, c1, c2, c3, c4]):
            with col:
                if st.button(f"View memory {i+1} 💐", key=f"flower_{i}"):
                    st.session_state.photo_modal = i
                    st.rerun()
        if st.session_state.photo_modal is not None:
            idx = st.session_state.photo_modal
            st.markdown(
                f'<div class="bg-white-95 rounded-2xl shadow-2xl p-8 border-4 border-pink-200 mb-4" style="border-color:#f9a8d4;">'
                f'<p class="text-2xl font-semibold mb-4" style="color:#be185d;">{PHOTOS[idx]}</p>'
                f'<img src="https://images.unsplash.com/photo-{PHOTO_URLS[idx]}?w=400&h=500&fit=crop" alt="Memory" style="width:100%; max-width:20rem; border-radius:0.5rem;">'
                f'</div>',
                unsafe_allow_html=True,
            )
            if st.button("Close 💝", key="close_photo"):
                st.session_state.photo_modal = None
                st.rerun()
        if st.button("Ready for the FINAL SURPRISE!!!! 🎁✨", key="btn_bouquet"):
            st.session_state.photo_modal = None
            st.session_state.current_tab = 5
            st.rerun()
        return

    if tab == 5:
        render_final_surprise_ui()
        if not st.session_state.envelope_open:
            if st.button("Open envelope 💕", key="open_env"):
                st.session_state.envelope_open = True
                st.rerun()
        else:
            if st.button("Continue... 💕", key="btn_letter"):
                st.session_state.current_tab = 6
                st.rerun()
        return

    if tab == 6:
        render_see_you_soon_ui()
        return


if __name__ == "__main__":
    main()
