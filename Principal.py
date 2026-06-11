#!python3.13.11
import random
import sys
import math
import array
import time
try:
    import pygame
except ModuleNotFoundError:
    pygame = None


AUDIO_INITIALIZED = False
AUDIO_ENABLED = True
SOUND_CACHE = {}


def inicializar_audio():
    global AUDIO_INITIALIZED, AUDIO_ENABLED
    if AUDIO_INITIALIZED:
        return
    if pygame is None:
        AUDIO_ENABLED = False
        AUDIO_INITIALIZED = True
        return
    try:
        pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=512)
        AUDIO_INITIALIZED = True
    except pygame.error:
        AUDIO_ENABLED = False
        AUDIO_INITIALIZED = True


def gerar_tom(frequencia, duracao_ms, volume=0.4):
    if not AUDIO_ENABLED:
        return None
    sample_rate = 44100
    samples = int(sample_rate * duracao_ms / 1000)
    buffer = array.array('h')
    for i in range(samples):
        sin_value = math.sin(2.0 * math.pi * frequencia * i / sample_rate)
        buffer.append(int(sin_value * volume * 32767))
    sound = pygame.mixer.Sound(buffer=buffer)
    return sound


def get_som(key, frequencias, duracao_ms=300, volume=0.4):
    if key in SOUND_CACHE:
        return SOUND_CACHE[key]
    if not AUDIO_ENABLED:
        return None
    if isinstance(frequencias, (list, tuple)):
        sounds = [gerar_tom(freq, duracao_ms, volume) for freq in frequencias]
        SOUND_CACHE[key] = sounds
    else:
        SOUND_CACHE[key] = gerar_tom(frequencias, duracao_ms, volume)
    return SOUND_CACHE[key]


def tocar_som(tipo):
    inicializar_audio()
    if not AUDIO_ENABLED:
        return
    try:
        if tipo == "start":
            som = get_som("start", [440, 660], 150)
            if isinstance(som, list):
                for s in som:
                    s.play()
                    time.sleep(0.14)
        elif tipo == "correct":
            sequencia = [660, 740, 880]
            for freq in sequencia:
                som = get_som(f"correct_{freq}", freq, 120)
                if som:
                    som.play()
                    time.sleep(0.14)
        elif tipo == "wrong":
            sequencia = [330, 220]
            for freq in sequencia:
                som = get_som(f"wrong_{freq}", freq, 220)
                if som:
                    som.play()
                    time.sleep(0.24)
        elif tipo == "game_over":
            sequencia = [220, 196, 174]
            for freq in sequencia:
                som = get_som(f"game_over_{freq}", freq, 200)
                if som:
                    som.play()
                    time.sleep(0.22)
        elif tipo == "lifeline":
            som = get_som("lifeline", [660, 880], 100)
            if isinstance(som, list):
                for s in som:
                    s.play()
                    time.sleep(0.12)
        elif tipo == "win":
            sequencia = [880, 988, 1047]
            for freq in sequencia:
                som = get_som(f"win_{freq}", freq, 140)
                if som:
                    som.play()
                    time.sleep(0.16)
    except pygame.error:
        pass


def tocar_suspense():
    inicializar_audio()
    if not AUDIO_ENABLED:
        return None
    som = get_som("suspense", 220, 800, volume=0.01)
    if som:
        return som.play(loops=-1)
    return None


def parar_suspense(channel):
    if channel is not None:
        channel.stop()


def exibir_menu_inicial():
    print("\n" + "#" * 40)
    print("#          SHOW DO MILHÃO          #")
    print("#" * 40)
    print("1 - Jogar")
    print("2 - Instruções")
    print("3 - Ranking")
    print("4 - Sair")
    print()
    return input("Escolha uma opção: ").strip()


def exibir_instrucoes():
    print("\nINSTRUÇÕES")
    print("Ao iniciar, escolha um tema para jogar.")
    print("Responda as perguntas digitando A, B, C ou D.")
    print("Digite L durante uma pergunta para usar uma ajuda.")
    print("Digite S durante uma pergunta para sair do jogo.")
    print("As ajudas disponíveis são: 50-50, pedir ao público e pular pergunta.")
    print("Quanto mais perguntas acertar, maior será o prêmio.\n")


def exibir_ranking():
    ranking = [
        {
            "nome": "Guilherme Arrais",
            "idade": 16,
            "serie": "2a",
            "pontuacao": 850000,
        },
        {
            "nome": "Pietro Martins",
            "idade": 16,
            "serie": "2a",
            "pontuacao": 650000,
        },
    ]

    print("\nRANKING")
    print("-" * 40)
    for posicao, jogador in enumerate(ranking, start=1):
        print(
            f"{posicao}. {jogador['nome']} - {jogador['idade']} anos - "
            f"{jogador['serie']} - R$ {jogador['pontuacao']}"
        )
    print("-" * 40)
    print()


def exibir_titulo(nome, serie, tema):
    tocar_som("start")
    print("\n" + "#" * 40)
    print("#    MILIONÁRIO - JOGO DE PERGUNTAS   #")
    print("#" * 40)
    print(f"Tema: {tema}")
    print(
        f"Bem-vindo, {nome}, da {serie}! Responda as perguntas ou use uma ajuda quando precisar.")
    print("Digite 'L' para usar uma lifeline, 'S' para sair do jogo a qualquer momento.")
    print()


def solicitar_dados_jogador():
    print("DADOS DO JOGADOR")
    while True:
        nome = input("Digite seu nome: ").strip()
        if nome:
            break
        print("Nome não pode ficar em branco.")

    while True:
        idade = input("Digite sua idade: ").strip()
        if idade.isdigit() and int(idade) > 0:
            idade = int(idade)
            break
        print("Idade inválida. Digite um número inteiro maior que zero.")

    while True:
        serie = input("Digite sua série escolar: ").strip()
        if serie:
            break
        print("Série escolar não pode ficar em branco.")

    print(
        f"\nOlá, {nome}! Idade registrada: {idade} anos. Série escolar: {serie}.")
    print("Escolha um tema e responda com atenção.")
    print("Você pode usar as ajudas durante o jogo quando precisar.\n")
    return nome, idade, serie


PREMIOS = [
    100, 200, 300, 500, 1000, 2000, 3000, 5000, 10000, 15000,
    25000, 50000, 75000, 100000, 150000, 250000, 350000,
    500000, 600000, 700000, 780000, 820000, 860000, 900000,
    950000, 1000000,
]


def criar_perguntas():
    return [
        {
            "texto": 'Identifique a oração em destaque cujo sujeito é indeterminado.',
            "opcoes": ['Está garoando hoje.', 'Ligaram para saber como você se sente.', 'Aluga-se casa.', 'Faz anos que não falo com ele'],
            "resposta": 'C',
            "premio": 100,
        },
        {
            "texto": 'Qual sinal de pontuação encerra uma frase interrogativa?',
            "opcoes": ['Ponto final', 'Vírgula', 'Ponto e vírgula', 'Ponto de interrogação'],
            "resposta": 'D',
            "premio": 200,
        },
        {
            "texto": 'Qual sinal indica surpresa ou emoção forte?',
            "opcoes": ['Sinal de virgula', 'Exclamacao', 'Dois-pontos', 'Reticencias'],
            "resposta": 'B',
            "premio": 300,
        },
        {
            "texto": 'Ao localizar fatos no texto, o leitor deve buscar informações que sejam:',
            "opcoes": ['opinioes pessoais', 'inferencias do leitor', 'informacoes exatas do texto', 'suposicoes vagas'],
            "resposta": 'C',
            "premio": 500,
        },
        {
            "texto": 'Ler entrelinhas permite identificar:',
            "opcoes": ['dados explicitos', 'subtexto', 'numeros no texto', 'correcoes gramaticais'],
            "resposta": 'B',
            "premio": 1000,
        },
        {
            "texto": 'Uma mensagem subentendida depende principalmente de:',
            "opcoes": ['pontuacao', 'contexto da situacao', 'grifo', 'fonte do texto'],
            "resposta": 'B',
            "premio": 2000,
        },
        {
            "texto": 'O uso de ponto e vírgula geralmente liga orações que são:',
            "opcoes": ['independentes', 'opostas no sentido', 'conexas', 'alternativas'],
            "resposta": 'C',
            "premio": 3000,
        },
        {
            "texto": 'A frase que termina com ponto final é normalmente:',
            "opcoes": ['interrogativa', 'exclamativa', 'frase declarativa', 'trecho aberto'],
            "resposta": 'C',
            "premio": 5000,
        },
        {
            "texto": 'Qual elemento mostra que o autor escreveu com emoção forte?',
            "opcoes": ['Palavras longas', 'Ponto final', 'Interrogacao', 'Exclamacao'],
            "resposta": 'D',
            "premio": 10000,
        },
        {
            "texto": 'Identificar personagens significa lembrar:',
            "opcoes": ['nomes exatos dos personagens', 'sons das palavras', 'cores favoritas', 'numero de letras'],
            "resposta": 'A',
            "premio": 15000,
        },
        {
            "texto": 'Qual alternativa descreve melhor um fato no texto?',
            "opcoes": ['opinião do narrador', 'informação apresentada', 'sensação pessoal', 'predição futura'],
            "resposta": 'B',
            "premio": 25000,
        },
        {
            "texto": "Uma pergunta como 'Você gostou?' termina com:",
            "opcoes": ['Sinal de ponto final', 'Sinal de virgula', 'Sinal de reticencias', 'Interrogacao'],
            "resposta": 'D',
            "premio": 50000,
        },
        {
            "texto": 'Ao encontrar dados no texto, o leitor deve procurar informações que estejam:',
            "opcoes": ['implícitas', 'explicitamente escritas', 'em outras fontes', 'omitidas'],
            "resposta": 'B',
            "premio": 75000,
        },
        {
            "texto": "A frase 'Não foi apenas um dia triste' sugere:",
            "opcoes": ['alegria evidente', 'tristeza', 'fato isolado', 'ordem direta'],
            "resposta": 'B',
            "premio": 100000,
        },
        {
            "texto": 'Qual sinal é usado para separar itens complexos em uma lista?',
            "opcoes": ['ponto final', 'vírgula', 'ponto e vírgula', 'três pontos'],
            "resposta": 'C',
            "premio": 150000,
        },
        {
            "texto": 'Uma causa de um acontecimento costuma aparecer antes do:',
            "opcoes": ['efeito', 'titulo do texto', 'subtitulo', 'sumario'],
            "resposta": 'A',
            "premio": 250000,
        },
        {
            "texto": 'A leitura entrelinhas ajuda a perceber:',
            "opcoes": ['a cor do texto', 'o tipo de fonte', 'o sentimento não dito', 'a margem do papel'],
            "resposta": 'C',
            "premio": 350000,
        },
        {
            "texto": 'No texto, a informação que deve ser localizada exatamente é:',
            "opcoes": ['um fato', 'uma opinião', 'um adjetivo', 'uma adivinhação'],
            "resposta": 'A',
            "premio": 500000,
        },
        {
            "texto": 'O uso correto de pontuação faz o texto ficar mais:',
            "opcoes": ['confuso', 'claro e organizado', 'curto', 'longo'],
            "resposta": 'B',
            "premio": 600000,
        },
        {
            "texto": 'Quando se fala em mensagem subentendida, procura-se o que está:',
            "opcoes": ['escrito em negrito', 'muito destacado', 'implicito', 'ausente do texto'],
            "resposta": 'C',
            "premio": 700000,
        },
        {
            "texto": 'Qual recurso textual cria suspense sem afirmar diretamente?',
            "opcoes": ['descrição clara', 'afirmação direta', 'sugestão indireta', 'questionamento'],
            "resposta": 'C',
            "premio": 780000,
        },
        {
            "texto": 'Quando um personagem fala de forma indireta, há:',
            "opcoes": ['uma descrição literal', 'uma instrução explícita', 'um dado numérico', 'uma mensagem subentendida'],
            "resposta": 'D',
            "premio": 820000,
        },
        {
            "texto": 'Qual pontuação é usada antes de uma explicação adicional?',
            "opcoes": ['dois pontos', 'vírgula', 'ponto final', 'aspas'],
            "resposta": 'A',
            "premio": 860000,
        },
        {
            "texto": 'A leitura entrelinhas revela geralmente:',
            "opcoes": ['um número exato', 'uma sensação oculta', 'uma lista de itens', 'um título evidente'],
            "resposta": 'B',
            "premio": 900000,
        },
        {
            "texto": 'Dados exatos no texto devem ser localizados de forma:',
            "opcoes": ['imprecisa', 'aproximada', 'literal', 'aleatória'],
            "resposta": 'C',
            "premio": 950000,
        },
        {
            "texto": 'Qual pontuação liga duas ideias relacionadas dentro da mesma frase?',
            "opcoes": ['ponto final', 'vírgula', 'dois pontos', 'ponto e vírgula'],
            "resposta": 'D',
            "premio": 1000000,
        },
    ]


