import socket
import json 

# Configurações do cliente
HOST = 'localhost'
PORT = 123

# Função principal do cliente
def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    name = input("Digite seu nome: ")
    client_socket.send(name.encode('utf-8'))

    total_questions = 0
    correct_guesses = 0
    ia_responses = 0
    human_responses = 0

    while True:
        question = input("Faça uma pergunta: ")
        client_socket.send(question.encode('utf-8'))
    
        # Recebe a resposta como JSON
        response_data = client_socket.recv(4096).decode('utf-8')
        response_json = json.loads(response_data)  # Converte a string JSON em um dicionário
        response_text = response_json.get('response', 'Erro na resposta')  # Acessa a chave 'response'
        print(f"Resposta: {response_text}")
       
        guess = input("Você acha que a resposta é de um humano ou IA? ")
        client_socket.send(guess.encode('utf-8'))

        # Recebe o resultado como JSON
        result = client_socket.recv(1024).decode('utf-8')
        print(f"Resultado: {result}")

        # Atualiza contadores
        total_questions += 1
        if result == 'Correto':
            correct_guesses += 1
        if 'IA' in response_text:
            ia_responses += 1
        else:
            human_responses += 1

        again = input("Deseja fazer outra pergunta? (s/n): ")
        if again.lower() != 's':
            break

        # Exibe o resumo
    print("\nResumo:")
    print(f"Total de perguntas: {total_questions}")
    print(f"Respostas da IA: {ia_responses}")
    print(f"Respostas de humanos: {human_responses}")
    print(f"Total de acertos: {correct_guesses}")
    print(f"Percentual de acertos: {correct_guesses / total_questions * 100:.2f}%")

    client_socket.close()

if __name__ == "__main__":
    start_client()
