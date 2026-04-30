import streamlit as st

st.set_page_config(page_title="FitGenie Pro", page_icon="🦾", layout="wide")

# --- Функции за данни ---
def get_workout_schedule(training_type, days_count):
    # Базови тренировки
    base_exercises = {
        "Фитнес (Зала)": [
            ("Гърди", ["Лежанка", "Флайс"]),
            ("Гръб", ["Набирания", "Гребане с лост"]),
            ("Крака", ["Клек", "Лег преса"]),
            ("Рамена", ["Раменна преса", "Разтваряне встрани"]),
            ("Ръце", ["Сгъване за бицепс", "Разгъване за трицепс"]),
            ("Кардио/Корем", ["Пътека", "Повдигане на крака"]),
            ("Мобилност", ["Стречинг", "Йога пози"])
        ],
        "Калистеника (Собствено тегло)": [
            ("Push", ["Лицеви опори", "Дипсове"]),
            ("Pull", ["Набирания", "Австралийски набирания"]),
            ("Legs", ["Български клек", "Напади"]),
            ("Core", ["Планк", "L-sit"]),
            ("Skills", ["Стойка на ръце", "Опит за Muscle up"]),
            ("Cardio", ["Бърпита", "Скачане на въже"]),
            ("Active Recovery", ["Дълго ходене", "Леки разтягания"])
        ]
    }
    
    days_names = ["Понеделник", "Вторник", "Сряда", "Четвъртък", "Петък", "Събота", "Неделя"]
    
    # Генерираме график според избрания брой дни
    current_exercises = base_exercises[training_type]
    schedule = []
    
    for i in range(days_count):
        day_name = days_names[i]
        muscle_group, ex_list = current_exercises[i % len(current_exercises)]
        schedule.append((day_name, muscle_group, ex_list))
        
    return schedule

def get_macros(weight, goal, tdee):
    if goal == "Отслабване": target = tdee - 500
    elif goal == "Качване на мускулна маса": target = tdee + 400
    else: target = tdee
    
    protein = weight * 2
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
    st.header("🏋️ Настройки")
    train_type = st.radio("Тип тренировка:", ["Фитнес (Зала)", "Калистеника (Собствено тегло)"])
    # ПРОМЯНА: Слайдерът вече е от 1 до 7
    days = st.slider("Брой тренировки в седмицата", 1, 7, 3)

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
    st.subheader(f"📅 График за {days} дни: {train_type}")
    
    schedule = get_workout_schedule(train_type, days)
    
    for day, muscles, exercises in schedule:
        with st.expander(f"🗓️ {day} - {muscles}"):
            st.write(f"**Фокус:** {muscles}")
            cols = st.columns(len(exercises))
            for i, ex in enumerate(exercises):
                cols[i].markdown(f"✅ **{ex}**\n\n 3 серии x 12")

st.success("🔥 Готов си за действие! Консултирай се с лекар преди започване на нов режим.")
