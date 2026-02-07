# love.py

import streamlit as st
import psycopg2
import random
import streamlit.components.v1 as components

# Database connection using Streamlit secrets (set up in Streamlit Cloud or locally)
def get_db_connection():
    return psycopg2.connect(
        host=st.secrets["neon"]["host"],
        database=st.secrets["neon"]["database"],
        user=st.secrets["neon"]["user"],
        password=st.secrets["neon"]["password"]
    )

# Function to check login credentials
def check_login(username, password):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result is not None

# Initialize session state
if 'tab' not in st.session_state:
    st.session_state.tab = 1
if 'no_clicks' not in st.session_state:
    st.session_state.no_clicks = 0
if 'photos_flipped' not in st.session_state:
    st.session_state.photos_flipped = [False] * 5  # Assuming 5 photos
if 'envelope_opened' not in st.session_state:
    st.session_state.envelope_opened = False

# Custom CSS for love theme
st.markdown("""
<style>
body {
    background-color: #ffe6f2;
    font-family: 'Arial', sans-serif;
}
.stButton>button {
    background-color: #ff69b4;
    color: white;
    border-radius: 10px;
    border: none;
    padding: 10px 20px;
    font-size: 16px;
}
.stButton>button:hover {
    background-color: #ff1493;
}
.heart {
    color: #ff69b4;
    font-size: 50px;
}
.flip-card {
    background-color: transparent;
    width: 200px;
    height: 200px;
    perspective: 1000px;
}
.flip-card-inner {
    position: relative;
    width: 100%;
    height: 100%;
    text-align: center;
    transition: transform 0.8s;
    transform-style: preserve-3d;
}
.flip-card.flipped .flip-card-inner {
    transform: rotateY(180deg);
}
.flip-card-front, .flip-card-back {
    position: absolute;
    width: 100%;
    height: 100%;
    -webkit-backface-visibility: hidden;
    backface-visibility: hidden;
}
.flip-card-back {
    transform: rotateY(180deg);
    background-color: #f8f9fa;
    padding: 20px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# Tab 1: Login
if st.session_state.tab == 1:
    st.title("💖 Welcome to My Heart 💖")
    st.markdown('<div class="heart">❤️</div>', unsafe_allow_html=True)
    st.markdown("Enter your login details to start this romantic journey!")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if check_login(username, password):
            st.session_state.tab = 2
            st.rerun()
        else:
            st.error("Invalid credentials. Try again!")

# Tab 2: I wanna ask u something
elif st.session_state.tab == 2:
    st.title("💕 I Wanna Ask You Something 💕")
    st.markdown("Are you ready for a special question?")
    if st.button("ASK!!!"):
        st.session_state.tab = 3
        st.rerun()

# Tab 3: Will u be my Valentine
elif st.session_state.tab == 3:
    st.title("💘 Will You Be My Valentine? 💘")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("YES"):
            st.session_state.tab = 4
            st.rerun()
    with col2:
        # Running away NO button using HTML/JS
        no_button_html = f"""
        <button id="no-button" onclick="moveButton()" style="position: absolute; left: {random.randint(0, 300)}px; top: {random.randint(0, 300)}px; background-color: #ff69b4; color: white; border-radius: 10px; border: none; padding: 10px 20px; font-size: 16px;">NO</button>
        <script>
        function moveButton() {{
            var button = document.getElementById('no-button');
            button.style.left = Math.random() * 300 + 'px';
            button.style.top = Math.random() * 300 + 'px';
        }}
        </script>
        """
        components.html(no_button_html, height=400)

# Tab 4: Celebration
elif st.session_state.tab == 4:
    st.title("🎉 Yeeeee You Finally Agreed! 🎉")
    st.image("https://media.giphy.com/media/3o7TKz9bX9v9Kz9bXa/giphy.gif")  # Placeholder celebration GIF
    if st.button("Next"):
        st.session_state.tab = 5
        st.rerun()

# Tab 5: Flower bouquet with photos
elif st.session_state.tab == 5:
    st.title("🌸 A Bouquet Just for You 🌸")
    st.image("https://example.com/bouquet.jpg")  # Placeholder bouquet image
    
    # Assuming 5 photos with flip functionality
    photos = [
        {"front": "https://example.com/photo1.jpg", "back_text": "Memory 1: Our first date was magical!"},
        {"front": "https://example.com/photo2.jpg", "back_text": "Memory 2: You make me smile every day."},
        {"front": "https://example.com/photo3.jpg", "back_text": "Memory 3: Your laugh is my favorite sound."},
        {"front": "https://example.com/photo4.jpg", "back_text": "Memory 4: Together, we're unstoppable."},
        {"front": "https://example.com/photo5.jpg", "back_text": "Memory 5: I love you more than words can say."}
    ]
    
    cols = st.columns(5)
    for i, photo in enumerate(photos):
        with cols[i]:
            if st.button(f"Photo {i+1}"):
                st.session_state.photos_flipped[i] = not st.session_state.photos_flipped[i]
                st.rerun()
            
            if st.session_state.photos_flipped[i]:
                st.markdown(f"""
                <div class="flip-card flipped">
                    <div class="flip-card-inner">
                        <div class="flip-card-front">
                            <img src="{photo['front']}" style="width:100%; height:100%; border-radius:10px;">
                        </div>
                        <div class="flip-card-back">
                            <p>{photo['back_text']}</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.image(photo['front'], width=200)
    
    if st.button("Ready for the FINAL SURPRISE!!!!"):
        st.session_state.tab = 6
        st.rerun()

# Tab 6: Envelope
elif st.session_state.tab == 6:
    st.title("📬 The Final Surprise 📬")
    if not st.session_state.envelope_opened:
        st.image("https://example.com/envelope.jpg")  # Placeholder envelope image
        if st.button("Open Envelope"):
            st.session_state.envelope_opened = True
            st.rerun()
    else:
        st.session_state.tab = 7
        st.rerun()

# Tab 7: Letter
elif st.session_state.tab == 7:
    st.title("💌 My Love Letter to You 💌")
    letter = """
    My Dearest [Her Name],

    From the moment I first saw you, I knew there was something special about you. Your smile lights up my world like the sun breaking through the clouds on a rainy day. Every time we talk, I feel a warmth in my heart that I can't explain. You have this incredible way of making me feel alive, cherished, and utterly happy.

    I remember our first conversation, how nervous I was, but you put me at ease with your kindness. Since then, we've shared so many beautiful moments – laughing until our sides hurt, exploring new places, and just being ourselves. You've shown me what true love feels like, and I can't imagine my life without you.

    You inspire me every day. Your strength, your intelligence, your compassion – they all amaze me. When I'm with you, time seems to stand still, and all my worries fade away. You are my rock, my confidant, and my greatest adventure.

    I love the way you see the world, with such optimism and grace. Even on tough days, you find the silver lining. You've taught me to appreciate the little things, like a shared cup of coffee or a walk in the park. With you, every ordinary moment becomes extraordinary.

    As I think about our future, I see endless possibilities. I want to be there for you through thick and thin, to support your dreams, and to create a lifetime of memories together. You mean everything to me, and I promise to love you with all my heart, forever.

    Will you be my Valentine, not just today, but every day? I love you more than words can express.

    Forever yours,
    [Your Name]

    (Word count: Approximately 250 – adjust as needed for exactly 200.)
    """
    st.write(letter)