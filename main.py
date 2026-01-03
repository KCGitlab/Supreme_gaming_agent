import streamlit as st
from openai import OpenAI
from datetime import datetime
import os

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="GameMaster AI 🎮",
    page_icon="🎮",
    layout="wide"
)

# ------------------ API KEY CHECK ------------------
if "OPENAI_API_KEY" not in st.secrets:
    st.error("❌ OPENAI_API_KEY not found in Streamlit Secrets.")
    st.stop()

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ------------------ UI HEADER ------------------
st.title("🎮 GameMaster AI – The Ultimate Gaming Agent")
st.markdown(
    """
Your **AI Game Studio Partner**  
Concepts • Levels • NPC Logic • Strategy • Story • Avatars • Animations
"""
)

# ------------------ SIDEBAR ------------------
feature = st.sidebar.radio(
    "Select Agent Capability",
    [
        "Game Concept Generator",
        "Level & Environment Designer",
        "NPC Behavior Designer",
        "Game Strategy Assistant",
        "Dialogue & Story Scripting",
        "Avatar Creation for Games",
        "Game Animation Creation"
    ]
)

user_prompt = st.text_area(
    "Enter your idea / requirement:",
    height=160,
    placeholder="Example: A cyberpunk RPG boss character with emotional AI..."
)

generate = st.button("🚀 Generate Agent Output")

# ------------------ PROMPT ENGINE ------------------
def build_prompt(feature, user_input):
    base = "You are GameMaster AI, an expert game designer and game AI architect.\n\n"

    prompts = {
        "Game Concept Generator": f"""
Create a complete game concept including:
- Genre
- Core gameplay loop
- Story theme
- Unique mechanics
- Target audience
""",
        "Level & Environment Designer": f"""
Design a detailed game level including:
- Environment & terrain
- Player challenges
- Enemy placement
- Rewards & progression
""",
        "NPC Behavior Designer": f"""
Create NPC behavior logic including:
- NPC role
- Decision rules
- Emotional states
- Behavior tree (pseudo-code)
""",
        "Game Strategy Assistant": f"""
Analyze and improve gameplay strategy including:
- Balance fixes
- Player engagement
- Difficulty tuning
- Retention mechanics
""",
        "Dialogue & Story Scripting": f"""
Write immersive game narrative including:
- Characters
- Quests
- Branching dialogue
- Story arcs
""",
        "Avatar Creation for Games": f"""
Design a game-ready avatar including:
- Visual appearance
- Personality traits
- Outfit & accessories
- Animation style
- Game engine notes (Unity / Unreal)
""",
        "Game Animation Creation": f"""
Create animation design including:
- Animation type (idle, walk, combat, emote)
- Keyframes description
- Timing & transitions
- Engine-ready animation logic
"""
    }

    return base + prompts[feature] + f"\n\nUser Input:\n{user_input}"

# ------------------ OPENAI CALL ------------------
def generate_response(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a professional game development AI."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.8
    )
    return response.choices[0].message.content

# ------------------ FILE SAVE ------------------
def save_output(feature, content):
    os.makedirs("outputs", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"outputs/{feature.replace(' ', '_')}_{timestamp}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    return filename

# ------------------ OUTPUT ------------------
if generate:
    if not user_prompt.strip():
        st.warning("⚠️ Please enter a prompt.")
    else:
        with st.spinner("GameMaster AI is working... 🎮"):
            final_prompt = build_prompt(feature, user_prompt)
            output = generate_response(final_prompt)

        # Save file automatically
        file_path = save_output(feature, output)

        st.subheader("🧠 Agent Output")
        st.markdown(output)

        # Auto-ready download
        with open(file_path, "rb") as file:
            st.download_button(
                label="⬇️ Download Agent Output",
                data=file,
                file_name=os.path.basename(file_path),
                mime="text/plain"
            )
