def call_deepseek(prompt, system="Eres un agente de HB Jew"):
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 4096,
        "temperature": 0.7
    }

    try:
        resp = requests.post(DEEPSEEK_URL, json=payload, headers=headers, timeout=60)
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error DeepSeek: {str(e)}"
