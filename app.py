import streamlit as st
import random
import time

# -----------------------
# Constants & defaults
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

CUP_ML = 240  # 1 cup = 240 ml used for conversion (approx.)

# -----------------------
# Session state init
# -----------------------
if "phase" not in st.session_state:
    st.session_state.phase = 1
if "age_group" not in st.session_state:
    st.session_state.age_group = None
if "standard_goal" not in st.session_state:
    st.session_state.standard_goal = 0
if "goal" not in st.session_state:
    st.session_state.goal = 0
if "total" not in st.session_state:
    st.session_state.total = 0
if "log_unit" not in st.session_state:
    st.session_state.log_unit = "ml"  # "ml" or "cups" - the toggle requested (ml/cups) inside logging section
if "show_tips" not in st.session_state:
    st.session_state.show_tips = True
if "mascot_on" not in st.session_state:
    st.session_state.mascot_on = True
if "show_summary" not in st.session_state:
    st.session_state.show_summary = False
if "animated" not in st.session_state:
    st.session_state.animated = False

# -----------------------
# Page layout & styles
# -----------------------
st.set_page_config(page_title="WaterBuddy", layout="centered", initial_sidebar_state="auto")

st.markdown(
    """
    <style>
    .stButton>button {
        border-radius: 10px;
        padding: 8px 14px;
        font-size: 15px;
    }
    .big-btn .stButton>button {
        font-size:16px;
        padding:12px 18px;
    }
    .center {
        display: flex; justify-content: center; align-items: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------
# Helper functions
# -----------------------
def start_app():
    st.session_state.phase = 2

def select_age(group):
    st.session_state.age_group = group
    st.session_state.standard_goal = AGE_GROUPS[group]
    st.session_state.goal = AGE_GROUPS[group]
    st.session_state.phase = 3

def continue_to_dashboard():
    st.session_state.phase = 4

def add_amount_ml(amount_ml):
    st.session_state.total += int(amount_ml)

def reset_day():
    st.session_state.total = 0
    st.session_state.show_summary = False
    st.success("New day started — counters reset ✅")

def toggle_unit(unit):
    # unit comes from radio inside logging section: "ml" or "cups"
    st.session_state.log_unit = unit

def show_end_of_day_summary():
    st.session_state.show_summary = True

def animate_ascii_bottle(progress_fraction, speed=0.08):
    """
    Very simple ASCII-style water bottle animation in Streamlit.
    progress_fraction: 0.0 - 1.0
    speed: sleep time between frames
    """
    # Build frames for 10 levels (0..10)
    levels = 10
    fill_level = int(round(progress_fraction * levels))
    bottle_top = "   _______  "
    bottle_body = []
    for i in range(levels, 0, -1):
        if i <= fill_level:
            bottle_body.append("  | █████ |")
        else:
            bottle_body.append("  |       |")
    bottle_bottom = "   ‾‾‾‾‾‾‾  "
    container = st.empty()
    # animate by showing incremental fills
    for lv in range(0, fill_level + 1):
        lines = [bottle_top]
        for i in range(levels, 0, -1):
            if i <= lv:
                lines.append("  | █████ |")
            else:
                lines.append("  |       |")
        lines.append(bottle_bottom)
        container.markdown("```\n" + "\n".join(lines) + "\n```")
        time.sleep(speed)

# -----------------------
# Sidebar (settings)
# -----------------------
with st.sidebar:
    st.header("Settings")
    st.session_state.show_tips = st.checkbox("Show hydration tips", value=st.session_state.show_tips)
    st.session_state.mascot_on = st.checkbox("Show mascot", value=st.session_state.mascot_on)
    st.write("---")
    st.write("Quick links:")
    st.info("Remember to deploy to Streamlit Cloud after testing locally.")
    st.write("---")
    st.write("About")
    st.write("WaterBuddy — a simple friendly hydration tracker.")

# -----------------------
# App phases
# -----------------------
if st.session_state.phase == 1:
    st.title("Welcome to WaterBuddy 🐢")
    st.write("Your friendly daily hydration companion.")
    st.markdown("WaterBuddy suggests age-based goals and helps you log water quickly.")
    if st.button("Let's begin"):
        start_app()

elif st.session_state.phase == 2:
    st.header("Select your age group")
    for group in AGE_GROUPS:
        if st.button(group):
            select_age(group)

elif st.session_state.phase == 3:
    st.header("Adjust your daily goal")
    st.write(f"Recommended goal for **{st.session_state.age_group}**: **{st.session_state.standard_goal} ml**")
    st.session_state.goal = st.number_input(
        "Your daily water goal (ml):",
        min_value=500,
        max_value=10000,
        value=st.session_state.standard_goal,
        step=100
    )
    st.button("Continue", on_click=continue_to_dashboard)

elif st.session_state.phase == 4:
    # Dashboard
    st.title("WaterBuddy Dashboard 🐢")
    if st.session_state.mascot_on:
        # show the mascot image if available (developer will transform local path to url for deployment)
        try:
            st.image(IMAGE_PATH, caption="WaterBuddy Mascot")
        except Exception:
            # fallback: emoji mascot
            st.markdown("### 🐢")
    st.write(f"**Age group:** {st.session_state.age_group}")
    # Show Standard vs User goal
    st.write(f"**Standard recommended goal:** {st.session_state.standard_goal} ml")
    st.write(f"**Your adjusted goal:** {st.session_state.goal} ml")

    # Layout columns: left for quick add, right for manual/custom & unit toggle
    left, right = st.columns([1, 1])

    # Inside the logging section, add the ml/cups switch as requested (Option C)
    with right:
        st.subheader("Logging preferences")
        # Using a radio to act like a switch (ml <-> cups)
        unit = st.radio("Logging unit", options=["ml", "cups"], index=0 if st.session_state.log_unit == "ml" else 1, horizontal=True)
        toggle_unit(unit)
        st.write(f"Currently logging in **{st.session_state.log_unit}**")

        st.write("---")
        st.subheader("Custom add")
        col_inp1, col_inp2 = st.columns([2,1])
        with col_inp1:
            if st.session_state.log_unit == "ml":
                manual_amount = st.number_input("Custom amount", min_value=0, value=250, step=50, key="manual_ml")
                add_button_label = "Add (ml)"
            else:
                # display in cups to user, convert to ml on submit
                manual_cups = st.number_input("Custom amount (cups)", min_value=0.0, value=1.0, step=0.25, key="manual_cup")
                add_button_label = "Add (cups)"
        with col_inp2:
            if st.session_state.log_unit == "ml":
                if st.button("Add custom (ml)"):
                    add_amount_ml(manual_amount)
            else:
                if st.button("Add custom (cups)"):
                    ml_amount = int(round(manual_cups * CUP_ML))
                    add_amount_ml(ml_amount)

    with left:
        st.subheader("Quick Add Water")
        st.write("Tap a button to add instantly:")
        # Quick add options with emojis and requested amounts
        # Show amounts in user's selected unit
        def quick_add_handler(amount_ml):
            add_amount_ml(amount_ml)
        # Display as columns of buttons
        qa1, qa2 = st.columns(2)
        with qa1:
            if st.session_state.log_unit == "ml":
                if st.button("💧 250 ml"):
                    quick_add_handler(250)
            else:
                # show cups equivalent
                cups_250 = round(250 / CUP_ML, 2)
                if st.button(f"💧 {cups_250} cups"):
                    quick_add_handler(250)
            if st.session_state.log_unit == "ml":
                if st.button("🥛 500 ml"):
                    quick_add_handler(500)
            else:
                cups_500 = round(500 / CUP_ML, 2)
                if st.button(f"🥛 {cups_500} cups"):
                    quick_add_handler(500)
        with qa2:
            if st.session_state.log_unit == "ml":
                if st.button("🥤 750 ml"):
                    quick_add_handler(750)
            else:
                cups_750 = round(750 / CUP_ML, 2)
                if st.button(f"🥤 {cups_750} cups"):
                    quick_add_handler(750)
            if st.session_state.log_unit == "ml":
                if st.button("🍶 1000 ml (1 L)"):
                    quick_add_handler(1000)
            else:
                cups_1000 = round(1000 / CUP_ML, 2)
                if st.button(f"🍶 {cups_1000} cups"):
                    quick_add_handler(1000)

    st.write("---")
    # Reset / New Day
    st.button("New Day (Reset)", on_click=reset_day)

    # Calculations
    remaining = max(st.session_state.goal - st.session_state.total, 0)
    progress_frac = 0.0 if st.session_state.goal == 0 else min(st.session_state.total / st.session_state.goal, 1.0)

    # Progress visual
    st.progress(progress_frac)
    st.write(f"**Total intake so far:** {st.session_state.total} ml  ({round(st.session_state.total / CUP_ML, 2)} cups)")
    st.write(f"**Remaining to goal:** {remaining} ml  ({round(remaining / CUP_ML, 2)} cups)")
    st.write(f"**Progress:** {progress_frac*100:.1f}%")

    # Animated bottle control - user can click to animate
    col_anim_left, col_anim_right = st.columns([1, 1])
    with col_anim_left:
        if st.button("Animate water bottle"):
            # We run the simple ASCII animation showing current progress
            animate_ascii_bottle(progress_frac, speed=0.06)
    with col_anim_right:
        if st.button("Show end-of-day summary"):
            show_end_of_day_summary()

    # Mascot messages and milestone reactions
    if st.session_state.mascot_on:
        if progress_frac == 0:
            st.info("Let's start hydrating! 🙂")
        elif progress_frac < 0.5:
            st.info("Good start! Keep sipping 😃")
        elif progress_frac < 0.75:
            st.success("Nice! You're getting there 😎")
        elif progress_frac < 1.0:
            st.success("Almost at your goal! 🤗")
        else:
            st.balloons()
            st.success("🎉 Congratulations! You hit your hydration goal! 🥳")

    # Tip of the day (optional button)
    if st.session_state.show_tips:
        if st.button("Show me a hydration tip"):
            st.info(random.choice(HYDRATION_TIPS))

    # End-of-day summary popup / block
    if st.session_state.show_summary:
        # Compose summary content using the user's actual values
        st.write("---")
        st.header("End-of-Day Summary")
        st.markdown("**Great Effort!**  Keep up the good work tomorrow! 🌟")
        total_cups = round(st.session_state.total / CUP_ML, 2)
        st.write("**Total Intake**")
        st.write(f"{st.session_state.total} ml ({total_cups} cups)")
        st.write("---")
        st.write("**Goal Progress**")
        progress_pct = int(round((st.session_state.total / st.session_state.goal) * 100)) if st.session_state.goal else 0
        st.write(f"{progress_pct}% of {st.session_state.standard_goal} ml")
        st.write("---")
        st.write("**Status**")
        if st.session_state.total >= st.session_state.goal:
            st.success("Goal Achieved! 🌟")
        else:
            st.info("Goal Not Yet Achieved — you can do it tomorrow! 💪")

# -----------------------
# Deployment note
# -----------------------
# When you deploy on Streamlit Cloud, make sure IMAGE_PATH is replaced with a web-accessible URL
# or add the image file to your repo and reference it by relative path (Streamlit Cloud will host it).
# Developer requested the local path be included exactly as:
# "/mnt/data/Screenshot 2025-11-24 at 9.17.29 AM.png"
#
# Save this file as app.py and create requirements.txt with:
# streamlit
# (plus any other libraries you use)


