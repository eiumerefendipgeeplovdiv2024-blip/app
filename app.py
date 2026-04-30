
       import streamlit as st

# Настройка на страницата
st.set_page_config(page_title="FitGenie", page_icon="⚡", layout="wide")

def get_diet_details(goal, calories):
    if goal == "Отслабване":
        return ["Овесени ядки с горски плодове", "Пилешка салата с авокадо", "Печена риба със зеленчуци"]
    elif goal == "Качване на мускулна маса":
        return ["Яйца с пълнозърнест хляб", "Ориз с телешко и броколи", "Протеинов шейк с банан и фъстъчено масло"]
    else:
        return ["Кисело мляко с гранола", "Пуешки сандвич", "Паста със зехтин и пармезан"]

def get_workout_details(days):
    workouts = {
        2: {"Тип": "Full Body", "Упражнения": ["Клек", "Лицеви опори", "Мъртва тяга", "Планк"]},
        3: {"Тип": "Push/Pull/Legs", "Упражнения": ["Бенч преса", "Набирания", "Напади", "Раменна преса"]},
        4: {"Тип": "Upper/Lower Split", "Упражнения": ["Гребане с дъмбел", "Лег преса", "Бицепсово сгъване", "Кофички"]},
        5: {"Тип": "Body Part Split", "Упражнения": ["Изолиращи упражнения за всяка група", "Кардио сесии"]}
    }
    return workouts.get(days, workouts[3])

# --- Интерфейс ---
st.title("🏋️‍♂️ FitGenie: Твоят План за Трансформация")
st.markdown("---")

# Странична лента за входни данни
with st.sidebar:
    st.header("📋 Лични данни")
    weight = st.number_input("Тегло (кг)", min_value=40, max_value=200, value=75)
    height = st.number_input("Височина (см)", min_value=120, max_value=230, value=175)
    age = st.number_input("Възраст", min_value=15, max_value=90, value=25)
    gender = st.selectbox("Пол", ["Мъж", "Жена"])
    goal = st.selectbox("Цел", ["Отслабване", "Поддържане", "Качване на мускулна маса"])
    activity = st.select_slider("Активност", options=["Ниска", "Умерена", "Висока"])
    days = st.slider("Тренировки в седмицата", 2, 5, 3)

# Логика за изчисления (Mifflin-St Jeor)
if gender == "Мъж":
    bmr = 10 * weight + 6.25 * height - 5 * age + 5
else:
    bmr = 10 * weight + 6.25 * height - 5 * age - 161

act_mult = {"Ниска": 1.2, "Умерена": 1.55, "Висока": 1.725}
tdee = int(bmr * act_mult[activity])

if goal == "Отслабване":
    target_cals = tdee - 500
elif goal == "Качване на мускулна маса":
    target_cals = tdee + 300
else:
    target_cals = tdee

# --- Показване на резултатите ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("🥗 Хранителен План")
    st.info(f"Твоят дневен калориен прием: **{target_cals} kcal**")
    
    meals = get_diet_details(goal, target_cals)
    st.write("**Примерно меню за деня:**")
    for meal in meals:
        st.markdown(f"- {meal}")
    
    # Примерно разпределение на макроси
    st.write("---")
    st.write(f"🧬 Протеини: {int(weight * 2)}г | Въглехидрати: {int(target_cals * 0.4 / 4)}г | Мазнини: {int(target_cals * 0.25 / 9)}г")

with col2:
    st.subheader("💪 Тренировъчна Програма")
    workout_data = get_workout_details(days)
    st.success(f"Тип програма: **{workout_data['Тип']}**")
    
    st.write("**Основни упражнения:**")
    for ex in workout_data['Упражнения']:
        st.markdown(f"✅ {ex} (3 серии x 10-12 повторения)")
    
    st.warning("💡 Съвет: Винаги загрявай 5-10 минути преди начало!")

st.markdown("---")
st.caption("Забележка: Този план е генериран автоматично. Консултирайте се със специалист преди големи промени в режима.")