def criar_perguntas_por_lista(dados):
    perguntas = []
    for premio, item in zip(PREMIOS, dados):
        perguntas.append({
            "texto": item["texto"],
            "opcoes": item["opcoes"],
            "resposta": item["resposta"],
            "premio": premio,
        })
    return perguntas


def criar_perguntas_matematica():
    dados = [
        {
            "texto": 'Na equação ax² + bx + c = 0, qual expressão representa o delta?',
            "opcoes": ['b²-4ac', 'a² - 4bc', '2a + b + c', 'b - 4ac'],
            "resposta": 'A',
        },
        {
            "texto": 'Se o delta de uma equação do segundo grau é maior que zero, ela possui:',
            "opcoes": ['nenhuma raiz real', 'uma raiz real', 'duas raízes reais diferentes', 'duas raízes não reais'],
            "resposta": 'C',
        },
        {
            "texto": 'Se o delta é igual a zero, a equação do segundo grau possui:',
            "opcoes": ['raiz dupla', 'duas raizes reais diferentes', 'nenhuma raiz real', 'tres raizes reais'],
            "resposta": 'A',
        },
        {
            "texto": 'Se o delta é menor que zero, a equação do segundo grau possui:',
            "opcoes": ['duas raizes reais', 'uma raiz real', 'nenhuma raiz real existente', 'infinitas raizes'],
            "resposta": 'C',
        },
        {
            "texto": 'Na fórmula de Bhaskara, o denominador é:',
            "opcoes": ['2 vezes a', '2 vezes o b', '4 vezes o a', 'a ao quadrado'],
            "resposta": 'A',
        },
        {
            "texto": 'Na equação x² - 5x + 6 = 0, os coeficientes a, b e c são:',
            "opcoes": ['a=1,b=-5,c=6', 'a=1,b=5,c=6', 'a=1,b=5,c=0', 'a=0,b=5,c=6'],
            "resposta": 'A',
        },
        {
            "texto": 'Uma equação do segundo grau completa possui:',
            "opcoes": ['Apenas ax2', 'Apenas bx', 'A, B e C', 'Somente c'],
            "resposta": 'C',
        },
        {
            "texto": 'A equação x² - 9 = 0 é chamada de incompleta porque:',
            "opcoes": ['Nao possui o termo bx', 'Nao tem termo ax2', 'Nao tem termo c', 'Nao tem igualdade'],
            "resposta": 'A',
        },
        {
            "texto": 'A equação 2x² = 0 tem como raiz:',
            "opcoes": ['x=0', 'x=+1', 'x=+2', 'x=-2'],
            "resposta": 'A',
        },
        {
            "texto": 'Em uma função do primeiro grau f(x) = ax + b, o número a representa:',
            "opcoes": ['coeficiente angular', 'termo independente', 'raiz da função', 'valor máximo'],
            "resposta": 'A',
        },
        {
            "texto": 'Em f(x) = 3x + 2, o termo independente é:',
            "opcoes": ['termo (0)', 'termo 2', 'termo 3x', 'termo x + 2'],
            "resposta": 'B',
        },
        {
            "texto": 'Uma função do primeiro grau tem gráfico em forma de:',
            "opcoes": ['parábola', 'reta', 'círculo', 'hipérbole'],
            "resposta": 'B',
        },
        {
            "texto": 'Se a > 0 em f(x) = ax + b, a função é:',
            "opcoes": ['funcao crescente linear', 'decrescente', 'constante', 'quadratica'],
            "resposta": 'A',
        },
        {
            "texto": 'Se a < 0 em f(x) = ax + b, a função é:',
            "opcoes": ['crescente no grafico', 'decrescente', 'sempre positiva', 'sem grafico real'],
            "resposta": 'B',
        },
        {
            "texto": 'A raiz da função f(x) = 2x - 6 é:',
            "opcoes": ['indefinida', 'raiz igual a 3', 'não possui', 'raiz 2x - 6'],
            "resposta": 'B',
        },
        {
            "texto": 'Modelar uma função do primeiro grau significa:',
            "opcoes": ['funcao afim', 'desenhar uma parabola', 'calcular apenas delta', 'eliminar o eixo y'],
            "resposta": 'A',
        },
        {
            "texto": 'Se um táxi cobra R$ 5 fixos mais R$ 2 por km, a função do preço é:',
            "opcoes": ['P=5x+2', 'P(x)=2x+5', 'P(x)=x+5', 'P=7x'],
            "resposta": 'B',
        },
        {
            "texto": 'Na função P(x) = 2x + 5, se x = 10, o valor de P(x) é:',
            "opcoes": ['R$ -25', 'R$ 250', 'R$ 25', 'R$ 205'],
            "resposta": 'C',
        },
        {
            "texto": 'A equação x² - 4x + 4 = 0 possui delta:',
            "opcoes": ['delta igual a zero', 'delta positivo 4', 'delta positivo 8', 'delta negativo -4'],
            "resposta": 'A',
        },
        {
            "texto": 'A equação x² + x + 1 = 0 possui delta:',
            "opcoes": ['delta positivo cinco', 'delta positivo de um', 'delta igual a zero', 'delta negativo -3'],
            "resposta": 'D',
        },
        {
            "texto": 'Quando uma equação do segundo grau tem duas raízes reais iguais, seu delta é:',
            "opcoes": ['positivo', 'negativo', 'zero', 'maior que 10'],
            "resposta": 'C',
        },
        {
            "texto": 'A forma geral da equação do segundo grau é:',
            "opcoes": ['ax + b = 0', 'x³ + ax = 0', 'a/x + b = 0', 'ax² + bx + c = 0'],
            "resposta": 'D',
        },
        {
            "texto": 'Na equação 3x² - 2x + 1 = 0, o coeficiente b é:',
            "opcoes": ['b=-2', 'b=3', 'b=1', 'b=0'],
            "resposta": 'A',
        },
        {
            "texto": 'A função f(x) = -4x + 8 é:',
            "opcoes": ['crescente', 'decrescente', 'quadrática', 'exponencial'],
            "resposta": 'B',
        },
        {
            "texto": 'Em uma função linear de custo C(x) = 10x + 30, o valor 30 representa:',
            "opcoes": ['preço por unidade', 'quantidade vendida', 'custo fixo', 'raiz da função'],
            "resposta": 'C',
        },
        {
            "texto": 'Para resolver uma equação do segundo grau por Bhaskara, primeiro é comum calcular:',
            "opcoes": ['o perímetro', 'a porcentagem', 'a média', 'o delta'],
            "resposta": 'D',
        },
    ]
    return criar_perguntas_por_lista(dados)


