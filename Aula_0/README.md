## 🚀 Aula 0: Controle de Hardware com Python e Arduino (UART)

Nesta aula vamos realizar a comunicação entre o computador com o Arduino pela porta USB (comunicação serial UART).

## Objetivo da aula:

Usar Python para enviar comandos ao Arduino

Ligar e desligar um LED pela porta serial

O computador passa a controlar o hardware fisicamente.

## 🛠️ Materiais Necessários

1x Arduino Uno.

1x Cabo USB.

## 💻 Parte 1 – Preparando o Arduino

Abra o arquivo aula_0.ino na Arduino IDE.

Conecte o Arduino ao computador via cabo USB.

## Selecione:
A placa correta

A porta correta (exemplo: COM3)

Clique em Upload para gravar o código.

## ⚠️ Anote a porta COM utilizada. Você precisará dela no Python.

## 🐍 Parte 2 – Preparando o Ambiente Python (Windows)

(⚠️Sugestão!!!) Vamos criar um ambiente virtual (venv) para manter as bibliotecas organizadas.

1️⃣ No terminal, acesse a pasta da aula:
```bash
cd caminho\para\Aula_0
```

2️⃣ Crie o ambiente virtual:
```bash
python -m venv venv
```

3️⃣ Ative o ambiente:
```bash
.\venv\Scripts\activate
```
(Deve aparecer (venv) no início do terminal.)

4️⃣ Instale a dependência necessária:
```bash
pip install pyserial
```

## ▶ Execução

1️⃣ Verifique se a porta no arquivo aula_0.py corresponde à porta do Arduino (ex: COM3).

2️⃣ Execute o script:
```bash
python aula_0.py
```
