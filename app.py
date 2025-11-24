elif st.session_state.phase == 4:
    st.title("WaterBuddy Dashboard")

    st.markdown(f"### Age group: **{st.session_state.age_group}**")
    st.markdown(f"### Daily goal: **{st.session_state.goal} ml**")

    st.write("")

    # ------------------------------------------------------
    #   1) QUICK ADD BUTTONS
    # ------------------------------------------------------
    st.markdown("## 💧 Quick Add Water")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("💧 250 ml"):
            st.session_state.total += 250
    with col2:
        if st.button("🥛 500 ml"):
            st.session_state.total += 500
    with col3:
        if st.button("🥤 750 ml"):
            st.session_state.total += 750
    with col4:
        if st.button("🍶 1 L"):
            st.session_state.total += 1000

    st.write("")

    # ------------------------------------------------------
    #   2) CUSTOM ADD
    # ------------------------------------------------------
    st.markdown("### ✏️ Add a custom amount")

    custom = st.number_input("Enter amount (ml):", min_value=0, step=50)
    if st.button("Add"):
        st.session_state.total += custom

    st.write("")

    # ------------------------------------------------------
    #   3) PROGRESS BAR & STATS
    # ------------------------------------------------------
    total = st.session_state.total
    goal = st.session_state.goal

    if goal > 0:
        progress = min(total / goal, 1.0)
    else:
        progress = 0

    st.markdown("### 📊 Progress")
    st.progress(progress)

    remaining = max(goal - total, 0)

    st.write(f"**Total intake so far:** {total} ml")
    st.write(f"**Remaining to goal:** {remaining} ml")
    st.write(f"**Progress:** {progress*100:.1f}%")

    st.write("")

    # ------------------------------------------------------
    #   4) MASCOT
    # ------------------------------------------------------
    if st.session_state.mascot_on:
        if progress == 0:
            st.info("Let's start hydrating! 🙂")
        elif progress < 0.5:
            st.info("Good start! Keep sipping 😃")
        elif progress < 0.75:
            st.success("Nice! You're halfway there 😎")
        elif progress < 1.0:
            st.success("Almost at your goal! 🤗")
        else:
            st.balloons()
            st.success("🎉 Congratulations! You hit your hydration goal! 🥳")

    st.write("")

    # ------------------------------------------------------
    #   5) RESET BUTTON (now AFTER mascot)
    # ------------------------------------------------------
    st.button("New Day (Reset)", on_click=reset_day)

    st.write("")

    # ------------------------------------------------------
    #   6) TIP OF THE DAY (always last)
    # ------------------------------------------------------
    if st.session_state.show_tips:
        st.write("---")
        st.write("💡 Tip of the day:")
        st.write(random.choice(HYDRATION_TIPS))



