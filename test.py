import requests
import json

API_KEY = 'a7f6f663c5msh1b6d147633ecf33p189430jsn964536a68f02'
API_HOST = 'open-ai21.p.rapidapi.com'
API_URL = f'https://{API_HOST}/chatgpt'

headers = {
    'Content-Type': 'application/json',
    'x-rapidapi-host': API_HOST,
    'x-rapidapi-key': API_KEY
}
payload = {
	"messages": [
		{
			"role": "user",
			"content": "hello"
		}
	],
	"web_access": False
}

try:
    response = requests.post(API_URL, headers=headers, json=payload)
    results = response.json()
    print("Resposta da API:", results)
    if 'result' in results:
        print(results['result'].strip())
    else:
        print("Resposta inesperada da API: estrutura de dados desconhecida")
except requests.RequestException as e:
    print(f"Erro ao obter resposta da IA: {e}")
