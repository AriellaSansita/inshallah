import streamlit as st
import random

# -------------------------------
# Hydration recommendations by age group (ml)
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

# -------------------------------
# Initialize session state
ss = st.session_state
ss.setdefault("phase", 1)
ss.setdefault("age_group", None)
ss.setdefault("goal", 0)
ss.setdefault("total", 0)
ss.setdefault("log_pref", "quick")
ss.setdefault("show_tips", True)
ss.setdefault("mascot_on", True)

# -------------------------------
# Page config
st.set_page_config(page_title="WaterBuddy", page_icon="💧", layout="centered")

# -------------------------------
# Global CSS
st.markdown("""
<style>
:root{
  --bg1:#eef7ff;
  --bg2:#f9f1ff;
  --card:#ffffff;
  --primary:#1d9bf0;
  --primaryDark:#1778c8;
  --teal:#3dd1c8;
  --purple:#a78bfa;
  --pink:#f472b6;
  --green:#10b981;
  --border:#e6e9ee;
  --text:#0f172a;
  --muted:#64748b;
}

html, body, [data-testid="stAppViewContainer"]{
  background: linear-gradient(180deg, #e8f6ff 0%, #fdf2ff 100%);
}

[data-testid="stHeader"]{display:none;}

.main-container{
  padding: 16px 0 40px 0;
}

.card{
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 18px;
  box-shadow: 0 6px 24px rgba(31,38,135,0.08);
  padding: 22px;
  margin: 12px 0;
}

.card-soft{
  background: linear-gradient(180deg, #fffafc 0%, #f2fbff 100%);
  border: 1px solid #eaeaea;
  border-radius: 22px;
  box-shadow: 0 10px 30px rgba(31,38,135,0.1);
  padding: 28px;
  margin: 16px 0;
}

.h1{
  font-weight: 800;
  font-size: 28px;
  text-align:center;
  color: var(--text);
  margin-bottom: 6px;
}
.h2{
  font-weight: 700;
  font-size: 20px;
  color: var(--text);
  margin-bottom: 10px;
}
.sub{
  text-align:center;
  color: var(--muted);
  margin-bottom: 14px;
}

.badge{
  display:inline-block;
  background: #eaf6ff;
  color: var(--primaryDark);
  border-radius: 999px;
  padding: 6px 12px;
  font-size: 13px;
  font-weight: 600;
}

.row{
  display:flex; gap:12px; flex-wrap:wrap;
}
.tile{
  flex:1 1 140px;
  min-width:150px;
  background: linear-gradient(135deg, #13c1d7 0%, #6c5efb 100%);
  color: white;
  border-radius: 16px;
  padding: 14px;
  text-align:center;
  cursor:pointer;
  box-shadow: 0 6px 16px rgba(0,0,0,0.08);
}
.tile > .label{
  font-weight:700; font-size:16px;
}
.tile > .desc{
  font-size:13px; opacity:0.86;
}

.tile.alt{
  background: linear-gradient(135deg, #22c55e 0%, #06b6d4 100%);
}
.tile.alt2{
  background: linear-gradient(135deg, #f43f5e 0%, #9333ea 100%);
}

.cta-row{
  display:flex; gap:12px; flex-wrap:wrap; margin-top:8px;
}
.btn{
  flex:1 1 160px; min-width:160px;
  border:none; border-radius:999px; padding:12px 18px;
  font-weight:700; font-size:15px; cursor:pointer;
}
.btn-outline{
  background:#fff; color:#0f172a; border:1px solid var(--border);
}
.btn-grad{
  color:white;
  background: linear-gradient(90deg, #3dd1c8 0%, #a78bfa 50%, #f472b6 100%);
}

.notice{
  background:#e9f5ff; border:1px solid #dbeafe;
  color:#0ea5e9; border-radius:12px; padding:12px; text-align:center;
  margin:14px 0;
}

.progress-label{
  text-align:center; color:var(--muted); font-size:14px; margin-bottom:6px;
}

.age-card{
  border: 2px solid transparent;
  background:#fff; border-radius:18px; padding:16px; margin-bottom:12px;
  box-shadow: 0 6px 18px rgba(40, 90, 170, 0.07);
}
.age-card.blue{ border-color:#8ecaff; background: #f4fbff; }
.age-card.pink{ border-color:#ff9ecb; background: #fff5f8; }
.age-card.green{ border-color:#8ee3bc; background: #f5fff9; }
.age-card.violet{ border-color:#c9a9ff; background: #fbf8ff; }

.age-title{ font-weight:700; color:#0f172a; }
.age-sub{ color:#64748b; margin-top:4px; }

.center{ display:flex; align-items:center; justify-content:center; }
.small{ font-size:13px; color:#64748b; text-align:center; }
</style>
""", unsafe_allow_html=True)

