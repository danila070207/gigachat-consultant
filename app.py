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
Мы предлагаем широкий ассортимент цветов: розы, тюльпаны, хризантемы, орхидеи, а также горшечные растения.
Возможна доставка по городу от 30 минут.
Отвечай на вопросы вежливо, кратко и по делу. Если вопрос не касается деятельности компании, вежливо сообщи, что можешь ответить только на вопросы о компании.
"""

def ask_yandex_gpt(question, api_key, folder_id):
    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Authorization": f"Api-Key {api_key}",
        "Content-Type": "application/json"
    }
    prompt = f"{SYSTEM_PROMPT}\n\nВопрос пользователя: {question}\nОтвет:"
    data = {
        "modelUri": f"gpt://{folder_id}/yandexgpt-lite",
        "messages": [{"role": "user", "text": prompt}],
        "temperature": 0.6,
        "maxTokens": 500
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            result = response.json()
            return result["result"]["message"]["text"]
        else:
            st.error(f"Ошибка API: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Ошибка соединения: {e}")
        return None

question = st.text_input("Ваш вопрос:", placeholder="Например: какой у вас график работы?")
if st.button("Спросить"):
    if not question:
        st.warning("Введите вопрос.")
    else:
        with st.spinner("Думаю..."):
            api_key = st.secrets["YANDEX_API_KEY"]
            folder_id = st.secrets["FOLDER_ID"]
            answer = ask_yandex_gpt(question, api_key, folder_id)
            if answer:
                st.success("Ответ:")
                st.write(answer)
