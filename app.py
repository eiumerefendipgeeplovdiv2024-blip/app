import streamlit as st

st.set_page_config(page_title="FitGenie Pro", page_icon="🦾", layout="wide")

# --- Функции за данни ---
def get_workout_schedule(training_type, days_count):
    # Дефиниране на тренировъчни планове
    schedules = {
        "Фитнес (Зала)": {
            2: [
                ("Понеделник", "Цяло тяло", ["Клек с лост", "Лежанка", "Гребане с дъмбел"]),
                ("Четвъртък", "Цяло тяло", ["Мъртва тяга", "Раменна преса", "Набирания"])
            ],
            3: [
                ("Понеделник", "Гърди и Трицепс", ["Лежанка", "Флайс", "Разгъване за трицепс"]),
                ("Сряда", "Гръб и Бицепс", ["Набирания", "Гребане с лост", "Сгъване за бицепс"]),
                ("Петък", "Крака и Рамена", ["Клек", "Лег преса", "Раменна преса"])
            ]
        },
        "Калистеника (Собствено тегло)": {
            2: [
                ("Вторник", "Горна част", ["Лицеви опори", "Набирания", "Кофички"]),
                ("Петък", "Долна част и Корем", ["Клекове", "Напади", "Планк"])
            ],
            3: [
                ("Понеделник", "Бутащи (Push)", ["Лицеви опори", "Дипсове", "Стойка на ръце"]),
                ("Сряда", "Дърпащи (Pull)", ["Набирания", "Австралийски набирания", "Коремно възлизане"]),
                ("Петък", "Крака", ["Български клек", "Скокове върху кутия", "Повдигане на пръсти"])
            ]
        }
    }
    
    # Връщаме плана според избора (ако няма за 4/5 дни в този пример, връщаме за 3)
    return schedules[training_type].get(days_count, schedules[training_type][3])

def get_macros(weight, goal, tdee):
    if goal == "Отслабване": target = tdee - 500
    elif goal == "Качване на мускулна маса": target = tdee + 400
    else: target = tdee
    
    protein = weight * 2  # 2г на кг тегло
    return int(target), int(protein)

# --- Интерфейс ---
st.title("🦾 Твоят Седмичен Фитнес Инструктор")

with st.sidebar:
    st.header("👤 Профил")
    weight = st.number_input("Тегло (кг)", 40, 150, 80)
    height = st.number_input("Височина (см)", 140, 220, 180)
    age = st.number_input("Възраст", 15, 80, 30)
    goal = st.selectbox("Цел", ["Отслабване", "Поддържане", "Качване на мускулна маса"])
    
    st.divider()
    st.header("🏋️ Тренировъчни предпочитания")
    train_type = st.radio("Тип тренировка:", ["Фитнес (Зала)", "Калистеника (Собствено тегло)"])
    days = st.select_slider("Брой тренировки в седмицата", options=[2, 3])

# Изчисления
bmr = 10 * weight + 6.25 * height - 5 * age + 5
tdee = bmr * 1.4
calories, protein = get_macros(weight, goal, tdee)

# --- Основно съдържание ---
col_diet, col_workout = st.columns([1, 2])

with col_diet:
    st.subheader("🍎 Диета и Макроси")
    st.metric("Дневни калории", f"{calories} kcal")
    st.write(f"🎯 **Протеин:** {protein}г")
    st.write(f"🍞 **Въглехидрати:** {int(calories*0.4/4)}г")
    st.write(f"🥑 **Мазнини:** {int(calories*0.25/9)}г")
    
    st.info("💡 Пий поне 3 литра вода на ден.")

with col_workout:
    st.subheader(f"📅 Седмичен график: {train_type}")
    
    schedule = get_workout_schedule(train_type, days)
    
    for day, muscles, exercises in schedule:
        with st.expander(f"🗓️ {day} - {muscles}", expanded=True):
            st.write("**Фокус върху:** " + muscles)
            cols = st.columns(len(exercises))
            for i, ex in enumerate(exercises):
                cols[i].markdown(f"✅ **{ex}**\n\n 3 серии x 10")

st.success("🔥 Готов си за действие! Консултирай се с лекар преди започване на нов режим.")
