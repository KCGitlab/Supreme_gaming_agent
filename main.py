import streamlit as st
from openai import OpenAI

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="GameMaster AI 🎮",
    page_icon="🎮",
    layout="wide"
)

# ------------------ API CLIENT ------------------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ------------------ UI HEADER ------------------
st.title("🎮 GameMaster AI – The Ultimate Gaming Agent")
st.markdown(
    """
Your virtual **AI game studio partner**  
Design game ideas, NPC behaviors, levels, stories & strategies — instantly.
"""
)

# ------------------ SIDEBAR ------------------
feature = st.sidebar.radio(
    "Select Feature",
    [
        "Game Concept Generator",
        "Level & Environment Designer",
        "NPC Behavior Designer",
        "Game Strategy Assistant",
        "Dialogue & Story Scripting"
    ]
)

user_prompt = st.text_area(
    "Enter your idea / requirement:",
    height=150,
    placeholder="Example: A fantasy RPG set in a floating sky kingdom..."
)

generate = st.button("🚀 Generate")

# ------------------ PROMPT ENGINE ------------------
def build_prompt(feature, user_input):
    base = f"You are GameMaster AI, an expert game designer and strategist.\n\n"
    
    if feature == "Game Concept Generator":
        return base + f"""
Create a unique game concept including:
- Genre
- Core gameplay loop
- Story theme
- Unique selling point

User idea:
{user_input}
"""

    if feature == "Level & Environment Designer":
        return base + f"""
Design a game level with:
- Environment description
- Player challenges
- Progression flow
- Rewards

Game context:
{user_input}
"""

    if feature == "NPC Behavior Designer":
        return base + f"""
Design NPC behavior logic including:
- NPC role
- Decision rules
- Emotional reactions
- Pseudo-code style behavior tree

Game context:
{user_input}
"""

    if feature == "Game Strategy Assistant":
        return base + f"""
Provide gameplay strategy advice including:
- Balance improvements
- Player engagement tips
- Difficulty tuning
- Retention mechanics

Game details:
{user_input}
"""

    if feature == "Dialogue & Story Scripting":
        return base + f"""
Write immersive game dialogue and story elements including:
- Characters
- Quest hooks
- Branching dialogue
- Narrative tone

Game context:
{user_input}
"""

# ------------------ OPENAI CALL ------------------
def generate_response(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a professional game design AI."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.8
    )
    return response.choices[0].message.content

# ------------------ OUTPUT ------------------
if generate:
    if not user_prompt.strip():
        st.warning("Please enter a prompt.")
    else:
        with st.spinner("GameMaster AI is thinking... 🎮"):
            final_prompt = build_prompt(feature, user_prompt)
            output = generate_response(final_prompt)

        st.subheader("🧠 AI Output")
        st.markdown(output)