def criar_perguntas_fisica():
    dados = [
        {
            "texto": 'Em uma transformação isotérmica de um gás ideal, qual grandeza permanece constante?',
            "opcoes": ['temperatura', 'pressao do gas', 'volume do gas', 'massa molecular'],
            "resposta": 'A',
        },
        {
            "texto": 'A lei de Boyle relaciona pressão e volume quando a temperatura é:',
            "opcoes": ['constante', 'variável', 'nula', 'infinita'],
            "resposta": 'A',
        },
        {
            "texto": 'Na transformação isotérmica, se o volume aumenta, a pressão tende a:',
            "opcoes": ['Aumentar', 'Cair', 'Ficar sempre zero', 'Sumir'],
            "resposta": 'B',
        },
        {
            "texto": 'Em uma transformação isobárica, qual grandeza permanece constante?',
            "opcoes": ['pressao constante', 'volume', 'temperatura', 'energia cinetica'],
            "resposta": 'A',
        },
        {
            "texto": 'Em uma transformação isovolumétrica, qual grandeza permanece constante?',
            "opcoes": ['volume', 'pressão', 'temperatura', 'número de mols'],
            "resposta": 'A',
        },
        {
            "texto": 'A equação geral dos gases ideais é:',
            "opcoes": ['PV = nRT', 'P + V', 'P/V', 'P = mgh'],
            "resposta": 'A',
        },
        {
            "texto": 'Na equação PV = nRT, a letra P representa:',
            "opcoes": ['pressao', 'potencia', 'peso do corpo', 'periodo orbital'],
            "resposta": 'A',
        },
        {
            "texto": 'Na equação PV = nRT, a letra V representa:',
            "opcoes": ['velocidade', 'volume do gas', 'vacuo', 'variacao'],
            "resposta": 'B',
        },
        {
            "texto": 'Na equação PV = nRT, a letra T representa:',
            "opcoes": ['tempo medido', 'temperatura', 'tensão elétrica', 'trabalho realizado'],
            "resposta": 'B',
        },
        {
            "texto": 'A temperatura usada nas leis dos gases deve estar geralmente em:',
            "opcoes": ['temperatura em Kelvin', 'Celsius e Kelvin', 'Fahrenheit apenas', 'metros'],
            "resposta": 'A',
        },
        {
            "texto": 'Zero grau Celsius corresponde aproximadamente a:',
            "opcoes": ['0 K', '-100 Kelvin', '+273 Kelvin', '373 Kelvin'],
            "resposta": 'C',
        },
        {
            "texto": 'Em uma transformação isobárica, volume e temperatura absoluta são:',
            "opcoes": ['proporcionais', 'inversamente proporcionais', 'valores sempre iguais', 'independentes entre si'],
            "resposta": 'A',
        },
        {
            "texto": 'Em uma transformação isovolumétrica, pressão e temperatura absoluta são:',
            "opcoes": ['diretamente proporcionais', 'inversas', 'iguais a zero', 'sem relacao'],
            "resposta": 'A',
        },
        {
            "texto": 'Na transformação isotérmica, pressão e volume são:',
            "opcoes": ['diretamente proporcionais', 'inversas', 'iguais sempre', 'sempre constantes'],
            "resposta": 'B',
        },
        {
            "texto": 'A constante R na equação dos gases ideais é chamada de:',
            "opcoes": ['constante universal dos gases', 'resistência elétrica', 'raio do gás', 'razão térmica'],
            "resposta": 'A',
        },
        {
            "texto": 'O número de mols de um gás é representado por:',
            "opcoes": ['n (mols)', 'm (massa)', 'g (gravidade)', 't (tempo)'],
            "resposta": 'A',
        },
        {
            "texto": 'Se a temperatura de um gás aumenta em volume constante, a pressão:',
            "opcoes": ['aumenta com a temperatura', 'diminui', 'fica sempre zero', 'não existe'],
            "resposta": 'A',
        },
        {
            "texto": 'Se um gás é comprimido mantendo a temperatura constante, seu volume:',
            "opcoes": ['Aumenta', 'Reduz', 'Nao muda', 'Vira massa'],
            "resposta": 'B',
        },
        {
            "texto": 'A lei de Charles está ligada principalmente à transformação:',
            "opcoes": ['isobarica, em pressao constante', 'isotermica, sem pressão', 'isovolumetrica', 'adiabatica, sem calor'],
            "resposta": 'A',
        },
        {
            "texto": 'A lei de Gay-Lussac está ligada principalmente à transformação:',
            "opcoes": ['isocorica', 'isotermica', 'mecanica simples', 'eletrica comum'],
            "resposta": 'A',
        },
        {
            "texto": 'Um gás ideal é um modelo em que as partículas são consideradas:',
            "opcoes": ['sempre líquidas', 'presas em posições fixas', 'sem volume próprio e sem interações relevantes', 'sem movimento'],
            "resposta": 'C',
        },
        {
            "texto": 'Quando a quantidade de gás n aumenta, mantendo P e T constantes, o volume tende a:',
            "opcoes": ['ficar negativo', 'diminuir', 'zerar', 'aumentar'],
            "resposta": 'D',
        },
        {
            "texto": 'A unidade SI de pressão é:',
            "opcoes": ['pascal', 'metro', 'joule', 'kelvin'],
            "resposta": 'A',
        },
        {
            "texto": 'A unidade SI de volume é:',
            "opcoes": ['pascal', 'metro cúbico', 'newton', 'kelvin'],
            "resposta": 'B',
        },
        {
            "texto": 'Em PV = nRT, se n e R são constantes, P, V e T descrevem:',
            "opcoes": ['a massa da Terra', 'a cor do gás', 'o estado do gás', 'a velocidade da luz'],
            "resposta": 'C',
        },
        {
            "texto": 'Uma transformação gasosa é uma mudança em grandezas como:',
            "opcoes": ['densidade, nota e série', 'cor, cheiro e sabor', 'altura, idade e nome', 'pressão, volume e temperatura'],
            "resposta": 'D',
        },
    ]
    return criar_perguntas_por_lista(dados)


