# Aula sobre comunicação serial com Arduino usando Python

import serial
import time

# --- Configuração Inicial ---
# Ajuste a porta COM para a que seu Arduino está usando
PORTA = 'COM9'    
VELOCIDADE = 9600

print(f"Conectando ao Arduino na porta {PORTA}...")

try:
    # 1. Estabelece a conexão
    arduino = serial.Serial(PORTA, VELOCIDADE, timeout=1)
    time.sleep(2)  # Aguarda 2 segundos para o Arduino reiniciar a conexão
    print("Conexao estabelecida! \n")

    print("--- Comandos de Revisão ---")
    print("Digite o que deseja enviar e pressione ENTER.")
    print("Exemplos: 'L' (Liga), 'D' (Desliga)")
    print("Digite 'sair' para encerrar.\n")

    # 2. Loop Principal
    while True:
        comando = input("Enviar > ")

        if comando.lower() == 'sair':
            break

        # 3. Envia o dado para o Arduino (converte string para bytes)
        arduino.write(comando.encode('utf-8'))

        # 4. (Opcional) Lê resposta do Arduino se houver
        if arduino.in_waiting > 0:
            resposta = arduino.readline().decode('utf-8').strip()
            print(f"Arduino respondeu: {resposta}")

    arduino.close()
    print("Conexão encerrada.")

except Exception as e:
    print(f"Erro: {e}")
    print("Verifique se a porta COM está correta e o Arduino conectado.")
