import streamlit as st

def calculate_macros(goal, tdee):
    if goal == "Lose Weight":
        calories = tdee - 500
        protein = 1.2  # grams per lb (approx)
    elif goal == "Gain Muscle":
        calories = tdee + 300
        protein = 1.0
    else:
        calories = tdee
        protein = 0.8
    
    # Simple macro split: 30% Protein, 40% Carbs, 30% Fats
    return int(calories), int((calories * 0.3) / 4), int((calories * 0.4) / 4), int((calories * 0.3) / 9)

def get_workout(days):
    plans = {
        2: "Full Body (Day 1: Compound Lifts, Day 2: Accessory Work)",
        3: "Full Body Split (Mon/Wed/Fri)",
        4: "Upper/Lower Split (2 Upper days, 2 Lower days)",
        5: "PPL + Upper/Lower (Push, Pull, Legs, Upper, Lower)",
        6: "PPL (Push, Pull, Legs x2)"
    }
    return plans.get(days, "Full Body Routine")

# --- Streamlit UI ---
st.set_page_config(page_title="Fitness Planner", layout="centered")
st.title("🏋️‍♂️ AI Personal Trainer & Nutritionist")
st.markdown("Enter your details below to generate a custom plan.")

with st.sidebar:
    st.header("Your Stats")
    age = st.number_input("Age", min_value=15, max_value=100, value=25)
    gender = st.selectbox("Gender", ["Male", "Female"])
    weight = st.number_input("Weight (kg)", min_value=40, value=75)
    height = st.number_input("Height (cm)", min_value=120, value=175)
    activity = st.selectbox("Activity Level", ["Sedentary", "Lightly Active", "Moderately Active", "Very Active"])
    goal = st.selectbox("Goal", ["Lose Weight", "Maintain", "Gain Muscle"])
    days = st.slider("Workout days per week", 2, 6, 3)

if st.button("Generate My Plan"):
    # BMR Calculation (Mifflin-St Jeor Equation)
    if gender == "Male":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    
    # Activity Multipliers
    multipliers = {"Sedentary": 1.2, "Lightly Active": 1.375, "Moderately Active": 1.55, "Very Active": 1.725}
    tdee = bmr * multipliers[activity]
    
    calories, p, c, f = calculate_macros(goal, tdee)
    
    # --- Display Results ---
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🍎 Diet Plan")
        st.metric("Daily Calories", f"{calories} kcal")
        st.write(f"**Protein:** {p}g")
        st.write(f"**Carbs:** {c}g")
        st.write(f"**Fats:** {f}g")
        
    with col2:
        st.subheader("💪 Workout Plan")
        st.info(f"Recommended Split: **{get_workout(days)}**")
        st.write("1. Focus on progressive overload.")
        st.write("2. Prioritize compound movements.")
        st.write("3. Rest 60-90s between sets.")

    st.success("Plan generated! Remember to stay hydrated and get 7-9 hours of sleep.")