def criar_perguntas_historia():
    dados = [
        {
            "texto": 'Quem foi o prefeito responsável pela grande reforma urbana do Rio de Janeiro no início do século XX?',
            "opcoes": ['Getulio Vargas presidente', 'Pereira Passos', 'Rodrigues Alves presidente', 'Oswaldo Cruz sanitarista'],
            "resposta": 'B',
        },
        {
            "texto": 'Qual doença o governo brasileiro tentava erradicar com a vacinação obrigatória que causou a Revolta da Vacina em 1904?',
            "opcoes": ['Febre Amarela', 'Peste Bubonica', 'Variola pela vacina obrigatoria', 'Gripe Espanhola'],
            "resposta": 'C',
        },
        {
            "texto": 'Qual era o lema principal que guiava os ideais da Revolução Francesa?',
            "opcoes": ['Deus, Patria e Familia integralista', 'Paz, Pao e Terra da Revolucao Russa', 'Ordem e Progresso positivista republicano', 'Liberdade, igualdade, fraternidade'],
            "resposta": 'D',
        },
        {
            "texto": "Nas independências da América Espanhola, quem eram os 'criollos'?",
            "opcoes": ['Descendentes de espanhóis nascidos na América', 'Indígenas escravizados nas minas', 'Espanhóis natos enviados pela Coroa', 'Mestiços sem direitos políticos'],
            "resposta": 'A',
        },
        {
            "texto": "Qual órgão foi criado no Brasil em 1910 para 'proteger' os povos indígenas?",
            "opcoes": ['Fundacao Nacional do Indio (FUNAI)', 'Instituto Brasileiro do Meio Ambiente', 'Servico de Protecao aos Indios', 'Ministerio dos Povos Originarios'],
            "resposta": 'C',
        },
        {
            "texto": 'A destruição de cortiços e velhos casarões no centro do RJ ficou popularmente conhecida como:',
            "opcoes": ['Bota-abaixo dos corticos', 'Limpeza Geral', 'Plano Diretor', 'Marcha para o Oeste'],
            "resposta": 'A',
        },
        {
            "texto": 'Um interesse econômico fundamental para a elite criolla buscar a independência na América foi:',
            "opcoes": ['Distribuir terras aos camponeses pobres', 'fim do pacto colonial', 'abolicao imediata da escravidao', 'criacao de industrias de base'],
            "resposta": 'B',
        },
        {
            "texto": 'A Revolução Francesa teve forte caráter burguês porque buscou principalmente:',
            "opcoes": ['Derrubar a monarquia para dar poder político exclusivo aos camponeses', 'Acabar com os privilégios feudais da nobreza para favorecer o livre comércio e a propriedade', 'Instaurar uma ditadura do proletariado na Europa', 'Manter os privilégios do clero, mas com impostos menores'],
            "resposta": 'B',
        },
        {
            "texto": 'A política higienista no Rio de Janeiro republicano resultou, na prática, em:',
            "opcoes": ['expulsão dos pobres do centro', 'construção de hospitais públicos em todas as favelas', 'distribuição de renda aos moradores desapropriados', 'fim das desigualdades sociais na capital federal'],
            "resposta": 'A',
        },
        {
            "texto": 'O médico sanitarista que liderou as campanhas de saúde pública durante o governo Rodrigues Alves foi:',
            "opcoes": ['Carlos Chagas', 'Vital Brazil', 'Oswaldo Gonçalves', 'Adolfo Lutz'],
            "resposta": 'C',
        },
        {
            "texto": 'Na Primeira República brasileira, a ação do Estado em relação aos indígenas focava em:',
            "opcoes": ['Demarcar suas terras ancestrais e respeitar sua cultura de forma isolada', "Integrá-los forçosamente à 'civilização' e transformá-los em trabalhadores rurais", 'Garantir cotas nas nascentes universidades públicas', 'Armá-los para proteger as fronteiras do país contra invasores'],
            "resposta": 'B',
        },
        {
            "texto": 'Qual documento da Revolução Francesa consagrou a proteção à propriedade privada, refletindo o interesse burguês?',
            "opcoes": ['Codigo de Hamurabi antigo', 'Declaracao de 1789', 'Constituicao Civil do Clero', 'Tratado de Versalhes'],
            "resposta": 'B',
        },
        {
            "texto": 'A independência do Haiti foi única no continente americano porque:',
            "opcoes": ['Foi liderada por escravizados e resultou na imediata abolição da escravidão', 'Foi a única apoiada militarmente pela Inglaterra', 'Foi um processo pacífico liderado pela elite branca local', 'Resultou na anexação do território pelos Estados Unidos'],
            "resposta": 'A',
        },
        {
            "texto": 'Durante a Revolta da Vacina, o povo também protestava contra:',
            "opcoes": ['Entrada do Brasil na Primeira Guerra Mundial', 'truculencia sanitaria', 'Fechamento do Congresso Nacional por Rodrigues Alves', 'Proibicao do Carnaval de rua pela policia republicana'],
            "resposta": 'B',
        },
        {
            "texto": 'A reforma de Pereira Passos no Rio de Janeiro foi diretamente inspirada na remodelação de qual capital europeia?',
            "opcoes": ['Cuba', 'Peru', 'Paris', 'Roma'],
            "resposta": 'C',
        },
        {
            "texto": 'Na Revolução Francesa, o período do Diretório (1795-1799) representou politicamente:',
            "opcoes": ['Radicalizacao popular liderada por Robespierre', 'Volta da Monarquia Absolutista', 'poder da alta burguesia', 'Dominio da Igreja Catolica sobre as leis do Estado'],
            "resposta": 'C',
        },
        {
            "texto": "A 'Doutrina Monroe' (1823) influenciou as independências americanas ao defender a ideia de:",
            "opcoes": ['Destino Manifesto e expansão para o Pacífico', 'América para os americanos, opondo-se a tentativas de recolonização europeia', 'Pan-americanismo e uma única república na América do Sul', 'Abolição gradual da escravatura em todo o hemisfério'],
            "resposta": 'B',
        },
        {
            "texto": 'O SPI (Serviço de Proteção aos Índios) tinha fortes bases no Positivismo, o qual acreditava que os indígenas:',
            "opcoes": ['Culturalmente superiores aos europeus', 'necessitavam de tutela estatal', 'Exterminados para liberar terras ao agronegocio', 'Republicas autonomas dentro do Brasil'],
            "resposta": 'B',
        },
        {
            "texto": 'A política higienista no RJ também agiu como controle social, visando reprimir principalmente:',
            "opcoes": ['O comércio de luxo de produtos importados', 'A vadiagem, a capoeira e as manifestações culturais afro-brasileiras', 'As greves de trabalhadores das montadoras de automóveis', 'Os bailes de elite financiados pelos barões do café'],
            "resposta": 'B',
        },
        {
            "texto": 'Na Independência do Brasil, o principal interesse da elite agrária que apoiou D. Pedro I era:',
            "opcoes": ['livre comercio com escravidao', 'Transformar o Brasil em uma federacao descentralizada e industrial', 'Garantir reforma agraria para evitar revoltas populares', 'Aliar-se a Franca para derrotar a marinha britanica'],
            "resposta": 'A',
        },
        {
            "texto": 'A Lei de Le Chapelier (1791) evidencia o aspecto excludente da burguesia na Revolução Francesa ao:',
            "opcoes": ['Restaurar o poder de veto do Rei', 'Aumentar os impostos sobre o pão', 'Proibir as corporações de ofício, greves e a formação de sindicatos trabalhistas', 'Excluir as mulheres das eleições indiretas'],
            "resposta": 'C',
        },
        {
            "texto": 'Durante a Revolta da Vacina, ocorreu também o levante da Escola Militar da Praia Vermelha. Qual era seu objetivo político oculto?',
            "opcoes": ['Restaurar a Monarquia de D. Pedro II', 'Instaurar uma ditadura comunista inspirada em Marx', 'Forçar a capital do Brasil a ser transferida para Brasília imediatamente', 'Derrubar Rodrigues Alves e instaurar um governo militar positivista/florianista'],
            "resposta": 'D',
        },
        {
            "texto": 'O Congresso do Panamá (1826), convocado por Simón Bolívar, fracassou devido principalmente:',
            "opcoes": ['Aos interesses particularistas das elites locais e à oposição de Inglaterra e EUA a uma América unida', 'À invasão espanhola que reconquistou a Venezuela no mesmo ano', 'À recusa dos escravizados em lutar no exército bolivariano', 'Aos desastres naturais que destruíram o local das negociações'],
            "resposta": 'A',
        },
        {
            "texto": 'O Marechal Rondon, primeiro líder do SPI, adotava um lema que refletia sua abordagem de pacificação tutelar. Qual era?',
            "opcoes": ['A ordem pelo progresso', 'Morrer se preciso for, matar nunca', 'A lei é para todos, a terra para quem trabalha', 'Civilizar ou perecer'],
            "resposta": 'B',
        },
        {
            "texto": "Antes da aceitação total da bacteriologia, o higienismo no Brasil apoiava-se na 'Teoria Miasmática', que justificava a destruição de cortiços argumentando que:",
            "opcoes": ['Eles abrigavam ratos infectados com pulgas transmissoras', 'A falta de moralidade religiosa causava o enfraquecimento do sistema imune', 'As doenças emanavam de gases ruins (miasmas) de ambientes fechados, exigindo circulação de ar e luz solar', 'As doenças eram transmitidas por mosquitos encontrados na água parada dos casarões'],
            "resposta": 'C',
        },
        {
            "texto": 'Analisando as independências latino-americanas e a modernização republicana brasileira sob a ótica da Revolução Francesa, qual afirmação melhor sintetiza a formação dos Estados na América Latina?',
            "opcoes": ['A aplicação irrestrita da fraternidade jacobina gerou repúblicas radicais e igualitárias no século XIX.', 'A elite criolla rejeitou integralmente o Iluminismo, copiando o modelo absolutista ibérico para sufocar o desenvolvimento urbano.', 'O sucesso do pan-americanismo garantiu o fim imediato das desigualdades, graças à abolição da escravidão financiada pela burguesia europeia.', 'Houve uma apropriação seletiva do liberalismo pela elite: buscou-se o livre-mercado e a modernização institucional, mas perpetuou-se a exclusão social e política de negros, indígenas e pobres urbanos.'],
            "resposta": 'D',
        },
    ]
    return criar_perguntas_por_lista(dados)


def criar_perguntas_biologia():
    dados = [
        {
            "texto": 'Qual ação contribui diretamente para a preservação ambiental?',
            "opcoes": ['Expansão de áreas urbanas', 'Descarte irregular de resíduos', 'Exploração intensiva de recursos naturais', 'proteger ecossistemas'],
            "resposta": 'D',
        },
        {
            "texto": 'O conceito de conservação ambiental está relacionado a:',
            "opcoes": ['Proibir qualquer atividade humana', 'Substituir florestas por plantações', 'Utilizar os recursos naturais de forma sustentável', 'Eliminar espécies exóticas'],
            "resposta": 'C',
        },
        {
            "texto": 'Qual atividade representa uma ameaça à biodiversidade?',
            "opcoes": ['Educacao ambiental', 'Desmatar', 'Reciclagem', 'Reflorestamento'],
            "resposta": 'B',
        },
        {
            "texto": 'A preservação ambiental tem como principal objetivo:',
            "opcoes": ['Manter ambientes naturais protegidos de alterações significativas', 'Expandir áreas agrícolas', 'Construir novas rodovias', 'Aumentar a exploração mineral'],
            "resposta": 'A',
        },
        {
            "texto": 'Qual prática favorece a conservação dos recursos naturais?',
            "opcoes": ['Queimadas frequentes', 'Caca predatoria', 'Reciclagem', 'Poluicao de rios'],
            "resposta": 'C',
        },
        {
            "texto": 'As unidades de conservação foram criadas para:',
            "opcoes": ['Expandir cidades', 'Proteger a biodiversidade e os ecossistemas', 'Incentivar a mineração', 'Facilitar o desmatamento'],
            "resposta": 'B',
        },
        {
            "texto": 'Qual unidade pertence ao grupo de proteção integral?',
            "opcoes": ['Área de Proteção Ambiental', 'Reserva Extrativista', 'Floresta Nacional', 'Parque Nacional'],
            "resposta": 'D',
        },
        {
            "texto": 'Uma Área de Proteção Ambiental (APA) permite:',
            "opcoes": ['Caça de espécies ameaçadas', 'Desmatamento sem controle', 'Uso sustentável dos recursos naturais', 'Ocupação irregular'],
            "resposta": 'C',
        },
        {
            "texto": 'A sigla SNUC significa:',
            "opcoes": ['Sistema Nacional de Uso da Conservacao Ambiental', 'Sistema Nacional de Unidades de Conservacao', 'Servico Nacional de Unidades Conservadas no Brasil', 'Sistema Natural de Conservacao Ambiental Federal'],
            "resposta": 'B',
        },
        {
            "texto": 'Uma Reserva Biológica tem como principal finalidade:',
            "opcoes": ['Preservação integral da biodiversidade', 'Produção agrícola', 'Extração de madeira', 'Pecuária extensiva'],
            "resposta": 'A',
        },
        {
            "texto": 'Bioacumulação é o processo de:',
            "opcoes": ['Produção de nutrientes', 'Reprodução celular', 'Acúmulo de substâncias tóxicas em organismos', 'Formação de fósseis'],
            "resposta": 'C',
        },
        {
            "texto": 'Qual substância pode sofrer bioacumulação nos seres vivos?',
            "opcoes": ['Oxigenio dissolvido', 'Mercurio', 'Agua potavel', 'Gas carbonico'],
            "resposta": 'B',
        },
        {
            "texto": 'A bioacumulação ocorre quando:',
            "opcoes": ['Eliminacao rapida pelo organismo', 'Nao existe cadeia alimentar', 'Ambiente sem poluentes', 'absorcao maior que eliminacao em organismos'],
            "resposta": 'D',
        },
        {
            "texto": 'Em uma cadeia alimentar contaminada, os maiores níveis de poluentes costumam ser encontrados:',
            "opcoes": ['Nos organismos produtores', 'Nos organismos decompositores', 'Predadores de topo', 'Apenas na agua contaminada'],
            "resposta": 'C',
        },
        {
            "texto": 'O aumento da concentração de contaminantes ao longo dos níveis tróficos recebe o nome de:',
            "opcoes": ['Fotossintese', 'biomagnificacao trofica', 'Respiracao celular', 'Sucessao ecologica'],
            "resposta": 'B',
        },
        {
            "texto": 'Uma aplicação benéfica da radiação é:',
            "opcoes": ['Radioterapia', 'Contaminacao ambiental', 'Danos ao DNA celular', 'Exposicao excessiva de trabalhadores'],
            "resposta": 'A',
        },
        {
            "texto": 'A exposição prolongada a altas doses de radiação pode causar:',
            "opcoes": ['Producao de vitaminas', 'Crescimento celular controlado', 'mutacoes geneticas no DNA celular', 'Fotossintese'],
            "resposta": 'C',
        },
        {
            "texto": 'Os raios X são amplamente utilizados para:',
            "opcoes": ['Producao agricola intensiva', 'Diagnostico medico', 'Geracao de energia hidreletrica', 'Tratamento de agua potavel'],
            "resposta": 'B',
        },
        {
            "texto": 'Qual das alternativas representa uma fonte natural de radiação?',
            "opcoes": ['Equipamento de radiografia', 'Usina nuclear', 'Reator experimental', 'raios cósmicos naturais do espaço'],
            "resposta": 'D',
        },
        {
            "texto": 'A proteção radiológica busca:',
            "opcoes": ['Aumentar a exposição humana', 'Eliminar toda tecnologia nuclear', 'Reduzir riscos da radiação', 'Produzir resíduos radioativos'],
            "resposta": 'C',
        },
        {
            "texto": 'A mitose resulta em:',
            "opcoes": ['Quatro células diferentes', 'Oito células haploides', 'Duas células geneticamente idênticas', 'Apenas gametas'],
            "resposta": 'C',
        },
        {
            "texto": 'A principal função da meiose é:',
            "opcoes": ['Produzir células somáticas', 'Reparar tecidos lesionados', 'Formar bactérias', 'Produzir gametas'],
            "resposta": 'D',
        },
        {
            "texto": 'Na mitose, os cromossomos alinham-se no plano equatorial durante a:',
            "opcoes": ['Metáfase', 'Telófase', 'Prófase', 'Citocinese'],
            "resposta": 'A',
        },
        {
            "texto": 'O crossing-over ocorre durante a:',
            "opcoes": ['Anáfase II', 'Prófase I da meiose', 'Metáfase da mitose', 'Telófase I'],
            "resposta": 'B',
        },
        {
            "texto": 'Qual evento aumenta significativamente a variabilidade genética das populações?',
            "opcoes": ['Mitose', 'Reprodução assexuada', 'Meiose associada ao crossing-over', 'Fissão binária'],
            "resposta": 'C',
        },
        {
            "texto": 'Em um ecossistema protegido por unidades de conservação, peixes acumulam mercúrio ao longo da cadeia alimentar. Estudos indicam que a exposição excessiva à radiação pode causar alterações no DNA, enquanto a meiose contribui para a variabilidade genética das espécies. Qual alternativa relaciona corretamente esses conceitos?',
            "opcoes": ['A bioacumulação reduz a concentração de poluentes nos predadores de topo.', 'A meiose produz células geneticamente idênticas.', 'A radiação não apresenta aplicações benéficas para a sociedade.', 'A bioacumulação pode concentrar contaminantes nos organismos, enquanto a meiose promove variabilidade genética e a conservação ajuda a proteger os ecossistemas.'],
            "resposta": 'D',
        },
    ]
    return criar_perguntas_por_lista(dados)


