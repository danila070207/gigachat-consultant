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
            verify=False
        )
        if response.status_code == 200:
            token_data = response.json()
            return token_data["access_token"], datetime.now() + timedelta(seconds=token_data["expires_in"])
        else:
            # Выводим детали ошибки
            st.error(f"Ошибка получения токена: {response.status_code}")
            st.error(f"Ответ сервера: {response.text}")
            return None, None
    except Exception as e:
        st.error(f"Ошибка соединения: {e}")
        return None, None