# -------------------------------
# Helper UI functions
def headline(title, subtitle=None, emoji=None):
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown(f'<div class="h1">{emoji or ""} {title}</div>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<div class="sub">{subtitle}</div>', unsafe_allow_html=True)

def info_badge(text):
    st.markdown(f'<span class="badge">{text}</span>', unsafe_allow_html=True)

def card_start(soft=False):
    st.markdown(f'<div class="{"card-soft" if soft else "card"}">', unsafe_allow_html=True)

def card_end():
    st.markdown('</div>', unsafe_allow_html=True)

def cup_text(ml):
    cups = ml/250
    return f"{ml} ml ({int(cups)} cups)" if ml % 250 == 0 else f"{ml} ml (~{cups:.1f} cups)"

# -------------------------------
# Phase 1: Welcome
if ss.phase == 1:
    headline("Welcome to WaterBuddy", "Your friendly daily hydration companion.", "💧")
    card_start(soft=True)
    st.write("Set your age group to get a recommended daily goal, then log water with quick-add tiles or a custom amount.")
    info_badge("Tip: 1 cup ≈ 250 ml")
    st.write("")
    proceed = st.button("Let's begin 💧", key="begin", use_container_width=True)
    card_end()
    if proceed:
        ss.phase = 2

# -------------------------------
# Phase 2: Age selection
elif ss.phase == 2:
    headline("Select Your Age Group", None, "👤")

    # Age cards (visual), plus radio to actually bind the selection
    card_start()
    # Visual cards
    st.markdown('<div class="age-card blue"><div class="age-title">Children (4–8 years)</div><div class="age-sub">Daily goal: 1200 ml/day (4–5 cups)</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="age-card pink"><div class="age-title">Teens (9–13 years)</div><div class="age-sub">Daily goal: 1700 ml/day (6–7 cups)</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="age-card green"><div class="age-title">Adults (14–64 years)</div><div class="age-sub">Daily goal: 2200 ml/day (8–9 cups)</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="age-card violet"><div class="age-title">Seniors (65+ years)</div><div class="age-sub">Daily goal: 1800 ml/day (6–7 cups)</div></div>', unsafe_allow_html=True)

    # Actual selection control
    age_choice = st.radio(
        "Choose one:",
        list(AGE_GROUPS.keys()),
        index=0 if ss.age_group is None else list(AGE_GROUPS.keys()).index(ss.age_group),
        key="age_radio"
    )
    st.markdown(f'<div class="small">Recommended: <strong>{AGE_GROUPS[age_choice]} ml/day</strong></div>', unsafe_allow_html=True)

    cont = st.button("Continue ➡️", key="age_continue", use_container_width=True)
    card_end()

    if cont:
        ss.age_group = age_choice
        ss.goal = AGE_GROUPS[age_choice]
        ss.phase = 3

# -------------------------------
# Phase 3: Goal confirmation (slider look)
elif ss.phase == 3:
    headline("Adjust your goal", f"Recommended for {ss.age_group}: {AGE_GROUPS[ss.age_group]} ml/day", "🎯")
    card_start()
    # Slider + live label
    goal = st.slider(
        "Your daily water goal (ml):",
        min_value=500, max_value=4000,
        value=AGE_GROUPS[ss.age_group], step=50,
        key="goal_slider"
    )
    ss.goal = goal
    st.markdown(f'<div class="center"><div class="badge">{ss.goal} ml</div></div>', unsafe_allow_html=True)
    cont = st.button("Continue", key="goal_continue", use_container_width=True)
    st.button("← Back to Age Groups", key="back_age", use_container_width=True)
    card_end()

    if st.session_state.get("back_age"):
        ss.phase = 2
    elif cont:
        ss.phase = 4

