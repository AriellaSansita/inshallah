import streamlit as st
import random
from datetime import datetime
import matplotlib.pyplot as plt

# -----------------------
# Constants
# -----------------------
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

# -----------------------
# Session State
# -----------------------
if "phase" not in st.session_state: st.session_state.phase = 1
if "age_group" not in st.session_state: st.session_state.age_group = None
if "goal" not in st.session_state: st.session_state.goal = 0
if "total" not in st.session_state: st.session_state.total = 0
if "custom_amount" not in st.session_state: st.session_state.custom_amount = 0
if "history" not in st.session_state: st.session_state.history = []   # NEW
if "show_tips" not in st.session_state: st.session_state.show_tips = True

# --- NEW: Stable tip ---
def get_stable_tip():
    index = datetime.now().toordinal() % len(HYDRATION_TIPS)
    return HYDRATION_TIPS[index]

# --- NEW: Add water with timestamp ---
def add_log(amount):
    if amount > 0:
        st.session_state.total += amount
        time = datetime.now().strftime("%H:%M:%S")
        cumulative = st.session_state.total
        st.session_state.history.append((time, amount, cumulative))

# -----------------------
# Navigation
# -----------------------
def start_app(): st.session_state.phase = 2
def select_age(group, ml):
    st.session_state.age_group = group
    st.session_state.goal = ml
    st.session_state.phase = 3
def continue_to_dashboard(): st.session_state.phase = 4
def view_summary(): st.session_state.phase = 5
def back_to_dashboard(): st.session_state.phase = 4

def reset_day():
    st.session_state.total = 0
    st.session_state.history = []

# --- NEW: Reset all (age + goal + totals) ---
def reset_all():
    st.session_state.total = 0
    st.session_state.history = []
    st.session_state.goal = 0
    st.session_state.age_group = None
    st.session_state.phase = 1

# -----------------------
# PHASE 1 — Welcome
# -----------------------
if st.session_state.phase == 1:
    st.title("Welcome to WaterBuddy")
    st.write("Your friendly hydration companion.")
    st.button("Let's begin", on_click=start_app)

# -----------------------
# PHASE 2 — Age Selection
# -----------------------
elif st.session_state.phase == 2:
    st.header("Select your age group")
    for group, ml in AGE_GROUPS.items():
        st.button(group, on_click=select_age, args=(group, ml))

# -----------------------
# PHASE 3 — Adjust Goal
# -----------------------
elif st.session_state.phase == 3:
    st.header("Adjust your daily goal")
    st.write(f"Recommended goal: {AGE_GROUPS[st.session_state.age_group]} ml")

    st.session_state.goal = st.number_input(
        "Daily water goal (ml):",
        min_value=500,
        max_value=10000,
        value=st.session_state.goal,
        step=100,
    )
    st.button("Continue", on_click=continue_to_dashboard)

# -----------------------
# PHASE 4 — Dashboard
# -----------------------
elif st.session_state.phase == 4:
    st.title("WaterBuddy Dashboard")
    st.write(f"### Age group: {st.session_state.age_group}")
    st.write(f"### Daily goal: **{st.session_state.goal} ml**")

    st.write("## 💧 Quick Add")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("+250 ml"): add_log(250)
    with col2:
        if st.button("+500 ml"): add_log(500)
    with col3:
        if st.button("+750 ml"): add_log(750)
    with col4:
        if st.button("+1000 ml"): add_log(1000)

    st.write("### ✏️ Add custom amount")
    custom = st.number_input("Enter amount (ml):", min_value=0, step=50, value=0)
    if st.button("Add"):
        add_log(custom)

    # --- NEW: Progress ---
    total = st.session_state.total
    goal = st.session_state.goal
    progress = min(total / goal, 1.0)

    st.write("### 📊 Progress")
    st.progress(progress)
    st.write(f"Total: **{total} ml**")
    st.write(f"Remaining: **{goal - total} ml**")
    st.write(f"Progress: **{progress*100:.1f}%**")

    # --- NEW: Comparison to recommended goal ---
    st.write(f"Compared to standard for your age: **{(total/AGE_GROUPS[st.session_state.age_group])*100:.1f}%**")

    # Mascot
    if progress == 0:
        st.info("Let's start hydrating! 🙂")
    elif progress < 0.5:
        st.info("Good start! Keep going 😄")
    elif progress < 0.75:
        st.success("Nice progress! 😎")
    elif progress < 1:
        st.success("Almost there! 🤗")
    else:
        st.balloons()
        st.success("Goal achieved! 🎉")

    # --- NEW: Tip of the day ---
    st.write("---")
    st.write("💡 Tip of the day:")
    st.write(get_stable_tip())

    # Buttons
    colA, colB, colC = st.columns(3)
    with colA:
        st.button("New Day", on_click=reset_day)
    with colB:
        st.button("Summary", on_click=view_summary)
    with colC:
        st.button("Reset All", on_click=reset_all)

    # --- NEW: History ---
    st.write("### ⏱ Today's Log")
    if st.session_state.history:
        for t, amt, cum in st.session_state.history[-7:]:
            st.write(f"{t} — +{amt} ml (total: {cum} ml)")
    else:
        st.write("No entries yet.")

# -----------------------
# PHASE 5 — Summary
# -----------------------
elif st.session_state.phase == 5:
    st.title("🌙 End-of-Day Summary")
    total = st.session_state.total
    goal = st.session_state.goal
    progress = min(total / goal, 1)

    st.write(f"Total intake: **{total} ml**")
    st.write(f"Progress: **{progress*100:.1f}%**")

    if total >= goal:
        st.success("Goal achieved! 🌟")
    else:
        st.info("Keep trying tomorrow!")

    # --- NEW: Chart ---
    if st.session_state.history:
        times = [h[0] for h in st.session_state.history]
        totals = [h[2] for h in st.session_state.history]

        fig, ax = plt.subplots(figsize=(6,3))
        ax.plot(times, totals, marker="o")
        ax.set_ylabel("Total ml")
        ax.set_xlabel("Time")
        ax.set_title("Today's Hydration Progress")
        plt.xticks(rotation=30)
        st.pyplot(fig)
    else:
        st.write("No logs available.")

    st.button("Back to Dashboard", on_click=back_to_dashboard)