def criar_perguntas_geografia():
    dados = [
        {
            "texto": 'O que significa a sigla ONU?',
            "opcoes": ['Organizacao Nacional Unificada Mundial', 'Organizacao das Nacoes Unidas', 'Organizacao Natural Urbana Global', 'Organizacao Nuclear Universal Internacional'],
            "resposta": 'B',
        },
        {
            "texto": 'Em que ano a ONU foi criada?',
            "opcoes": ['24 de março de 2001', '2 de outubro de 1981', '24 de outubro de 1945', '22 de agosto de 1990'],
            "resposta": 'C',
        },
        {
            "texto": 'Qual é a principal função da ONU?',
            "opcoes": ['Promover e manter paz', 'Criar empresas internacionais', 'Construir cidades pelo mundo', 'Produzir alimentos em massa'],
            "resposta": 'A',
        },
        {
            "texto": 'Quem faz parte da ONU?',
            "opcoes": ['paises membros da organizacao', 'Empresas multinacionais', 'Apenas paises ricos', 'Apenas paises da Europa'],
            "resposta": 'A',
        },
        {
            "texto": 'Qual órgão da ONU ajuda a combater a fome?',
            "opcoes": ['Mercosul', 'FAO', 'FIFA', 'OTAN'],
            "resposta": 'B',
        },
        {
            "texto": 'O que são territórios indígenas?',
            "opcoes": ['Áreas industriais', 'Áreas turísticas', 'Áreas militares', 'Áreas ocupadas por povos indígenas'],
            "resposta": 'D',
        },
        {
            "texto": 'O que os territórios indígenas ajudam a proteger?',
            "opcoes": ['Rodovias federais', 'Fabricas industriais', 'Matas e culturas', 'Aeroportos internacionais'],
            "resposta": 'C',
        },
        {
            "texto": 'Qual é um problema enfrentado por muitos povos indígenas?',
            "opcoes": ['Excesso de terras', 'Falta de cidades', 'Excesso de indústrias', 'Invasão de suas terras'],
            "resposta": 'D',
        },
        {
            "texto": 'Por que os territórios indígenas são importantes?',
            "opcoes": ['Conservam a natureza', 'Porque aumentam o desmatamento', 'Porque reduzem as florestas', 'Porque ocupam cidades'],
            "resposta": 'A',
        },
        {
            "texto": 'Os povos indígenas ajudam a:',
            "opcoes": ['Aumentar a poluição', 'Destruir florestas', 'Preservar a biodiversidade', 'Reduzir áreas verdes'],
            "resposta": 'C',
        },
        {
            "texto": 'O que significa a sigla ODS?',
            "opcoes": ['Organização dos Direitos Sociais', 'Ordem do Desenvolvimento Sustentável', 'Organização do Desenvolvimento Social', 'Objetivos de Desenvolvimento Sustentável'],
            "resposta": 'D',
        },
        {
            "texto": 'Quem criou os ODS?',
            "opcoes": ['FAO agricultura', 'OTAN', 'ONU', 'Mercosul'],
            "resposta": 'C',
        },
        {
            "texto": 'Os ODS fazem parte da:',
            "opcoes": ['Agenda 2030 ONU', 'Lei 2020 ONU', 'Federal 2050', 'Agenda Verde'],
            "resposta": 'A',
        },
        {
            "texto": 'Qual é o principal objetivo dos ODS?',
            "opcoes": ['Desenvolvimento sustentavel', 'Aumentar o desmatamento mundial', 'Criar guerras entre todos os paises', 'Favorecer apenas paises ricos'],
            "resposta": 'A',
        },
        {
            "texto": 'O ODS 2 trata de:',
            "opcoes": ['Saúde e bem-estar', 'Educação de qualidade', 'Energia limpa e acessível', 'Fome Zero e Agricultura Sustentável'],
            "resposta": 'D',
        },
        {
            "texto": 'Os ODS procuram equilibrar:',
            "opcoes": ['Tripe sustentavel', 'Apenas economia e sociedade', 'Apenas politica e economia', 'Apenas meio ambiente'],
            "resposta": 'A',
        },
        {
            "texto": 'Até que ano os ODS devem ser alcançados?',
            "opcoes": ['31 de dezembro de 2030', '2 de janeiro de 2025', '31 de março de 2040', '1 de abril de 2050'],
            "resposta": 'A',
        },
        {
            "texto": 'Qual destes temas faz parte dos ODS?',
            "opcoes": ['Aumento das guerras internacionais', 'Aumento da poluicao urbana', 'Erradicacao da pobreza', 'Expansao do desmatamento'],
            "resposta": 'C',
        },
        {
            "texto": 'O que os ODS incentivam?',
            "opcoes": ['A destruição das florestas', 'O uso responsável dos recursos naturais', 'O desperdício de água', 'A poluição dos rios'],
            "resposta": 'B',
        },
        {
            "texto": 'Por que proteger o meio ambiente é importante para os ODS?',
            "opcoes": ['Porque diminui a qualidade de vida', 'Porque aumenta a poluicao', 'Futuro sustentavel', 'Porque impede o desenvolvimento tecnologico'],
            "resposta": 'C',
        },
        {
            "texto": 'O que os ODS incentivam em relação à educação?',
            "opcoes": ['A educação apenas para adultos', 'A educação apenas para crianças', 'A educação de qualidade para todos', 'A educação apenas para países ricos'],
            "resposta": 'C',
        },
        {
            "texto": 'Qual dos temas abaixo está relacionado aos ODS?',
            "opcoes": ['Aumento das guerras', 'Expansão do desmatamento', 'Exploração sem limites dos recursos naturais', 'Igualdade de gênero'],
            "resposta": 'D',
        },
        {
            "texto": 'Qual alternativa representa melhor a ideia de desenvolvimento sustentável?',
            "opcoes": ['Equilibrar crescimento econômico, bem-estar social e preservação ambiental.', 'Preservar o meio ambiente sem desenvolver a economia.', 'Crescer economicamente sem se preocupar com o meio ambiente.', 'Priorizar apenas a produção agrícola.'],
            "resposta": 'A',
        },
        {
            "texto": 'O que os ODS incentivam em relação à energia?',
            "opcoes": ['O uso de energia apenas para países ricos', 'O uso de energia limpa e acessível para todos', 'O uso de energia apenas para indústrias', 'O uso de energia apenas para cidades'],
            "resposta": 'B',
        },
        {
            "texto": 'O que os ODS incentivam em relação à ação climática?',
            "opcoes": ['Ação para destruir florestas', 'Ação para aumentar a poluição', 'Ação para combater as mudanças climáticas e seus impactos', 'Ação para expandir o desmatamento'],
            "resposta": 'C',
        },
        {
            "texto": 'O que os ODS incentivam em relação à paz e justiça?',
            "opcoes": ['Injustiça apenas para países pobres', 'Guerra, injustiça e instituições corruptas para todos', 'Paz apenas para países ricos', 'Paz, justiça e instituições eficazes para todos'],
            "resposta": 'D',
        },
    ]
    return criar_perguntas_por_lista(dados)