# -------------------------------
# Phase 4: Logging preference (single-choice visual)
elif ss.phase == 4:
    headline("Choose your logging preference", None, "⚙️")
    card_start()
    ss.log_pref = st.radio(
        "How would you like to log water?",
        ["Quick log (+250 ml)", "Custom entry"],
        index=0 if ss.log_pref == "quick" else 1,
        key="log_radio"
    )
    next_btn = st.button("Next ➡️", key="pref_continue", use_container_width=True)
    card_end()
    if next_btn:
        ss.log_pref = "quick" if "Quick log" in ss.log_pref else "custom"
        ss.phase = 5

# -------------------------------
# Phase 5: Optional settings
elif ss.phase == 5:
    headline("Personalize your experience", None, "✨")
    card_start()
    ss.show_tips = st.checkbox("Show daily hydration tips", value=ss.show_tips, key="tips_checkbox")
    ss.mascot_on = st.checkbox("Enable mascot reactions", value=ss.mascot_on, key="mascot_checkbox")
    finish = st.button("Finish setup ✅", key="finish_setup", use_container_width=True)
    card_end()
    if finish:
        ss.phase = 6

# -------------------------------
# Phase 6: Dashboard
elif ss.phase == 6:
    headline("Daily Water Goal", None, "📊")

    # Header with goal & change age group
    card_start(soft=True)
    cols = st.columns([3,1])
    with cols[0]:
        st.markdown(f'<div class="h2">Daily Water Goal</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="badge">{ss.goal} ml</div>', unsafe_allow_html=True)
    with cols[1]:
        change = st.button("Change Age Group", key="change_age")
    if change:
        ss.phase = 2

    # Progress block
    consumed = ss.total
    remaining = max(ss.goal - consumed, 0)
    progress = min(consumed / ss.goal if ss.goal else 0, 1.0)

    st.markdown(f'<div class="progress-label">{consumed} ml / {ss.goal} ml</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="progress-label">{progress*100:.0f}% Complete</div>', unsafe_allow_html=True)
    st.progress(progress)

    # Status message
    msg = ("Let's start your hydration journey! 💧"
           if progress == 0 else
           "Good start! Keep sipping 💦" if progress < 0.5 else
           "Nice! You're halfway there 😎" if progress < 0.75 else
           "Almost at your goal! 🌊" if progress < 1.0 else
           "Goal Achieved! 🥳")
    st.markdown(f'<div class="notice">{msg}</div>', unsafe_allow_html=True)

    # Quick Add tiles
    st.markdown('<div class="h2">Quick Add Water</div>', unsafe_allow_html=True)
    st.markdown('<div class="row">', unsafe_allow_html=True)

    # Use buttons styled as tiles
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("💧 250 ml", key="add250"):
            ss.total += 250
    with c2:
        if st.button("🥛 500 ml", key="add500"):
            ss.total += 500
    with c3:
        if st.button("🍹 750 ml", key="add750"):
            ss.total += 750
    with c4:
        if st.button("🫙 1 L", key="add1000"):
            ss.total += 1000

    st.markdown('</div>', unsafe_allow_html=True)

    # Custom amount
    colA, colB = st.columns([3,1])
    with colA:
        manual_amount = st.number_input("Custom amount (ml):", min_value=0, step=50, key="manual_amount")
    with colB:
        if st.button("Add", key="add_custom"):
            ss.total += manual_amount

    # Footer CTAs
    st.write("")
    colX, colY = st.columns([1,1])
    with colX:
        reset_clicked = st.button("🔄 Reset Day", key="reset_day")
    with colY:
        details_clicked = st.button("End Day Summary", key="end_day")

    card_end()

    # Celebration / summary card (when achieved or on End Day)
    if progress >= 1.0 or details_clicked:
        card_start(soft=True)
        st.markdown('<div class="h1">🎉 Congratulations!</div>', unsafe_allow_html=True)
        st.markdown('<div class="sub">You\'ve reached your daily hydration goal!</div>', unsafe_allow_html=True)

        # Three info blocks
        st.write("")
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.write(f"**Total Intake** — {cup_text(ss.total)}")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.write(f"**Goal Progress** — {int(progress*100)}% of {ss.goal} ml")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.write(f"**Status** — {'Goal Achieved! ✨' if progress >= 1.0 else 'In progress 🚶‍♀️'}")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="notice">Amazing! Your body thanks you for staying hydrated! 💙</div>', unsafe_allow_html=True)

        # CTA row
        col1, col2 = st.columns(2)
        with col1:
            st.button("View Details", key="view_details")
        with col2:
            if st.button("Start New Day", key="new_day"):
                ss.total = 0

        card_end()

    # Reset
    if reset_clicked:
        ss.total = 0

    # Tips
    if ss.show_tips:
        card_start()
        st.write("💡 Tip of the day:")
        st.write(random.choice(HYDRATION_TIPS))
        card_end()

    # Reminder footer
    st.markdown('<div class="small">Remember: Consistency is key to building healthy habits! 🦎</div>', unsafe_allow_html=True)


