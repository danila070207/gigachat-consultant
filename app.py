import streamlit as st
import requests
import uuid
from datetime import datetime, timedelta

# Настройки страницы
st.set_page_config(page_title="Консультант предприятия", page_icon="💬")
st.title("🤖 Консультант предприятия")
st.markdown("Задайте вопрос о нашей компании")

# Системный промпт
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

# Функция получения токена GigaChat
def get_gigachat_token(client_id, client_secret):
    auth_url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
        "RqUID": str(uuid.uuid4())
    }
    data = {"scope": "GIGACHAT_API_PERS"}
    try:
        response = requests.post(
            auth_url,
            headers=headers,
            data=data,
            auth=(client_id, client_secret),
            verify=False  # для самоподписанного сертификата Сбера
        )
        if response.status_code == 200:
            token_data = response.json()
            # Сохраняем токен и время истечения (expires_at)
            return token_data["access_token"], datetime.now() + timedelta(seconds=token_data["expires_in"])
        else:
            st.error(f"Ошибка получения токена: {response.status_code}")
            return None, None
    except Exception as e:
        st.error(f"Ошибка соединения: {e}")
        return None, None

# Функция запроса к GigaChat
def ask_gigachat(question, token):
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {token}"
    }
    payload = {
        "model": "GigaChat",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question}
        ],
        "temperature": 0.7,
        "max_tokens": 1000
    }
    try:
        response = requests.post(url, headers=headers, json=payload, verify=False)
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            st.error(f"Ошибка запроса: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Ошибка соединения: {e}")
        return None

# Инициализация session_state
if "token" not in st.session_state:
    st.session_state.token = None
    st.session_state.token_expires = None

# Интерфейс
question = st.text_input("Ваш вопрос:", placeholder="Например: какой у вас график работы?")
if st.button("Спросить"):
    if not question:
        st.warning("Введите вопрос.")
    else:
        with st.spinner("Думаю..."):
            # Получаем секреты из Streamlit Cloud
            client_id = st.secrets["GIGACHAT_CLIENT_ID"]
            client_secret = st.secrets["GIGACHAT_CLIENT_SECRET"]

            # Проверяем, нужно ли получить новый токен
            if (st.session_state.token is None or
                st.session_state.token_expires is None or
                datetime.now() >= st.session_state.token_expires):
                token, expires = get_gigachat_token(client_id, client_secret)
                if token:
                    st.session_state.token = token
                    st.session_state.token_expires = expires
                else:
                    st.stop()

            answer = ask_gigachat(question, st.session_state.token)
            if answer:
                st.success("Ответ:")
                st.write(answer)
