import streamlit as st

st.set_page_config(page_title="FitGenie Pro + Video", page_icon="🎬", layout="wide")

# Речник с линкове към демонстрационни видеа (YouTube)
EXERCISE_VIDEOS = {
    "Клек": "https://www.youtube.com/watch?v=gcNh17Ckjgg",
    "Лежанка": "https://www.youtube.com/watch?v=rT7DgCr-3pg",
    "Мъртва тяга": "https://www.youtube.com/watch?v=op9kVnSso6Q",
    "Набирания": "https://www.youtube.com/watch?v=eGo4IYlbE5g",
    "Лицеви опори": "https://www.youtube.com/watch?v=IODxDxX7oi4",
    "Кофички": "https://www.youtube.com/watch?v=2z8JmcrW-As",
    "Раменна преса": "https://www.youtube.com/watch?v=qEwKCR5JCog",
    "Планк": "https://www.youtube.com/watch?v=pSHjTRCQxIw",
    "Български клек": "https://www.youtube.com/watch?v=2C-uNgKwPLE"
}

def get_workout_schedule(training_type, days_count):
    # Примерна логика за разпределение на дните
    # Ако потребителят избере 7 дни, ще има и тренировки, и активна почивка
    
    base_workout = []
    days_names = ["Понеделник", "Вторник", "Сряда", "Четвъртък", "Петък", "Събота", "Неделя"]
    
    for i in range(7):
        day_name = days_names[i]
        if i < days_count:
            if training_type == "Фитнес (Зала)":
                focus = "Силова тренировка"
                exs = ["Клек", "Лежанка", "Раменна преса"] if i % 2 == 0 else ["Мъртва тяга", "Набирания", "Планк"]
            else:
                focus = "Собствено тегло"
                exs = ["Лицеви опори", "Набирания", "Планк"] if i % 2 == 0 else ["Български клек", "Кофички", "Клек"]
            base_workout.append((day_name, focus, exs))
        else:
            base_workout.append((day_name, "Почивка", ["Разтягане / Лека разходка"]))
            
    return base_workout

# --- Интерфейс ---
st.title("🎬 FitGenie: План с Видео Инструкции")

with st.sidebar:
    st.header("👤 Настройки")
    weight = st.number_input("Тегло (кг)", 40, 150, 75)
    goal = st.selectbox("Цел", ["Отслабване", "Поддържане", "Качване на мускулна маса"])
    
    st.divider()
    train_type = st.radio("Тип тренировка:", ["Фитнес (Зала)", "Калистеника (Собствено тегло)"])
    days = st.slider("Колко дни в седмицата искаш да си активен?", 1, 7, 4)

# --- Основен панел ---
st.subheader(f"📅 Твоят 7-дневен график ({train_type})")
schedule = get_workout_schedule(train_type, days)

# Показване на дните в мрежа (grid)
cols = st.columns(3) # Показваме по 3 дни на ред

for idx, (day, focus, exercises) in enumerate(schedule):
    with cols[idx % 3]:
        with st.expander(f"📍 {day}: {focus}", expanded=(focus != "Почивка")):
            if focus == "Почивка":
                st.write("😴 Време за възстановяване.")
            else:
                for ex in exercises:
                    st.write(f"**{ex}**")
                    # Проверка дали имаме видео за това упражнение
                    video_url = EXERCISE_VIDEOS.get(ex)
                    if video_url:
                        st.video(video_url)
                    st.divider()

# --- Диета (накратко) ---
st.sidebar.markdown("---")
st.sidebar.subheader("🍎 Хранене")
if goal == "Отслабване":
    st.sidebar.warning("Яж повече зеленчуци и протеини. Намали захарта.")
elif goal == "Качване на мускулна маса":
    st.sidebar.success("Увеличи приема на сложни въглехидрати и месо/бобови.")