"""
import streamlit as st
import random

# -------------------------------
# Hydration recommendations by age group (ml)
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

# -------------------------------
# Initialize session state
if "phase" not in st.session_state:
    st.session_state.phase = 1
if "age_group" not in st.session_state:
    st.session_state.age_group = None
if "goal" not in st.session_state:
    st.session_state.goal = 0
if "total" not in st.session_state:
    st.session_state.total = 0
if "log_pref" not in st.session_state:
    st.session_state.log_pref = "quick"
if "show_tips" not in st.session_state:
    st.session_state.show_tips = True
if "mascot_on" not in st.session_state:
    st.session_state.mascot_on = True

# -------------------------------
# Custom CSS for colorful background & buttons
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

# -------------------------------
# Phase 1: Welcome
if st.session_state.phase == 1:
    st.title("💧 Welcome to WaterBuddy")
    st.write("Your friendly daily hydration companion.")
    if st.button("Let's begin 💧"):
        st.session_state.phase = 2

# -------------------------------
# Phase 2: Age selection
elif st.session_state.phase == 2:
    st.header("Step 1: Select your age group")
    for group, ml in AGE_GROUPS.items():
        if st.button(group):
            st.session_state.age_group = group
            st.session_state.goal = ml
            st.session_state.phase = 3

# -------------------------------
# Phase 3: Goal confirmation
elif st.session_state.phase == 3:
    st.header("Step 2: Confirm or adjust your daily goal")
    st.write(f"Recommended goal for {st.session_state.age_group}: {AGE_GROUPS[st.session_state.age_group]} ml")
    st.session_state.goal = st.number_input(
        "Your daily water goal (ml):",
        min_value=500,
        max_value=4000,
        value=AGE_GROUPS[st.session_state.age_group],
        step=100
    )
    if st.button("Continue ➡️"):
        st.session_state.phase = 4

# -------------------------------
# Phase 4: Logging preference
elif st.session_state.phase == 4:
    st.header("Step 3: Choose your logging preference")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Quick log (+250 ml)"):
            st.session_state.log_pref = "quick"
            st.session_state.phase = 5
    with col2:
        if st.button("Custom entry"):
            st.session_state.log_pref = "custom"
            st.session_state.phase = 5

# -------------------------------
# Phase 5: Optional settings
elif st.session_state.phase == 5:
    st.header("Step 4: Personalize your experience")
    st.session_state.show_tips = st.checkbox("Show daily hydration tips", value=True)
    st.session_state.mascot_on = st.checkbox("Enable mascot reactions", value=True)
    if st.button("Finish setup ✅"):
        st.session_state.phase = 6

# -------------------------------
# Phase 6: Dashboard
elif st.session_state.phase == 6:
    st.title("📊 WaterBuddy Dashboard")
    st.write(f"**Age group:** {st.session_state.age_group}")
    st.write(f"**Daily goal:** {st.session_state.goal} ml")

    # Logging intake
    col1, col2 = st.columns(2)
    with col1:
        if st.button("+250 ml"):
            st.session_state.total += 250
    with col2:
        manual_amount = st.number_input("Log custom amount (ml):", min_value=0, step=50)
        if st.button("Add custom amount"):
            st.session_state.total += manual_amount

    # Reset
    if st.button("🔄 New Day (Reset)"):
        st.session_state.total = 0

    # Calculations
    remaining = max(st.session_state.goal - st.session_state.total, 0)
    progress = min(st.session_state.total / st.session_state.goal, 1.0)

    st.progress(progress)
    st.write(f"**Total intake so far:** {st.session_state.total} ml")
    st.write(f"**Remaining to goal:** {remaining} ml")
    st.write(f"**Progress:** {progress*100:.1f}%")

    # Motivational messages with emojis
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

"""