def criar_perguntas_sociologia():
    dados = [
        {
            "texto": 'Quem é considerado o fundador da Sociologia como disciplina cientifica?',
            "opcoes": ['Auguste Comte', 'Max Weber alemao', 'Emile Durkheim', 'Karl Marx socialista'],
            "resposta": 'A',
        },
        {
            "texto": 'A Sociologia pode ser definida como:',
            "opcoes": ['O estudo dos astros e fenomenos da natureza', 'A ciencia que estuda os fenomenos, estruturas e relações sociais', 'A disciplina que analisa exclusivamente fenomenos economicos', 'O estudo do comportamento individual e psicologico'],
            "resposta": 'B',
        },
        {
            "texto": 'Em qual século a Sociologia surgiu como disciplina cientifica?',
            "opcoes": ['Seculo XIIV', 'Seculo XVII', 'Seculo XVIII', 'Seculo XIX'],
            "resposta": 'D',
        },
        {
            "texto": 'A Sociologia contribui para a sociedade ao:',
            "opcoes": ['Ignorar os conflitos e desigualdades sociais', 'Promover a compreensão critica das relações e estruturas sociais', 'Estudar apenas fenomenos biologicos do ser humano', 'Defender exclusivamente os interesses das classes dominantes'],
            "resposta": 'B',
        },
        {
            "texto": 'Qual e a principal utilidade da Sociologia para o cidadão?',
            "opcoes": ['Ensinar tecnicas de producao industrial', 'Focar apenas em culturas antigas', 'Compreender a sociedade', 'Estudar apenas economia global'],
            "resposta": 'C',
        },
        {
            "texto": 'A desigualdade social é caracterizada pela:',
            "opcoes": ['Distribuição desigual de recursos, oportunidades e poder na sociedade', 'Distribuição igualitária de riqueza entre todos os cidadãos', 'Garantia de acesso universal a educação e saúde', 'Eliminação das diferenças culturais entre grupos sociais'],
            "resposta": 'A',
        },
        {
            "texto": 'Qual das situações representa um exemplo de desigualdade social?',
            "opcoes": ['Diferenca de altura entre pessoas', 'Preferencias musicais distintas entre jovens', 'Acesso desigual a escola', 'Diferentes estilos de vestimenta entre culturas'],
            "resposta": 'C',
        },
        {
            "texto": 'A concentração de renda e oportunidades nas mãos de poucos é:',
            "opcoes": ['fator que aprofunda a desigualdade social', 'diferencas biologicas', 'escolhas individuais', 'fenomeno sem efeito na educacao e saude'],
            "resposta": 'A',
        },
        {
            "texto": 'A estratificação social refere-se á:',
            "opcoes": ['Analise das diferentes culturas ao redor do mundo', 'Relacao economica entre paises desenvolvidos e subdesenvolvidos', 'Divisao em classes sociais', 'Processo de urbanizacao das grandes cidades modernas'],
            "resposta": 'C',
        },
        {
            "texto": 'Qual critério e usado para definir a posição de um individuo na estratificação social?',
            "opcoes": ['Cor dos olhos', 'Altura e peso', 'Tipo sanguineo', 'Renda, prestigio e poder'],
            "resposta": 'D',
        },
        {
            "texto": 'Segundo Durkheim, fato social é:',
            "opcoes": ['Qualquer ação individual motivada por sentimentos pessoais', 'Uma maneira de agir exterior ao individuo que exerce coerção sobre ele', 'O estudo do comportamento animal em sociedade', 'A analise de fenômenos naturais como terremotos e enchentes'],
            "resposta": 'B',
        },
        {
            "texto": 'Quais são as 3 caracteristicas do fato social segundo Durkheim?',
            "opcoes": ['Subjetividade, liberdade e individualidade humana', 'Criatividade, espontaneidade e emotividade social', 'Exterior, coercitivo e geral', 'Racionalidade, liberdade e subjetividade individual'],
            "resposta": 'C',
        },
        {
            "texto": 'A coercitividade do fato social significa que:',
            "opcoes": ['O individuo cria suas proprias normas sociais livremente', 'As normas sociais são impostas ao individuo independentemente de sua vontade', 'Cada pessoa interpreta e aplica as regras da maneira que desejar', 'As normas sociais são sempre negociadas entre os membros da sociedade'],
            "resposta": 'B',
        },
        {
            "texto": 'Para Durkheim, os fatos sociais devem ser estudados:',
            "opcoes": ['Como coisas, de forma objetiva e cientifica', 'Apenas por meio da introspecção e da experiência pessoal', 'Exclusivamente pela filosofia e pela teologia', 'Como fenômenos subjetivos e estritamente individuais'],
            "resposta": 'A',
        },
        {
            "texto": 'Qual das alternativas representa um exemplo de fato social?',
            "opcoes": ['Decisão pessoal de comer sorvete', 'Preferência por cor de roupa', 'obrigação social de usar roupas em espaços públicos', 'Sonho durante o sono'],
            "resposta": 'C',
        },
        {
            "texto": 'Para Max Weber, ação social é:',
            "opcoes": ['Acao com sentido social', 'Normas e regras impostas pela sociedade', 'Qualquer comportamento humano', 'Acoes coletivas em grandes grupos'],
            "resposta": 'A',
        },
        {
            "texto": 'Qual alternativa apresenta os 4 tipos de ação social de Weber?',
            "opcoes": ['Economica, politica, cultural e religiosa', 'Racional com relação a fins, racional com relação a valores, afetiva e tradicional', 'Individual, coletiva, normativa e espontânea', 'Consciente, inconsciente, voluntária e involuntaria'],
            "resposta": 'B',
        },
        {
            "texto": 'Uma ação motivada por habitos transmitidos de geração em geração e classificada por Weber como:',
            "opcoes": ['Acao racional com relacao a fins', 'Acao racional com relacao a valores', 'Acao afetiva imediata', 'Acao tradicional'],
            "resposta": 'D',
        },
        {
            "texto": 'Segundo Marx, a alienação do trabalho ocorre quando:',
            "opcoes": ['O trabalhador tem total controle sobre o produto de seu trabalho', 'O trabalhador se sente plenamente realizado com sua atividade produtiva', 'As empresas distribuem os lucros igualmente entre os funcionários', 'O trabalhador e separado do produto de seu trabalho e não se reconhece nele'],
            "resposta": 'D',
        },
        {
            "texto": 'Para Marx, a mais-valia representa:',
            "opcoes": ['Salario extra por horas adicionais', 'Mais-valia', 'Lucro distribuido igualmente entre capitalistas e trabalhadores', 'Valor total de mercado de uma mercadoria industrializada'],
            "resposta": 'B',
        },
        {
            "texto": 'O conceito de desencantamento do mundo foi desenvolvido por:',
            "opcoes": ['Karl Marx', 'Emile Durkheim', 'Max Weber', 'Auguste Comte'],
            "resposta": 'C',
        },
        {
            "texto": 'Para Weber, o desencantamento do mundo refere-se ao processo em que:',
            "opcoes": ['O pensamento cientifico entra em declinio frente a religião', 'As crenças religiosas aumentam e se fortalecem na modernidade', 'As sociedades modernas retornam as praticas e tradições primitivas', 'A racionalidade e a ciencia substituem as explicações magicas e religiosas'],
            "resposta": 'D',
        },
        {
            "texto": 'O processo de racionalização de Weber esta ligado a:',
            "opcoes": ['A expansão da burocracia, da ciencia e do capitalismo moderno', 'O aumento da influencia da religião na politica moderna', 'O retorno as tradicoes e aos valores medievais', 'A redução da produção industrial nos paises desenvolvidos'],
            "resposta": 'A',
        },
        {
            "texto": 'Uma das consequências do desencantamento do mundo segundo Weber é:',
            "opcoes": ['O fortalecimento das praticas religiosas como principal guia da vida social', 'A perda de sentido e a jaula de ferro da burocracia e da racionalidade', 'O retorno ao pensamento magico como forma de explicar o mundo', 'A eliminação total das desigualdades sociais por meio da razão'],
            "resposta": 'B',
        },
        {
            "texto": 'De acordo com Weber, o capitalismo moderno e marcado por:',
            "opcoes": ['Relações baseadas em laços pessoais, emocionais e de lealdade', 'A predominancia de valores religiosos sobre os interesses economicos', 'A racionalidade formal, a burocracia e o calculo sistematico', 'A distribuição igualitaria dos meios de produção entre os trabalhadores'],
            "resposta": 'C',
        },
        {
            "texto": 'Considere os conceitos fundamentais da Sociologia: o fato social de Durkheim, a ação social e o desencantamento do mundo de Weber, e a alienação do trabalho de Marx. Qual alternativa relaciona corretamente esses conceitos com a sociedade contemporânea?',
            "opcoes": ['O fato social e uma ação subjetiva e individual; a ação social de Weber ignora o sentido dado pelo sujeito; a alienação representa a realização do trabalhador.', 'O desencantamento do mundo fortalece as explicacoes mágicas e religiosas; a ação social e sempre irracional e impulsiva; o fato social e criado livremente pelo individuo sem qualquer pressao externa.', 'Durkheim e Marx defendem que a sociedade e guiada apenas por forças economicas; Weber nega qualquer influencia da religião na vida social; a alienação representa a liberdade e realização plena do trabalhador.', 'Durkheim defende que os fatos sociais são exteriores e coercitivos; Weber analisa as ações sociais pelos seus significados; Marx aponta que o trabalhador se aliena ao perder o controle sobre seu trabalho; e Weber descreve como a racionalização transforma as relações sociais modernas.'],
            "resposta": 'D',
        },
    ]
    return criar_perguntas_por_lista(dados)


