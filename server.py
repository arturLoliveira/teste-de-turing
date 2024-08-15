import socket
import threading
import time
import requests
import json 

# Configurações do servidor
HOST = 'localhost'
PORT = 123

# Chave da API (substituir pela chave real)
API_KEY = '3a2166e909msh01eaf93ed5b99edp1eedd6jsndf82fcc73493'
API_HOST = 'chatgpt-42.p.rapidapi.com'
API_URL = f'https://{API_HOST}/chatgpt'

# Função para acessar a IA generativa via API
def get_ai_response(question):
    headers = {
        'Content-Type': 'application/json',
        'x-rapidapi-host': API_HOST,
        'x-rapidapi-key': API_KEY
    }
    payload = {
	    "messages": [
		    {
			    "role": "user",
			    "content": question
		    }
	    ],
	    "web_access": False
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Verifica se houve algum erro na resposta
        result_data = response.json()
        print("Resposta da API:", result_data)
        if 'result' in result_data:
            result_final = result_data['result'].strip()
            return result_final
        else:
            return "Resposta inesperada da API: estrutura de dados desconhecida"
    except (requests.RequestException, KeyError, IndexError) as e:
        print(f"Erro ao obter resposta da IA: {e}")
        return "Desculpe, não foi possível obter uma resposta da IA no momento."

# Função para salvar o histórico
def save_history(history, ranking):
    with open('history.json', 'w') as file:
        json.dump(history, file)
    with open('ranking.json', 'w') as file:
        json.dump(ranking, file)

# Função para carregar o histórico
def load_data():
    try:
        with open('history.json', 'r') as file:
            history = json.load(file)
    except FileNotFoundError:
        history = []

    try:
        with open('ranking.json', 'r') as file:
            ranking = json.load(file)
    except FileNotFoundError:
        ranking = {}

    return history, ranking

history, ranking = load_data()

# Função que lida com cada cliente
def handle_client(client_socket, mode, delay):
    global history, ranking

    user_name = client_socket.recv(1024).decode('utf-8')
    print(f"Cliente conectado: {user_name}")
    user_history = {'name': user_name, 'questions': []}

    if user_name not in ranking:
        ranking[user_name] = {'correct': 0, 'total': 0}

    while True:
        question = client_socket.recv(1024).decode('utf-8')
        if not question:
            break
        
        print(f"Pergunta recebida: {question}")
        
        if mode == 'IA':
            response = get_ai_response(question)
            time.sleep(delay)
        else:
            response = input("Digite a resposta humana: ")

        # Envia a resposta como JSON
        response_send = {'response': response}
        client_socket.send(json.dumps(response_send).encode('utf-8'))

        guess = client_socket.recv(1024).decode('utf-8')
        correct = (guess == 'humano' and mode == 'humano') or (guess == 'IA' and mode == 'IA')
        result = 'Correto' if correct else 'Incorreto'

        # Envia o resultado como JSON
        
        client_socket.send(result.encode('utf-8'))


        user_history['questions'].append({'question': question, 'response': response, 'guess': guess, 'result': result})
        history.append(user_history)

        ranking[user_name]['total'] += 1
        if correct:
            ranking[user_name]['correct'] += 1

        save_history(history, ranking)

    client_socket.close()

# Função principal do servidor
def start_server():
    mode = input("Escolha o modo (IA/humano): ")
    delay = int(input("Tempo de espera para resposta da IA (segundos): "))

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Servidor iniciado em {HOST}:{PORT}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Conexão aceita de {addr}")

        client_handler = threading.Thread(target=handle_client, args=(client_socket, mode, delay))
        client_handler.start()

if __name__ == "__main__":
    start_server()