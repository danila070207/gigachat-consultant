import streamlit as st
import requests

st.set_page_config(page_title="Консультант предприятия", page_icon="💬")
st.title("🤖 Консультант предприятия")
st.markdown("Задайте вопрос о нашей компании")

SYSTEM_PROMPT = """
Ты — консультант компании 'Ромашка'. Компания занимается продажей цветов и комнатных растений.
Режим работы: ежедневно с 9:00 до 21:00.
Адрес: г. Москва, ул. Ленина, д. 10.
Телефон: +7 (123) 456-78-90.
Электронная почта: info@romashka.ru
Сайт: www.romashka.ru
"""

def ask_yandex_gpt(question, api_key):
    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Authorization": f"Api-Key {api_key}",
        "Content-Type": "application/json"
    }
    prompt = SYSTEM_PROMPT + f"\nВопрос пользователя: {question}\nОтвет:"
    data = {
        "model": "yandexgpt-lite",
        "messages": [{"role": "user", "text": prompt}],
        "temperature": 0.6,
        "maxTokens": 500
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["result"]["message"]["text"]
    else:
        st.error(f"Ошибка API: {response.text}")
        return None

question = st.text_input("Ваш вопрос:", placeholder="Например: какой у вас график работы?")
if st.button("Спросить"):
    if question:
        with st.spinner("Думаю..."):
            api_key = st.secrets["YANDEX_API_KEY"]
            answer = ask_yandex_gpt(question, api_key)
            if answer:
                st.success("Ответ:")
                st.write(answer)
    else:
        st.warning("Введите вопрос.")