def criar_perguntas_quimica():
    dados = [
        {
            "texto": 'Qual das alternativas abaixo é um combustível biodegradável?',
            "opcoes": ['biodiesel', 'gasolina comum', 'diesel', 'carvao mineral'],
            "resposta": 'A',
        },
        {
            "texto": 'Escolha uma alternativa que fale uma vantagem do combustível biodegradável.',
            "opcoes": ['Pode elevar o preco dos alimentos.', 'Custo por litro ainda maior que o da gasolina.', 'Impacto socioeconomico: fomenta a agricultura local, gera empregos e diversifica a matriz economica.', 'Pode degradar com umidade no armazenamento.'],
            "resposta": 'C',
        },
        {
            "texto": 'Qual combustível biodegradável tem o melhor custo financeiro?',
            "opcoes": ['biodiesel', 'Etanol', 'Biometano', 'Carvão mineral'],
            "resposta": 'B',
        },
        {
            "texto": 'Escolha a alternativa onde tenha apenas combustíveis biodegradáveis.',
            "opcoes": ['Biogas, biodiesel, diesel verde, carvao mineral', 'Etanol, petroleo, carvao mineral, biogas', 'Etanol, biogas, biodiesel e diesel verde renovavel', 'Gas natural, petroleo, diesel verde, etanol'],
            "resposta": 'C',
        },
        {
            "texto": 'Qual é o biocombustível mais utilizado no Brasil?',
            "opcoes": ['Etanol', 'Biodiesel', 'Diesel verde', 'Carvao vegetal'],
            "resposta": 'A',
        },
        {
            "texto": 'Qual destes materiais pode ser reciclável?',
            "opcoes": ['Espelho', 'Guardanapo', 'Caixa de papelao', 'Caixa de pizza'],
            "resposta": 'C',
        },
        {
            "texto": 'Qual é a sequencia certa para a reciclagem?',
            "opcoes": ['Coleta, transformacao, realocacao e triagem', 'Coleta, triagem, transformacao, realocacao', 'Coleta, realocacao, triagem e transformacao', 'Coleta, triagem, realocacao e transformacao'],
            "resposta": 'B',
        },
        {
            "texto": 'Qual das cores abaixo é da lixeira de plástico?',
            "opcoes": ['Amarelo', 'Verde', 'Azul', 'Vermelho'],
            "resposta": 'D',
        },
        {
            "texto": 'Quais são as cores principais das lixeiras para a reciclagem?',
            "opcoes": ['Vermelha, preto, laranja, marrom e verde', 'Azul, vermelha, verde, laranja e roxo comum', 'Azul, verde, vermelha, amarela, marrom', 'Azul, verde, vermelha, laranja e marrom comum'],
            "resposta": 'C',
        },
        {
            "texto": 'Qual das alternativas abaixo é a cor da lixeira para reciclar madeira?',
            "opcoes": ['Branco', 'Azul', 'Roxo', 'Escuro'],
            "resposta": 'D',
        },
        {
            "texto": 'O aterro sanitário é...',
            "opcoes": ['Um ponto de coleta para equipamentos elétricos e eletrônicos obsoletos.', 'Uma formação geológica costeira rochosa próxima à costa.', 'Uma obra de engenharia projetada para a disposição final segura de resíduos sólidos urbanos.', 'Um espaço público gratuito para receber recicláveis e grandes resíduos.'],
            "resposta": 'C',
        },
        {
            "texto": 'O funcionamento do aterro sanitário segue um processo contínuo e técnico. Qual é a sequência correta?',
            "opcoes": ['Compactar e cobrir antes de receber, pesar, drenar chorume e captar gases sem ordem técnica', 'Construir células, compactar, pesar, monitorar, captar gases e só depois receber resíduos', 'Receber, criar células, compactar/cobrir, drenar chorume, monitorar, captar gases', 'Receber, construir células, compactar, drenar chorume, encerrar e deixar gases sem captação correta'],
            "resposta": 'C',
        },
        {
            "texto": 'Quanto tempo dura um aterro sanitário?',
            "opcoes": ['pode durar até 10 anos', 'menos de 15 anos', 'exatamente 27 anos', 'pode durar até 5 anos'],
            "resposta": 'A',
        },
        {
            "texto": 'Qual gás é produzido em grande quantidade pela decomposição da matéria orgânica em aterros sanitários?',
            "opcoes": ['Oxigênio (O2)', 'Hidrogênio (H2)', 'Nitrogênio (N2)', 'Metano (CH4)'],
            "resposta": 'D',
        },
        {
            "texto": 'Qual das alternativas apresenta uma medida que reduz a quantidade de resíduos destinados aos aterros sanitários?',
            "opcoes": ['Aumento do descarte de recicláveis no lixo comum.', 'Incentivo à reciclagem e compostagem dos resíduos orgânicos.', 'Construção de mais lixões.', 'Queima de todo o lixo produzido.'],
            "resposta": 'B',
        },
        {
            "texto": 'Qual efeito está mais diretamente associado ao uso intensivo de combustíveis fósseis em escala global?',
            "opcoes": ['Reducao da concentracao atmosferica de dioxido de carbono', 'Aumento do aquecimento global', 'Neutralizacao dos impactos climaticos por vapor dagua', 'Estabilizacao das temperaturas medias globais'],
            "resposta": 'B',
        },
        {
            "texto": 'Um dos principais riscos socioambientais relacionados à exploração petrolífera em áreas oceânicas é:',
            "opcoes": ['A ampliação imediata da biodiversidade marinha.', 'A redução permanente da salinidade dos oceanos.', 'A contaminação de ecossistemas aquáticos por derramamentos de petróleo e derivados.', 'A formação acelerada de recifes de corais.'],
            "resposta": 'C',
        },
        {
            "texto": 'A dependência econômica de combustíveis fósseis pode gerar impactos sociais porque:',
            "opcoes": ['Estabilidade economica garantida aos exportadores de petroleo', 'Fim da necessidade de investir em outras fontes energeticas', 'Conflitos e desigualdade energetica', 'Fim das oscilacoes nos precos dos combustiveis e da energia'],
            "resposta": 'C',
        },
        {
            "texto": 'A formação da chuva ácida está relacionada principalmente à emissão de quais substâncias?',
            "opcoes": ['Óxidos de enxofre e óxidos de nitrogênio liberados durante a combustão de combustíveis fósseis.', 'Gás carbônico e oxigênio provenientes da fotossíntese.', "Metano e vapor d'água emitidos por atividades agrícolas.", 'Hidrogênio e hélio resultantes da decomposição da matéria orgânica.'],
            "resposta": 'A',
        },
        {
            "texto": 'Sob a perspectiva da sustentabilidade, por que a substituição gradual dos combustíveis fósseis por fontes renováveis é defendida?',
            "opcoes": ['Elimina completamente os impactos ambientais da energia', 'Menores emissoes e menos dependencia', 'Dispensa planejamento energetico de longo prazo', 'Garante impacto ambiental nulo em toda energia renovavel'],
            "resposta": 'B',
        },
        {
            "texto": 'Um combustível apresenta elevado poder calorífico, mas é utilizado em um sistema com baixo rendimento térmico. Sobre sua eficiência energética, é correto afirmar que:',
            "opcoes": ['O alto poder calorífico garante maior aproveitamento energético independentemente das perdas.', 'A eficiência energética depende exclusivamente da energia química armazenada no combustível.', 'O aproveitamento energético efetivo resulta da interação entre a energia disponível no combustível e a capacidade do sistema de convertê-la em trabalho útil.', 'O rendimento térmico influencia apenas o consumo de combustível.'],
            "resposta": 'C',
        },
        {
            "texto": 'Em uma análise energética completa, por que o EROEI de um combustível é considerado relevante?',
            "opcoes": ['Expressa apenas a energia liberada por unidade de massa do combustível.', 'Mede exclusivamente a eficiência do equipamento consumidor de energia.', 'Determina a quantidade de poluentes emitidos durante a combustão.', 'Relaciona a energia obtida ao investimento energético necessário para disponibilizar o combustível para uso.'],
            "resposta": 'D',
        },
        {
            "texto": 'Dois combustíveis apresentam valores semelhantes de poder calorífico. Ainda assim, um deles pode apresentar melhor desempenho energético global porque:',
            "opcoes": ['A eficiência global é influenciada por fatores como processamento, transporte e conversão da energia em trabalho útil.', 'Combustíveis com poder calorífico semelhante possuem obrigatoriamente a mesma eficiência energética.', 'O desempenho energético depende apenas da estabilidade química do combustível.', 'O rendimento energético é determinado exclusivamente pela massa consumida.'],
            "resposta": 'A',
        },
        {
            "texto": 'Um combustível de alta densidade energética pode não representar a melhor opção sob a ótica da eficiência energética global quando:',
            "opcoes": ['Seu armazenamento ocorre em condições controladas.', 'A energia necessária para sua obtenção, processamento e distribuição reduz significativamente o ganho energético líquido.', 'Seu poder calorífico é superior ao de outros combustíveis.', 'Sua combustão ocorre de maneira completa.'],
            "resposta": 'B',
        },
        {
            "texto": 'Considerando a eficiência energética como a relação entre energia útil obtida e energia total disponível, qual situação representa o maior desafio para maximizar essa eficiência?',
            "opcoes": ['A utilização de combustíveis com elevado conteúdo energético em sistemas de conversão altamente eficientes.', 'A redução das perdas energéticas durante as etapas de transformação e utilização da energia.', 'A ocorrência de perdas térmicas inevitáveis associadas aos limites impostos pelas leis da termodinâmica.', 'O aumento da densidade energética do combustível sem alterações no sistema de conversão.'],
            "resposta": 'C',
        },
        {
            "texto": 'A reciclagem é uma estratégia importante para a gestão sustentável dos resíduos sólidos. Com base nesse princípio, assinale a alternativa correta:',
            "opcoes": ['A reciclagem tende a apresentar maior benefício ambiental quando substitui matérias-primas virgens, independentemente da energia consumida em seu processamento.', 'O desempenho ambiental da reciclagem está relacionado principalmente à capacidade tecnológica de transformar resíduos em novos produtos.', 'A reciclagem garante redução dos impactos ambientais sempre que a taxa de recuperação ultrapassa determinado valor percentual.', 'A eficiência ambiental da reciclagem depende do equilíbrio entre a recuperação de materiais e os impactos associados às etapas de coleta, transporte e reprocessamento.'],
            "resposta": 'D',
        },
    ]
    return criar_perguntas_por_lista(dados)

