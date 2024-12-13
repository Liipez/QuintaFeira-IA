import json
import os
import webbrowser  # Importa a biblioteca para abrir sites
import speech_recognition as sr  # Para reconhecimento de voz
import pyttsx3  # Para resposta de voz
import re  # Para processar expressões matemáticas
import random  # Para selecionar piadas aleatórias

# Função para falar usando voz
def falar(texto):
    engine = pyttsx3.init()
    engine.say(texto)
    engine.runAndWait()

# Função para ouvir comandos de voz
def ouvir_comando():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Diga algo...")
        try:
            audio = recognizer.listen(source)
            comando = recognizer.recognize_google(audio, language="pt-BR")
            print(f"Você disse: {comando}")
            return comando.lower()
        except sr.UnknownValueError:
            print("Não entendi o que você disse. Tente novamente.")
            return ""
        except sr.RequestError as e:
            print(f"Erro ao acessar o serviço de reconhecimento de voz: {e}")
            return ""

# Funções para carregar e salvar FAQ
def carregar_faq():
    if os.path.exists("faq.json"):
        with open("faq.json", "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return {}

def salvar_faq(faq):
    with open("faq.json", "w", encoding="utf-8") as f:
        json.dump(faq, f, ensure_ascii=False, indent=4)

# Função para treinar o bot
def treinar_bot(faq):
    print("Modo de treinamento iniciado. Diga 'sair' para sair.")
    while True:
        pergunta = input("Pergunta: ").strip()
        if pergunta.lower() == "sair":
            break
        resposta = input("Resposta: ").strip()
        if not pergunta or not resposta:
            print("Pergunta ou resposta inválida! Tente novamente.")
            continue
        faq[pergunta] = resposta
        print("Treinamento concluído!")
    salvar_faq(faq)

# Função para pesquisar no Google
def pesquisar_no_google(termo):
    if termo.strip():
        print(f"QuintaFeira: Pesquisando no Google por: {termo}")
        falar(f"Pesquisando no Google por {termo}")
        termo = termo.replace(" ", "+")  # Substituir espaços por '+'
        webbrowser.open(f"https://www.google.com/search?q={termo}")
    else:
        print("QuintaFeira: Não entendi o termo de pesquisa. Tente novamente.")
        falar("Não entendi o termo de pesquisa. Tente novamente.")

# Lista de piadas
piadas = [
    "Por que o livro de matemática ficou triste? Porque ele tinha muitos problemas!",
    "O que é um pontinho vermelho na sala? Um pimentão se escondendo.",
    "Por que o lápis não pode entrar na escola? Porque ele é muito afiado!",
    "Qual é o cúmulo da paciência? Esperar uma tartaruga atravessar a rua com uma lesma nas costas.",
    "O que é um astrônomo no espaço? Um estrelado.",
    "Por que a bicicleta caiu? Porque estava sem corrente.",
    "Como o relógio se despede? Tic-tchau!",
    "Por que os químicos são ótimos em resolver problemas? Porque eles têm todas as soluções!",
    "Por que o desenvolvedor faliu? Porque ele usou todo o seu cache.",
    "Você já ouviu falar do cara que roubou o calendário? Ele pegou 12 meses!",
    "O que ganha o melhor dentista do mundo? Uma pequena placa.",
    "Meus professores me disseram que eu nunca seria muito porque procrastino muito. Eu disse a eles: “Esperem para ver!”",
    "Minha memória ficou tão ruim que realmente me fez perder o emprego. Ainda estou empregado. Só não consigo lembrar onde.",
    "Quando em uma candidatura a emprego perguntam quem deve ser notificado em caso de emergência, sempre escrevo: “Um médico muito bom”",
    "Por que o médico está sempre calmo? Porque ele tem muitos pacientes.",
    "Por que o livro de matemática parece tão triste? Por causa de todos os seus problemas.",
    "Qual é a comida favorita de um lobisomem? Lobisomens não são reais.",
    "Como chamar um cão mágico? Um Labracadabrador.",
    "Por que os pássaros voam para climas mais quentes no inverno? É muito mais fácil do que caminhar!",
    "Seja como um próton. Sempre seja positivo.",
    "Que tipo de carro o Yoda dirige? Toyoda.",
    "O que o zero diz a um oito? Cinto legal.",
    "Quantos profissionais de marketing são necessários para arrumar uma lâmpada? Nenhum, eles já automatizaram o processo.",
    "Quer ouvir uma piada sobre o potássio? K.",
    "O que você faz quando suas piadas sobre ciência não tem graça? Continue tentando até conseguir uma reação.",
    "Por que o dinossauro atravessou a rua? Porque as galinhas ainda não existiam!",
    "O que um pato subatômico diz? Quark.",
    "O que o Oceano Atlântico disse ao Oceano Índico? “Experimente e seja mais Pacífico!”",
    "Um homem entra em uma biblioteca e pede ao bibliotecário livros sobre paranóia. O bibliotecário sussurra: “Eles estão bem atrás de você!”",
    "Por que os coalas não contam como ursos? Eles não têm as coalificações certas.",
    "Algumas pessoas comem caracóis. Eles não devem gostar de fast food.",
    "Como você chama uma pilha de gatinhos? Um meowntanha.",
    "O que fica mais úmido quanto mais seca? Uma toalha.",
    "Eu tenho uma piada sobre viagem no tempo, mas não vou contar. Vocês não gostaram.",
    "Alguém conhece uma boa piada sobre o sódio? R: Na…",
    "Como você chama o monstro mais inteligente de todos? FrankEinstein",
    "Você ouviu sobre todos os significados ocultos do Rei Leão? Sim, está cheio de simbalismo.",
    "Por que os físicos adoram o mar? Por causa das ondas.",
    "Eu tentei criar uma piada sobre o vácuo, mas era vazia demais.",
    "Um esqueleto tentou discutir comigo. Não tinha estômago para isso.",
    "Se eu conheço piadas sobre o nitrogênio e o oxigênio? NO.",
    "O que um físico faz quando está triste? Ele tenta melhorar seu estado.",
    "Por que os matemáticos não plantam flores? Porque não conseguem achar as raízes.",
    "Você ouviu sobre a planta que estudou medicina? Agora é uma planta medicinal.",
    "O que o programador disse depois de meditar? “Hello, World!”.",
    "O que o zero disse para o oito? Que cinto legal você tem!",
    "O que o teto disse para a parede? “Eu te cubro!”",
    "Por que os programadores não gostam da natureza? Muitos bugs.",
    "Qual é o animal favorito do computador? O mouse.",
    "Qual é a banda favorita dos físicos? AC/DC.",
    "O que o neurônio disse ao outro neurônio? “Você tá pensando o que eu tô pensando?”",
    "Por que o computador foi ao médico? Porque ele tinha um vírus!",
    "Como o banco de dados se declarou para a tabela? “Você é a chave primária do meu coração.”",
    "Por que o químico não conseguia resolver o enigma? Ele não tinha a solução.",
    "Qual é o café favorito do desenvolvedor? Java.",
    "O que o HTML disse ao CSS? “Eu gosto do seu estilo!”",
    "Por que o químico estava sempre otimista? Porque ele tinha uma solução para tudo."
]

# Função para contar uma piada aleatória
def contar_piada():
    piada = random.choice(piadas)  # Seleciona uma piada aleatória
    print(f"QuintaFeira: {piada}")
    falar(piada)

# Função para processar cálculos matemáticos
def processar_calculo(entrada):
    try:
        # Substitui palavras por operadores matemáticos
        entrada = entrada.lower()
        entrada = entrada.replace("mais", "+").replace("menos", "-")
        entrada = entrada.replace("vezes", "*").replace("dividido por", "/")

        # Extrai apenas os números e operadores
        expressao = re.sub(r"[^0-9+\-*/().]", "", entrada)
        resultado = eval(expressao)
        return resultado
    except Exception as e:
        return f"Não consegui calcular. Verifique a expressão. Erro: {e}"

# Função para a assistente QuintaFeira
def QuintaFeira(faq):
    print("QuintaFeira: Olá! Sou QuintaFeira, sua assistente virtual. Pergunte algo ou diga 'sair' para encerrar.")
    while True:
        entrada_usuario = input("Você: ").strip()

        if entrada_usuario.lower() in ["sair", "tchau", "adeus"]:
            print("QuintaFeira: Até logo! Espero ter ajudado.")
            break

        elif "piada" in entrada_usuario.lower():
            contar_piada()

        elif entrada_usuario in faq:
            print(f"QuintaFeira: {faq[entrada_usuario]}")

        elif any(frase in entrada_usuario.lower() for frase in ["bater o ponto", "preciso bater o ponto", "abre o ponto pra mim", "tenho que bater o ponto", "bater ponto"]):
            print("QuintaFeira: Abrindo o site para bater o ponto...")
            webbrowser.open("http://192.168.1.80:4000")  # Substitua pelo URL do site real

        elif "calcule" in entrada_usuario.lower() or re.search(r"\d+", entrada_usuario):
            print("QuintaFeira: Deixe-me calcular isso para você...")
            resultado = processar_calculo(entrada_usuario)
            print(f"QuintaFeira: O resultado é {resultado}")

        elif "pesquisar no google" in entrada_usuario.lower():
            termo_pesquisa = entrada_usuario.replace("pesquisar no google", "").strip()
            pesquisar_no_google(termo_pesquisa)

        else:
            print("QuintaFeira: Hmm, eu ainda não sei responder isso. Você pode me ensinar?")
            treinar_bot(faq)

# Função principal
def principal():
    faq = carregar_faq()
    while True:
        print("\nEscolha uma opção:")
        print("1. Iniciar chat")
        print("2. Treinar QuintaFeira")
        print("3. Sair")
        escolha = input("Escolha: ").strip()
        if escolha == "1":
            QuintaFeira(faq)
        elif escolha == "2":
            treinar_bot(faq)
        elif escolha == "3":
            print("Saindo...")
            break
        else:
            print("Opção inválida! Tente novamente.")

if __name__ == "__main__":
    principal()
