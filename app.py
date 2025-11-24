import streamlit as st
import random

# -------------------- CONSTANTS --------------------
AGE_GROUPS = {
    "Children (4-8 years)": 1200,
    "Teens (9-13 years)": 1700,
    "Adults (14-64 years)": 2200,
    "Seniors (65+ years)": 1800,
}

HYDRATION_TIPS = [
    "Try drinking a glass of water before meals.",
    "Keep a bottle on your desk as a reminder.",
    "Start your morning with a glass of water.",
    "Set small goals: one cup every hour.",
    "Hydrate after exercise to recover faster."
]

# -------------------- SESSION STATE --------------------
if "phase" not in st.session_state:
    st.session_state.phase = 1
if "age_group" not in st.session_state:
    st.session_state.age_group = None
if "goal" not in st.session_state:
    st.session_state.goal = 0
if "total" not in st.session_state:
    st.session_state.total = 0
if "show_tips" not in st.session_state:
    st.session_state.show_tips = True
if "mascot_on" not in st.session_state:
    st.session_state.mascot_on = True

# -------------------- GLOBAL STYLE --------------------
st.markdown("""
    <style>
    body {
        background: linear-gradient(to right, #4FD1C5, #60A5FA);
    }
    .stButton>button {
        background-color: #60A5FA;
        color: white;
        border-radius: 12px;
        font-size: 18px;
        padding: 10px 20px;
    }
    .stButton>button:hover {
        background-color: #2563EB;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# -------------------- PHASE 1 --------------------
if st.session_state.phase == 1:
    st.title("💧 Welcome to WaterBuddy")
    st.write("Your friendly daily hydration companion.")

    if st.button("Let's begin 💧", key="start_btn"):
        st.session_state.phase = 2

# -------------------- PHASE 2 --------------------
elif st.session_state.phase == 2:
    st.header("Step 1: Select your age group")

    for group, ml in AGE_GROUPS.items():
        if st.button(group, key=f"age_{group}"):
            st.session_state.age_group = group
            st.session_state.goal = ml
            st.session_state.phase = 3

# -------------------- PHASE 3 --------------------
elif st.session_state.phase == 3:
    st.header("Step 2: Confirm or adjust your daily goal")

    st.write(
        f"Recommended goal for **{st.session_state.age_group}**: "
        f"{AGE_GROUPS[st.session_state.age_group]} ml"
    )

    st.session_state.goal = st.number_input(
        "Your daily water goal (ml):",
        min_value=500,
        max_value=4000,
        value=AGE_GROUPS[st.session_state.age_group],
        step=100,
        key="goal_input"
    )

    if st.button("Continue ➡️", key="continue_btn"):
        st.session_state.phase = 4

# -------------------- PHASE 4 (MAIN DASHBOARD) --------------------
elif st.session_state.phase == 4:
    st.title("📊 WaterBuddy Dashboard")

    st.write(f"**Age group:** {st.session_state.age_group}")
    st.write(f"**Daily goal:** {st.session_state.goal} ml")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("+250 ml", key="add250_btn"):
            st.session_state.total += 250

    with col2:
        manual_amount = st.number_input("Log custom amount (ml):",
                                        min_value=0,
                                        step=50,
                                        key="manual_input")
        if st.button("Add custom amount", key="add_custom"):
            st.session_state.total += manual_amount

    if st.button("🔄 New Day (Reset)", key="reset_btn"):
        st.session_state.total = 0

    # Progress
    remaining = max(st.session_state.goal - st.session_state.total, 0)
    progress = min(st.session_state.total / st.session_state.goal, 1.0)

    st.progress(progress)
    st.write(f"**Total intake so far:** {st.session_state.total} ml")
    st.write(f"**Remaining to goal:** {remaining} ml")
    st.write(f"**Progress:** {progress*100:.1f}%")

    # Mascot messages
    if st.session_state.mascot_on:
        if progress == 0:
            st.info("Let's start hydrating! 🚰🙂")
        elif progress < 0.5:
            st.info("Good start! Keep sipping 💦😃")
        elif progress < 0.75:
            st.success("Nice! You're halfway there 😎")
        elif progress < 1.0:
            st.success("Almost at your goal! 🌊🤗")
        else:
            st.balloons()
            st.success("🎉 Congratulations! You hit your hydration goal! 🥳")

    # Tips
    if st.session_state.show_tips:
        st.write("---")
        st.write("💡 Tip of the day:")
        st.write(random.choice(HYDRATION_TIPS))
