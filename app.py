import streamlit as st

# Настройка на страницата
st.set_page_config(page_title="FitGenie Pro", page_icon="💪", layout="wide")

def get_diet_details(goal):
    if goal == "Отслабване":
        return ["Овесени ядки с горски плодове", "Пилешка салата с авокадо", "Печена риба със зеленчуци"]
    elif goal == "Качване на мускулна маса":
        return ["Яйца с пълнозърнест хляб", "Ориз с телешко и броколи", "Протеинов шейк с банан и фъстъчено масло"]
    else:
        return ["Кисело мляко с гранола", "Пуешки сандвич", "Паста със зехтин и пармезан"]

def get_workout_details(training_type, days):
    # Логика за Фитнес (Зала)
    gym_plans = {
        2: "Full Body (Клек, Лежанка, Тяга)",
        3: "Push / Pull / Legs (Бутащи, Дърпащи, Крака)",
        4: "Upper / Lower (Горна и Долна част)",
        5: "Brosplit (Гърди, Гръб, Крака, Рамена, Ръце)"
    }
    
    # Логика за Калистеника (Собствено тегло)
    cali_plans = {
        2: "Full Body Cali (Лицеви, Набирания, Клекове)",
        3: "Fundamentals (Набирания, Кофички, Напади)",
        4: "Skill + Strength (Работа за стойка на ръце + Сила)",
        5: "Advanced Flow (Комплексни движения и издръжливост)"
    }

    if training_type == "Фитнес (Зала)":
        plan = gym_plans.get(days, "Gym Routine")
        ex = ["Бенч преса", "Мъртва тяга", "Клякане с лост", "Раменна преса"]
    else:
        plan = cali_plans.get(days, "Calisthenics Routine")
        ex = ["Набирания", "Лицеви опори", "Кофички на успоредка", "Набирания с подхват"]
        
    return plan, ex

# --- Интерфейс ---
st.title("⚡ FitGenie: Твоят Персонален План")
st.markdown("Избери своите параметри и генерирай режим за секунди.")

with st.sidebar:
    st.header("⚙️ Настройки")
    weight = st.number_input("Тегло (кг)", 40, 200, 75)
    height = st.number_input("Височина (см)", 120, 230, 175)
    age = st.number_input("Възраст", 15, 90, 25)
    gender = st.selectbox("Пол", ["Мъж", "Жена"])
    goal = st.selectbox("Цел", ["Отслабване", "Поддържане", "Качване на мускулна маса"])
    
    st.write("---")
    # НОВИЯТ ИЗБОР ТУК:
    training_type = st.radio("Тип тренировки:", ["Фитнес (Зала)", "Калистеника (Собствено тегло)"])
    days = st.slider("Дни в седмицата", 2, 5, 3)

# Пресмятане на калории
bmr = (10 * weight + 6.25 * height - 5 * age + 5) if gender == "Мъж" else (10 * weight + 6.25 * height - 5 * age - 161)
tdee = int(bmr * 1.55) # Приемаме средна активност

if goal == "Отслабване": target_cals = tdee - 500
elif goal == "Качване на мускулна маса": target_cals = tdee + 300
else: target_cals = tdee

# --- Показване на резултатите ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("🥗 Хранене")
    st.info(f"Цел: **{target_cals} ккал** на ден")
    meals = get_diet_details(goal)
    for m in meals:
        st.write(f"🍴 {m}")

with col2:
    st.subheader("🏋️ Тренировка")
    plan_name, exercises = get_workout_details(training_type, days)
    st.success(f"Режим: **{plan_name}**")
    st.write(f"Тип: {training_type}")
    
    st.write("**Примерни упражнения:**")
    for e in exercises:
        st.write(f"🔹 {e}")

st.divider()
st.info("💡 **Съвет:** При калистениката се фокусирай върху правилното изпълнение, а във фитнеса - върху прогресивното натоварване с тежести.")