# Perguntas em branco para edição posterior, e usado em testes, decidi manter, mas pode ser removido


def criar_perguntas_em_branco():
    dados = []
    for _ in PREMIOS:
        dados.append({
            "texto": "(pergunta)",
            "opcoes": ["(resposta)", "(resposta)", "(resposta)", "(resposta)"],
            "resposta": "A",
        })
    return criar_perguntas_por_lista(dados)


def selecionar_tema():
    temas = {
        "1": ("LÍNGUA PORTUGUESA", criar_perguntas),
        "2": ("MATEMÁTICA", criar_perguntas_matematica),
        "3": ("HISTÓRIA", criar_perguntas_historia),
        "4": ("GEOGRAFIA", criar_perguntas_geografia),
        "5": ("SOCIOLOGIA", criar_perguntas_sociologia),
        "6": ("BIOLOGIA", criar_perguntas_biologia),
        "7": ("FÍSICA", criar_perguntas_fisica),
        "8": ("QUÍMICA", criar_perguntas_quimica),
    }

    while True:
        print("\nESCOLHA O TEMA")
        for codigo, (nome, _) in temas.items():
            print(f"{codigo} - {nome}")
        escolha = input("Tema: ").strip()
        if escolha in temas:
            nome, criar_perguntas_do_tema = temas[escolha]
            print(f"\nTema escolhido: {nome}")
            return nome, criar_perguntas_do_tema()
        print("Tema invalido. Digite um numero de 1 a 8.")


def exibir_pergunta(pergunta, opcoes_visiveis):
    print("Pergunta:", pergunta["texto"])
    letras = ["A", "B", "C", "D"]
    for letra, resposta in zip(letras, pergunta["opcoes"]):
        if letra in opcoes_visiveis:
            print(f"  {letra}) {resposta}")
    print()


def escolher_lifeline(lifelines_disponiveis):
    print("Lifelines disponíveis:")
    for codigo, descricao in lifelines_disponiveis.items():
        print(f"  {codigo} - {descricao}")
    print("Digite a letra da lifeline que deseja usar ou Enter para voltar.")
    escolha = input("Lifeline: ").strip().upper()
    return escolha


def aplicar_5050(pergunta, opcoes_visiveis):
    alternativas = ["A", "B", "C", "D"]
    corretas = [
        alternativa for alternativa in alternativas if alternativa == pergunta["resposta"]]
    erradas = [
        alternativa for alternativa in alternativas if alternativa != pergunta["resposta"]]
    removidas = random.sample(erradas, 2)
    for removida in removidas:
        if removida in opcoes_visiveis:
            opcoes_visiveis.remove(removida)
    print("50-50 usado: duas alternativas incorretas foram removidas.")
    return opcoes_visiveis


def aplicar_pedir_publico(pergunta):
    percentual = {"A": 25, "B": 25, "C": 25, "D": 25}
    opcao_correta = pergunta["resposta"]
    percentual[opcao_correta] = 60
    restante = 40
    outras = [op for op in percentual if op != opcao_correta]
    for i, opcao in enumerate(outras):
        percentual[opcao] = restante // (len(outras) - i)
        restante -= percentual[opcao]
    print("Pesquisa do público: probabilidade estimada")
    for opcao, valor in percentual.items():
        print(f"  {opcao}: {valor}%")
    print()


def aplicar_pular(pergunta_index, perguntas):
    if pergunta_index + 1 < len(perguntas):
        print("Você pulou esta pergunta. A próxima será apresentada.")
        return pergunta_index + 1
    print("Não é possível pular a última pergunta.")
    return pergunta_index


def calcular_garantia(perguntas_respondidas):
    if perguntas_respondidas >= 25:
        return 500000
    if perguntas_respondidas >= 20:
        return 250000
    if perguntas_respondidas >= 15:
        return 125000
    if perguntas_respondidas >= 10:
        return 32000
    if perguntas_respondidas >= 5:
        return 1000
    return 0


def exibir_resumo_final(nome, serie, tema, perguntas_respondidas, premio_final, lifelines_usadas, resultado):
    print("\n" + "=" * 40)
    print("RESUMO DA PARTIDA")
    print("=" * 40)
    print(f"Jogador: {nome}")
    print(f"Série: {serie}")
    print(f"Tema: {tema}")
    print(f"Resultado: {resultado}")
    print(f"Acertos: {perguntas_respondidas}/{len(PREMIOS)}")
    print(f"Prêmio final: R$ {premio_final}")
    print(
        "Ajudas usadas:",
        "Nenhuma" if not lifelines_usadas else ", ".join(lifelines_usadas),
    )
    print("=" * 40)


def jogar():
    nome, idade, serie = solicitar_dados_jogador()
    tema, perguntas = selecionar_tema()
    exibir_titulo(nome, serie, tema)
    lifelines = {
        "1": "50-50",
        "2": "Pedir ao público",
        "3": "Pular pergunta",
    }
    lifelines_usadas = []
    premio_atual = 0
    premio_final = 0
    resultado = "Jogo encerrado"
    pergunta_index = 0
    perguntas_respondidas = 0
    opcoes_visiveis = ["A", "B", "C", "D"]
    ultima_pergunta_index = None

    while pergunta_index < len(perguntas):
        try:
            pergunta = perguntas[pergunta_index]
            if pergunta_index != ultima_pergunta_index:
                opcoes_visiveis = ["A", "B", "C", "D"]
                ultima_pergunta_index = pergunta_index
            if pergunta_index == len(perguntas) - 1:
                bloco_texto = "Bloco Final"
                pergunta_no_bloco = 1
                total_no_bloco = 1
            else:
                bloco = pergunta_index // 5 + 1
                bloco_texto = f"Bloco {bloco}"
                pergunta_no_bloco = pergunta_index % 5 + 1
                total_no_bloco = 5

            print(
                f"\n{bloco_texto}, Pergunta {pergunta_no_bloco}/{total_no_bloco} - Nível {pergunta_index + 1} - Prêmio: R$ {pergunta['premio']}")
            exibir_pergunta(pergunta, opcoes_visiveis)

            suspense_channel = tocar_suspense()
            resposta = input(
                "Digite sua resposta (A/B/C/D) ou 'L' para lifeline, 'S' para sair: ").strip().upper()
            parar_suspense(suspense_channel)

            if resposta == "":
                print("Resposta inválida. Digite A, B, C, D, L ou S.")
                continue
        except (EOFError, KeyboardInterrupt):
            return

        if resposta == "S":
            premio_final = premio_atual
            resultado = "Saiu do jogo"
            print("Você saiu do jogo com R$", premio_atual)
            break
        if resposta == "L":
            if not lifelines:
                print("Não há lifelines disponíveis.")
                continue
            escolha = escolher_lifeline(lifelines)
            if escolha == "":
                continue
            if escolha not in lifelines:
                print("Lifeline inválida. Tente novamente.")
                continue
            nova_posicao = pergunta_index
            if escolha == "1":
                opcoes_visiveis = aplicar_5050(pergunta, opcoes_visiveis)
            elif escolha == "2":
                aplicar_pedir_publico(pergunta)
            elif escolha == "3":
                nova_posicao = aplicar_pular(pergunta_index, perguntas)
            tocar_som("lifeline")
            lifelines_usadas.append(lifelines[escolha])
            del lifelines[escolha]
            if nova_posicao != pergunta_index:
                pergunta_index = nova_posicao
                continue
            continue
        if resposta not in ["A", "B", "C", "D"]:
            print("Resposta inválida. Digite A, B, C, D, L ou S.")
            continue
        if resposta == pergunta["resposta"]:
            premio_atual = pergunta["premio"]
            perguntas_respondidas += 1
            tocar_som("correct")
            print("Resposta correta! Você ganhou R$", premio_atual)
            pergunta_index += 1
            if pergunta_index == len(perguntas):
                premio_final = premio_atual
                resultado = "Venceu o jogo"
                tocar_som("win")
                print("Parabéns! Você venceu o jogo e alcançou R$", premio_atual)
                break
        else:
            tocar_som("wrong")
            tocar_som("game_over")
            garantia = calcular_garantia(perguntas_respondidas)
            premio_final = garantia
            resultado = "Game over"
            print("Resposta incorreta. GAME OVER.")
            print("Você deixa o jogo com R$", garantia)
            break
    if pergunta_index >= len(perguntas):
        print("Fim de jogo. Obrigado por jogar!")
    exibir_resumo_final(
        nome,
        serie,
        tema,
        perguntas_respondidas,
        premio_final,
        lifelines_usadas,
        resultado,
    )


def main():
    try:
        while True:
            opcao = exibir_menu_inicial()
            if opcao == "1":
                jogar()
            elif opcao == "2":
                exibir_instrucoes()
            elif opcao == "3":
                exibir_ranking()
            elif opcao == "4":
                print("Até a próxima!")
                break
            else:
                print("Opção inválida. Digite 1, 2, 3 ou 4.")
    except (EOFError, KeyboardInterrupt):
        print("\nJogo encerrado.")
    finally:
        if not sys.stdin.isatty():
            input("Pressione Enter para sair...")


if __name__ == "__main__":
    main()
