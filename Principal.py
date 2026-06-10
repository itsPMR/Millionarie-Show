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
    print("#          SHOW DO MILIONARIO          #")
    print("#" * 40)
    print("1 - Jogar")
    print("2 - Instrucoes")
    print("3 - Ranking")
    print("4 - Sair")
    print()
    return input("Escolha uma opcao: ").strip()


def exibir_instrucoes():
    print("\nINSTRUCOES")
    print("Ao iniciar, escolha um tema para jogar.")
    print("Responda as perguntas digitando A, B, C ou D.")
    print("Digite L durante uma pergunta para usar uma ajuda.")
    print("Digite S durante uma pergunta para sair do jogo.")
    print("As ajudas disponiveis sao: 50-50, pedir ao publico e pular pergunta.")
    print("Quanto mais perguntas acertar, maior sera o premio.\n")


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
        serie = input("Digite sua serie escolar: ").strip()
        if serie:
            break
        print("Serie escolar nao pode ficar em branco.")

    print(
        f"\nOlá, {nome}! Idade registrada: {idade} anos. Serie escolar: {serie}.")
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
            "texto": "Identifique a oração em destaque cujo sujeito é indeterminado.",
            "opcoes": ["Está garoando.", "Ligaram para saber como você se sente.", "Aluga-se casa.", "Faz anos que não falo com ele"],
            "resposta": "C",
            "premio": 100,
        },
        {
            "texto": "Qual sinal de pontuação encerra uma frase interrogativa?",
            "opcoes": ["Ponto final", "Vírgula", "Ponto e vírgula", "Ponto de interrogação"],
            "resposta": "D",
            "premio": 200,
        },
        {
            "texto": "Qual sinal indica surpresa ou emoção forte?",
            "opcoes": ["Vírgula", "Ponto de exclamação", "Dois pontos", "Reticências"],
            "resposta": "B",
            "premio": 300,
        },
        {
            "texto": "Ao localizar fatos no texto, o leitor deve buscar informações que sejam:",
            "opcoes": ["interpretadas", "subentendidas", "exatas", "aleatórias"],
            "resposta": "C",
            "premio": 500,
        },
        {
            "texto": "Ler entrelinhas permite identificar:",
            "opcoes": ["dados explícitos", "sentimentos ocultos", "números no texto", "correções gramaticais"],
            "resposta": "B",
            "premio": 1000,
        },
        {
            "texto": "Uma mensagem subentendida depende principalmente de:",
            "opcoes": ["pontuação", "contexto", "grifo", "corpo do texto"],
            "resposta": "B",
            "premio": 2000,
        },
        {
            "texto": "O uso de ponto e vírgula geralmente liga orações que são:",
            "opcoes": ["independentes", "opostas", "relacionadas", "alternativas"],
            "resposta": "C",
            "premio": 3000,
        },
        {
            "texto": "A frase que termina com ponto final é normalmente:",
            "opcoes": ["interrogativa", "exclamativa", "declarativa", "incompleta"],
            "resposta": "C",
            "premio": 5000,
        },
        {
            "texto": "Qual elemento mostra que o autor escreveu com emoção forte?",
            "opcoes": ["palavras longas", "ponto final", "ponto de interrogação", "ponto de exclamação"],
            "resposta": "D",
            "premio": 10000,
        },
        {
            "texto": "Identificar personagens significa lembrar:",
            "opcoes": ["nomes exatos", "sons das palavras", "cores favoritas", "número de letras"],
            "resposta": "A",
            "premio": 15000,
        },
        {
            "texto": "Qual alternativa descreve melhor um fato no texto?",
            "opcoes": ["opinião do narrador", "informação apresentada", "sensação pessoal", "predição futura"],
            "resposta": "B",
            "premio": 25000,
        },
        {
            "texto": "Uma pergunta como 'Você gostou?' termina com:",
            "opcoes": ["ponto final", "vírgula", "reticências", "ponto de interrogação"],
            "resposta": "D",
            "premio": 50000,
        },
        {
            "texto": "Ao encontrar dados no texto, o leitor deve procurar informações que estejam:",
            "opcoes": ["implícitas", "explicitamente escritas", "em outras fontes", "omitidas"],
            "resposta": "B",
            "premio": 75000,
        },
        {
            "texto": "A frase 'Não foi apenas um dia triste' sugere:",
            "opcoes": ["alegria evidente", "sentimento oculto", "fato isolado", "ordem direta"],
            "resposta": "B",
            "premio": 100000,
        },
        {
            "texto": "Qual sinal é usado para separar itens complexos em uma lista?",
            "opcoes": ["ponto final", "vírgula", "ponto e vírgula", "três pontos"],
            "resposta": "C",
            "premio": 150000,
        },
        {
            "texto": "Uma causa de um acontecimento costuma aparecer antes do:",
            "opcoes": ["efeito", "título", "subtítulo", "sumário"],
            "resposta": "A",
            "premio": 250000,
        },
        {
            "texto": "A leitura entrelinhas ajuda a perceber:",
            "opcoes": ["a cor do texto", "o tipo de fonte", "o sentimento não dito", "a margem do papel"],
            "resposta": "C",
            "premio": 350000,
        },
        {
            "texto": "No texto, a informação que deve ser localizada exatamente é:",
            "opcoes": ["um fato", "uma opinião", "um adjetivo", "uma adivinhação"],
            "resposta": "A",
            "premio": 500000,
        },
        {
            "texto": "O uso correto de pontuação faz o texto ficar mais:",
            "opcoes": ["confuso", "claro", "curto", "longo"],
            "resposta": "B",
            "premio": 600000,
        },
        {
            "texto": "Quando se fala em mensagem subentendida, procura-se o que está:",
            "opcoes": ["escrito em negrito", "muito destacado", "sugerido no texto", "faltando no texto"],
            "resposta": "C",
            "premio": 700000,
        },
        {
            "texto": "Qual recurso textual cria suspense sem afirmar diretamente?",
            "opcoes": ["descrição clara", "afirmação direta", "sugestão indireta", "questionamento"],
            "resposta": "C",
            "premio": 780000,
        },
        {
            "texto": "Quando um personagem fala de forma indireta, há:",
            "opcoes": ["uma descrição literal", "uma instrução explícita", "uma mensagem subentendida", "um dado numérico"],
            "resposta": "C",
            "premio": 820000,
        },
        {
            "texto": "Qual pontuação é usada antes de uma explicação adicional?",
            "opcoes": ["vírgula", "dois pontos", "ponto final", "aspas"],
            "resposta": "B",
            "premio": 860000,
        },
        {
            "texto": "A leitura entrelinhas revela geralmente:",
            "opcoes": ["um número exato", "uma sensação oculta", "uma lista de itens", "um título evidente"],
            "resposta": "B",
            "premio": 900000,
        },
        {
            "texto": "Dados exatos no texto devem ser localizados de forma:",
            "opcoes": ["imprecisa", "literal", "aproximada", "aleatória"],
            "resposta": "B",
            "premio": 950000,
        },
        {
            "texto": "Qual pontuação liga duas ideias relacionadas dentro da mesma frase?",
            "opcoes": ["ponto final", "vírgula", "ponto e vírgula", "dois pontos"],
            "resposta": "C",
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
        {"texto": "Na equação ax² + bx + c = 0, qual expressão representa o delta?",
            "opcoes": ["b² - 4ac", "a² - 4bc", "2a + b", "b - 4ac"], "resposta": "A"},
        {"texto": "Se o delta de uma equação do segundo grau é maior que zero, ela possui:", "opcoes": [
            "nenhuma raiz real", "uma raiz real", "duas raízes reais diferentes", "duas raízes iguais e não reais"], "resposta": "C"},
        {"texto": "Se o delta é igual a zero, a equação do segundo grau possui:", "opcoes": [
            "duas raízes reais iguais", "duas raízes reais diferentes", "nenhuma raiz", "três raízes"], "resposta": "A"},
        {"texto": "Se o delta é menor que zero, a equação do segundo grau possui:", "opcoes": [
            "duas raízes reais", "uma raiz real", "nenhuma raiz real", "infinitas raízes reais"], "resposta": "C"},
        {"texto": "Na fórmula de Bhaskara, o denominador é:",
            "opcoes": ["2a", "2b", "4a", "a²"], "resposta": "A"},
        {"texto": "Na equação x² - 5x + 6 = 0, os coeficientes a, b e c são:",
            "opcoes": ["1, -5 e 6", "-1, 5 e 6", "1, 5 e -6", "0, -5 e 6"], "resposta": "A"},
        {"texto": "Uma equação do segundo grau completa possui:", "opcoes": [
            "apenas ax²", "apenas bx", "a, b e c diferentes de zero", "somente c"], "resposta": "C"},
        {"texto": "A equação x² - 9 = 0 é chamada de incompleta porque:", "opcoes": [
            "não tem termo bx", "não tem termo ax²", "não tem termo c", "não tem igualdade"], "resposta": "A"},
        {"texto": "A equação 2x² = 0 tem como raiz:",
            "opcoes": ["0", "1", "2", "-2"], "resposta": "A"},
        {"texto": "Em uma função do primeiro grau f(x) = ax + b, o número a representa:", "opcoes": [
            "coeficiente angular", "termo independente", "raiz da função", "valor máximo"], "resposta": "A"},
        {"texto": "Em f(x) = 3x + 2, o termo independente é:",
         "opcoes": ["3", "2", "x", "5"], "resposta": "B"},
        {"texto": "Uma função do primeiro grau tem gráfico em forma de:", "opcoes": [
            "parábola", "reta", "círculo", "hipérbole"], "resposta": "B"},
        {"texto": "Se a > 0 em f(x) = ax + b, a função é:", "opcoes": [
            "crescente", "decrescente", "constante", "quadrática"], "resposta": "A"},
        {"texto": "Se a < 0 em f(x) = ax + b, a função é:", "opcoes": [
            "crescente", "decrescente", "sempre positiva", "sem gráfico"], "resposta": "B"},
        {"texto": "A raiz da função f(x) = 2x - 6 é:",
         "opcoes": ["2", "3", "6", "-3"], "resposta": "B"},
        {"texto": "Modelar uma função do primeiro grau significa:", "opcoes": [
            "criar uma regra linear para uma situação", "desenhar uma parábola", "calcular apenas delta", "eliminar o eixo y"], "resposta": "A"},
        {"texto": "Se um táxi cobra R$ 5 fixos mais R$ 2 por km, a função do preço é:", "opcoes": [
            "P(x) = 5x + 2", "P(x) = 2x + 5", "P(x) = x² + 5", "P(x) = 7x"], "resposta": "B"},
        {"texto": "Na função P(x) = 2x + 5, se x = 10, o valor de P(x) é:",
         "opcoes": ["15", "20", "25", "30"], "resposta": "C"},
        {"texto": "A equação x² - 4x + 4 = 0 possui delta:",
            "opcoes": ["0", "4", "8", "-4"], "resposta": "A"},
        {"texto": "A equação x² + x + 1 = 0 possui delta:",
            "opcoes": ["5", "1", "0", "-3"], "resposta": "D"},
        {"texto": "Quando uma equação do segundo grau tem duas raízes reais iguais, seu delta é:",
            "opcoes": ["positivo", "zero", "negativo", "maior que 10"], "resposta": "B"},
        {"texto": "A forma geral da equação do segundo grau é:", "opcoes": [
            "ax + b = 0", "ax² + bx + c = 0", "a/x + b = 0", "x³ + ax = 0"], "resposta": "B"},
        {"texto": "Na equação 3x² - 2x + 1 = 0, o coeficiente b é:",
            "opcoes": ["3", "-2", "1", "0"], "resposta": "B"},
        {"texto": "A função f(x) = -4x + 8 é:", "opcoes": [
            "crescente", "decrescente", "quadrática", "exponencial"], "resposta": "B"},
        {"texto": "Em uma função linear de custo C(x) = 10x + 30, o valor 30 representa:", "opcoes": [
            "custo fixo", "quantidade vendida", "preço por unidade", "raiz da função"], "resposta": "A"},
        {"texto": "Para resolver uma equação do segundo grau por Bhaskara, primeiro é comum calcular:",
            "opcoes": ["o delta", "a porcentagem", "a média", "o perímetro"], "resposta": "A"},
    ]
    return criar_perguntas_por_lista(dados)


def criar_perguntas_fisica():
    dados = [
        {"texto": "Em uma transformação isotérmica de um gás ideal, qual grandeza permanece constante?",
            "opcoes": ["temperatura", "pressão", "volume", "massa molar"], "resposta": "A"},
        {"texto": "A lei de Boyle relaciona pressão e volume quando a temperatura é:",
            "opcoes": ["constante", "variável", "nula", "infinita"], "resposta": "A"},
        {"texto": "Na transformação isotérmica, se o volume aumenta, a pressão tende a:",
            "opcoes": ["aumentar", "diminuir", "ficar sempre zero", "sumir"], "resposta": "B"},
        {"texto": "Em uma transformação isobárica, qual grandeza permanece constante?", "opcoes": [
            "pressão", "volume", "temperatura", "energia cinética"], "resposta": "A"},
        {"texto": "Em uma transformação isovolumétrica, qual grandeza permanece constante?",
            "opcoes": ["volume", "pressão", "temperatura", "número de mols"], "resposta": "A"},
        {"texto": "A equação geral dos gases ideais é:", "opcoes": [
            "PV = nRT", "P + V = nRT", "P/V = n + R", "PV = mgh"], "resposta": "A"},
        {"texto": "Na equação PV = nRT, a letra P representa:", "opcoes": [
            "pressão", "potência", "peso", "período"], "resposta": "A"},
        {"texto": "Na equação PV = nRT, a letra V representa:", "opcoes": [
            "velocidade", "volume", "vácuo", "variação"], "resposta": "B"},
        {"texto": "Na equação PV = nRT, a letra T representa:", "opcoes": [
            "tempo", "temperatura", "tensão", "trabalho"], "resposta": "B"},
        {"texto": "A temperatura usada nas leis dos gases deve estar geralmente em:", "opcoes": [
            "Kelvin", "Celsius apenas", "Fahrenheit apenas", "metros"], "resposta": "A"},
        {"texto": "Zero grau Celsius corresponde aproximadamente a:",
            "opcoes": ["0 K", "100 K", "273 K", "373 K"], "resposta": "C"},
        {"texto": "Em uma transformação isobárica, volume e temperatura absoluta são:", "opcoes": [
            "diretamente proporcionais", "inversamente proporcionais", "sempre iguais", "independentes"], "resposta": "A"},
        {"texto": "Em uma transformação isovolumétrica, pressão e temperatura absoluta são:", "opcoes": [
            "diretamente proporcionais", "inversamente proporcionais", "iguais a zero", "sem relação"], "resposta": "A"},
        {"texto": "Na transformação isotérmica, pressão e volume são:", "opcoes": [
            "diretamente proporcionais", "inversamente proporcionais", "iguais", "sempre constantes"], "resposta": "B"},
        {"texto": "A constante R na equação dos gases ideais é chamada de:", "opcoes": [
            "constante universal dos gases", "resistência elétrica", "raio do gás", "razão térmica"], "resposta": "A"},
        {"texto": "O número de mols de um gás é representado por:",
            "opcoes": ["n", "m", "g", "t"], "resposta": "A"},
        {"texto": "Se a temperatura de um gás aumenta em volume constante, a pressão:", "opcoes": [
            "aumenta", "diminui", "fica sempre zero", "não existe"], "resposta": "A"},
        {"texto": "Se um gás é comprimido mantendo a temperatura constante, seu volume:",
            "opcoes": ["aumenta", "diminui", "não muda", "vira massa"], "resposta": "B"},
        {"texto": "A lei de Charles está ligada principalmente à transformação:", "opcoes": [
            "isobárica", "isotérmica", "isovolumétrica", "adiabática"], "resposta": "A"},
        {"texto": "A lei de Gay-Lussac está ligada principalmente à transformação:",
            "opcoes": ["isovolumétrica", "isotérmica", "mecânica", "elétrica"], "resposta": "A"},
        {"texto": "Um gás ideal é um modelo em que as partículas são consideradas:", "opcoes": [
            "sem volume próprio e sem interações relevantes", "presas em posições fixas", "sempre líquidas", "sem movimento"], "resposta": "A"},
        {"texto": "Quando a quantidade de gás n aumenta, mantendo P e T constantes, o volume tende a:",
            "opcoes": ["aumentar", "diminuir", "zerar", "ficar negativo"], "resposta": "A"},
        {"texto": "A unidade SI de pressão é:", "opcoes": [
            "pascal", "metro", "joule", "kelvin"], "resposta": "A"},
        {"texto": "A unidade SI de volume é:", "opcoes": [
            "metro cúbico", "pascal", "newton", "kelvin"], "resposta": "A"},
        {"texto": "Em PV = nRT, se n e R são constantes, P, V e T descrevem:", "opcoes": [
            "o estado do gás", "a cor do gás", "a massa da Terra", "a velocidade da luz"], "resposta": "A"},
        {"texto": "Uma transformação gasosa é uma mudança em grandezas como:", "opcoes": [
            "pressão, volume e temperatura", "cor, cheiro e sabor", "altura, idade e nome", "densidade, nota e série"], "resposta": "A"},
    ]
    return criar_perguntas_por_lista(dados)


def criar_perguntas_historia():
    dados = [
        {"texto": "Quem foi o prefeito responsável pela grande reforma urbana do Rio de Janeiro no início do século XX?",
            "opcoes": ["Getúlio Vargas", "Pereira Passos", "Rodrigues Alves", "Oswaldo Cruz"], "resposta": "B"},
        {"texto": "Qual doença o governo brasileiro tentava erradicar com a vacinação obrigatória que causou a Revolta da Vacina em 1904?",
            "opcoes": ["Febre Amarela", "Peste Bubônica", "Varíola", "Gripe Espanhola"], "resposta": "C"},
        {"texto": "Qual era o lema principal que guiava os ideais da Revolução Francesa?", "opcoes": [
            "Deus, Pátria e Família", "Paz, Pão e Terra", "Ordem e Progresso", "Liberdade, Igualdade e Fraternidade"], "resposta": "D"},
        {"texto": "Nas independências da América Espanhola, quem eram os 'criollos'?", "opcoes": [
            "Descendentes de espanhóis nascidos na América", "Indígenas escravizados nas minas", "Espanhóis natos enviados pela Coroa", "Mestiços sem direitos políticos"], "resposta": "A"},
        {"texto": "Qual órgão foi criado no Brasil em 1910 para 'proteger' os povos indígenas?", "opcoes": [
            "FUNAI", "IBAMA", "SPI (Serviço de Proteção aos Índios)", "Ministério dos Povos Originários"], "resposta": "C"},
        {"texto": "A destruição de cortiços e velhos casarões no centro do RJ ficou popularmente conhecida como:",
            "opcoes": ["Bota-abaixo", "Limpeza Geral", "Plano Diretor", "Marcha para o Oeste"], "resposta": "A"},
        {"texto": "Um interesse econômico fundamental para a elite criolla buscar a independência na América foi:", "opcoes": [
            "Distribuir terras aos camponeses", "O fim do pacto colonial e acesso ao livre comércio", "A abolição imediata da escravidão", "A criação de indústrias de base"], "resposta": "B"},
        {"texto": "A Revolução Francesa teve forte caráter burguês porque buscou principalmente:", "opcoes": [
            "Derrubar a monarquia para dar poder político exclusivo aos camponeses", "Acabar com os privilégios feudais da nobreza para favorecer o livre comércio e a propriedade", "Instaurar uma ditadura do proletariado na Europa", "Manter os privilégios do clero, mas com impostos menores"], "resposta": "B"},
        {"texto": "A política higienista no Rio de Janeiro republicano resultou, na prática, em:", "opcoes": ["Expulsão da população pobre do centro, iniciando a ocupação dos morros e periferias",
                                                                                                              "Construção de hospitais públicos em todas as favelas", "Distribuição de renda para os moradores dos cortiços desapropriados", "Fim das desigualdades sociais na capital federal"], "resposta": "A"},
        {"texto": "O médico sanitarista que liderou as campanhas de saúde pública durante o governo Rodrigues Alves foi:",
            "opcoes": ["Carlos Chagas", "Vital Brazil", "Oswaldo Cruz", "Adolfo Lutz"], "resposta": "C"},
        {"texto": "Na Primeira República brasileira, a ação do Estado em relação aos indígenas focava em:", "opcoes": [
            "Demarcar suas terras ancestrais e respeitar sua cultura de forma isolada", "Integrá-los forçosamente à 'civilização' e transformá-los em trabalhadores rurais", "Garantir cotas nas nascentes universidades públicas", "Armá-los para proteger as fronteiras do país contra invasores"], "resposta": "B"},
        {"texto": "Qual documento da Revolução Francesa consagrou a proteção à propriedade privada, refletindo o interesse burguês?", "opcoes": [
            "Código de Hamurabi", "Declaração dos Direitos do Homem e do Cidadão", "Constituição Civil do Clero", "O Tratado de Versalhes"], "resposta": "B"},
        {"texto": "A independência do Haiti foi única no continente americano porque:", "opcoes": ["Foi liderada por escravizados e resultou na imediata abolição da escravidão",
                                                                                                   "Foi a única apoiada militarmente pela Inglaterra", "Foi um processo pacífico liderado pela elite branca local", "Resultou na anexação do território pelos Estados Unidos"], "resposta": "A"},
        {"texto": "Durante a Revolta da Vacina, o povo também protestava contra:", "opcoes": [
            "A entrada do Brasil na Primeira Guerra Mundial", "A truculência dos agentes sanitários, a alta inflação e a crise econômica", "O fechamento do Congresso Nacional por Rodrigues Alves", "A proibição do Carnaval de rua pela polícia republicana"], "resposta": "B"},
        {"texto": "A reforma de Pereira Passos no Rio de Janeiro foi diretamente inspirada na remodelação de qual capital europeia?",
            "opcoes": ["Londres", "Madri", "Paris (reformas de Haussmann)", "Roma"], "resposta": "C"},
        {"texto": "Na Revolução Francesa, o período do Diretório (1795-1799) representou politicamente:", "opcoes": [
            "A radicalização popular liderada por Robespierre", "A volta da Monarquia Absolutista", "A consolidação do poder da alta burguesia, afastando os jacobinos", "O domínio da Igreja Católica sobre as leis do Estado"], "resposta": "C"},
        {"texto": "A 'Doutrina Monroe' (1823) influenciou as independências americanas ao defender a ideia de:", "opcoes": [
            "Destino Manifesto e expansão para o Pacífico", "América para os americanos, opondo-se a tentativas de recolonização europeia", "Pan-americanismo e uma única república na América do Sul", "Abolição gradual da escravatura em todo o hemisfério"], "resposta": "B"},
        {"texto": "O SPI (Serviço de Proteção aos Índios) tinha fortes bases no Positivismo, o qual acreditava que os indígenas:", "opcoes": [
            "Eram culturalmente superiores aos europeus", "Estavam em um estágio evolutivo inferior e precisavam de tutela do Estado até atingirem a civilização", "Deveriam ser exterminados para liberar terras ao agronegócio", "Tinham o direito de formar repúblicas autônomas dentro do Brasil"], "resposta": "B"},
        {"texto": "A política higienista no RJ também agiu como controle social, visando reprimir principalmente:", "opcoes": [
            "O comércio de luxo de produtos importados", "A vadiagem, a capoeira e as manifestações culturais afro-brasileiras", "As greves de trabalhadores das montadoras de automóveis", "Os bailes de elite financiados pelos barões do café"], "resposta": "B"},
        {"texto": "Na Independência do Brasil, o principal interesse da elite agrária que apoiou D. Pedro I era:", "opcoes": [
            "Garantir a liberdade comercial, mas mantendo a estrutura escravista e latifundiária", "Transformar o Brasil em uma federação descentralizada e industrial", "Garantir a reforma agrária para evitar revoltas populares", "Aliar-se à França para derrotar a marinha britânica"], "resposta": "A"},
        {"texto": "A Lei de Le Chapelier (1791) evidencia o aspecto excludente da burguesia na Revolução Francesa ao:", "opcoes": [
            "Restaurar o poder de veto do Rei", "Proibir as corporações de ofício, greves e a formação de sindicatos trabalhistas", "Aumentar os impostos sobre o pão", "Excluir as mulheres das eleições indiretas"], "resposta": "B"},
        {"texto": "Durante a Revolta da Vacina, ocorreu também o levante da Escola Militar da Praia Vermelha. Qual era seu objetivo político oculto?", "opcoes": [
            "Restaurar a Monarquia de D. Pedro II", "Instaurar uma ditadura comunista inspirada em Marx", "Derrubar Rodrigues Alves e instaurar um governo militar positivista/florianista", "Forçar a capital do Brasil a ser transferida para Brasília imediatamente"], "resposta": "C"},
        {"texto": "O Congresso do Panamá (1826), convocado por Simón Bolívar, fracassou devido principalmente:", "opcoes": [
            "À invasão espanhola que reconquistou a Venezuela no mesmo ano", "Aos interesses particularistas das elites locais e à oposição de Inglaterra e EUA a uma América unida", "À recusa dos escravizados em lutar no exército bolivariano", "Aos desastres naturais que destruíram o local das negociações"], "resposta": "B"},
        {"texto": "O Marechal Rondon, primeiro líder do SPI, adotava um lema que refletia sua abordagem de pacificação tutelar. Qual era?", "opcoes": [
            "A ordem pelo progresso", "Morrer se preciso for, matar nunca", "A lei é para todos, a terra para quem trabalha", "Civilizar ou perecer"], "resposta": "B"},
        {"texto": "Antes da aceitação total da bacteriologia, o higienismo no Brasil apoiava-se na 'Teoria Miasmática', que justificava a destruição de cortiços argumentando que:", "opcoes": [
            "Eles abrigavam ratos infectados com pulgas transmissoras", "A falta de moralidade religiosa causava o enfraquecimento do sistema imune", "As doenças eram transmitidas por mosquitos encontrados na água parada dos casarões", "As doenças emanavam de gases ruins (miasmas) de ambientes fechados, exigindo circulação de ar e luz solar"], "resposta": "D"},
        {"texto": "Analisando as independências latino-americanas e a modernização republicana brasileira sob a ótica da Revolução Francesa, qual afirmação melhor sintetiza a formação dos Estados na América Latina?", "opcoes": [
            "A aplicação irrestrita da fraternidade jacobina gerou repúblicas radicais e igualitárias no século XIX.", "Houve uma apropriação seletiva do liberalismo pela elite: buscou-se o livre-mercado e a modernização institucional, mas perpetuou-se a exclusão social e política de negros, indígenas e pobres urbanos.", "O sucesso do pan-americanismo garantiu o fim imediato das desigualdades, graças à abolição da escravidão financiada pela burguesia europeia.", "A elite criolla rejeitou integralmente o Iluminismo, copiando o modelo absolutista ibérico para sufocar o desenvolvimento urbano."], "resposta": "B"},
    ]
    return criar_perguntas_por_lista(dados)


def criar_perguntas_biologia():
    dados = [
        {"texto": "Qual ação contribui diretamente para a preservação ambiental?", "opcoes": [
            "Expansão de áreas urbanas", "Descarte irregular de resíduos", "Exploração intensiva de recursos naturais", "Proteção de ecossistemas naturais"], "resposta": "D"},
        {"texto": "O conceito de conservação ambiental está relacionado a:", "opcoes": [
            "Proibir qualquer atividade humana", "Substituir florestas por plantações", "Utilizar os recursos naturais de forma sustentável", "Eliminar espécies exóticas"], "resposta": "C"},
        {"texto": "Qual atividade representa uma ameaça à biodiversidade?", "opcoes": [
            "Educação ambiental", "Desmatamento", "Reciclagem", "Reflorestamento"], "resposta": "B"},
        {"texto": "A preservação ambiental tem como principal objetivo:", "opcoes": [
            "Manter ambientes naturais protegidos de alterações significativas", "Expandir áreas agrícolas", "Construir novas rodovias", "Aumentar a exploração mineral"], "resposta": "A"},
        {"texto": "Qual prática favorece a conservação dos recursos naturais?", "opcoes": [
            "Queimadas frequentes", "Caça predatória", "Reciclagem de materiais", "Poluição de rios"], "resposta": "C"},
        {"texto": "As unidades de conservação foram criadas para:", "opcoes": [
            "Expandir cidades", "Proteger a biodiversidade e os ecossistemas", "Incentivar a mineração", "Facilitar o desmatamento"], "resposta": "B"},
        {"texto": "Qual unidade pertence ao grupo de proteção integral?", "opcoes": [
            "Área de Proteção Ambiental", "Reserva Extrativista", "Floresta Nacional", "Parque Nacional"], "resposta": "D"},
        {"texto": "Uma Área de Proteção Ambiental (APA) permite:", "opcoes": [
            "Caça de espécies ameaçadas", "Desmatamento sem controle", "Uso sustentável dos recursos naturais", "Ocupação irregular"], "resposta": "C"},
        {"texto": "A sigla SNUC significa:", "opcoes": ["Sistema Nacional de Uso da Conservação", "Sistema Nacional de Unidades de Conservação da Natureza",
                                                        "Serviço Nacional de Unidades Conservadas", "Sistema Natural de Conservação"], "resposta": "B"},
        {"texto": "Uma Reserva Biológica tem como principal finalidade:", "opcoes": [
            "Preservação integral da biodiversidade", "Produção agrícola", "Extração de madeira", "Pecuária extensiva"], "resposta": "A"},
        {"texto": "Bioacumulação é o processo de:", "opcoes": [
            "Produção de nutrientes", "Reprodução celular", "Acúmulo de substâncias tóxicas em organismos", "Formação de fósseis"], "resposta": "C"},
        {"texto": "Qual substância pode sofrer bioacumulação nos seres vivos?", "opcoes": [
            "Oxigênio", "Mercúrio", "Água", "Gás carbônico"], "resposta": "B"},
        {"texto": "A bioacumulação ocorre quando:", "opcoes": ["Os organismos eliminam rapidamente as substâncias absorvidas", "Não existe cadeia alimentar",
                                                               "O ambiente é totalmente livre de poluentes", "A absorção de contaminantes é maior que sua eliminação"], "resposta": "D"},
        {"texto": "Em uma cadeia alimentar contaminada, os maiores níveis de poluentes costumam ser encontrados:", "opcoes": [
            "Nos produtores", "Nos decompositores", "Nos predadores de topo", "Apenas na água"], "resposta": "C"},
        {"texto": "O aumento da concentração de contaminantes ao longo dos níveis tróficos recebe o nome de:", "opcoes": [
            "Fotossíntese", "Biomagnificação", "Respiração celular", "Sucessão ecológica"], "resposta": "B"},
        {"texto": "Uma aplicação benéfica da radiação é:", "opcoes": [
            "Radioterapia para tratamento de câncer", "Contaminação ambiental", "Danos ao DNA", "Exposição excessiva de trabalhadores"], "resposta": "A"},
        {"texto": "A exposição prolongada a altas doses de radiação pode causar:", "opcoes": [
            "Produção de vitaminas", "Crescimento celular controlado", "Mutações genéticas", "Fotossíntese"], "resposta": "C"},
        {"texto": "Os raios X são amplamente utilizados para:", "opcoes": [
            "Produção agrícola", "Diagnóstico médico", "Geração de energia hidrelétrica", "Tratamento de água"], "resposta": "B"},
        {"texto": "Qual das alternativas representa uma fonte natural de radiação?", "opcoes": [
            "Equipamento de radiografia", "Usina nuclear", "Reator experimental", "Raios cósmicos"], "resposta": "D"},
        {"texto": "A proteção radiológica busca:", "opcoes": [
            "Aumentar a exposição humana", "Eliminar toda tecnologia nuclear", "Reduzir os riscos da exposição à radiação", "Produzir resíduos radioativos"], "resposta": "C"},
        {"texto": "A mitose resulta em:", "opcoes": [
            "Quatro células diferentes", "Duas células geneticamente idênticas", "Oito células haploides", "Apenas gametas"], "resposta": "B"},
        {"texto": "A principal função da meiose é:", "opcoes": [
            "Produzir gametas", "Reparar tecidos lesionados", "Formar bactérias", "Produzir células somáticas"], "resposta": "A"},
        {"texto": "Na mitose, os cromossomos alinham-se no plano equatorial durante a:",
            "opcoes": ["Prófase", "Telófase", "Metáfase", "Citocinese"], "resposta": "C"},
        {"texto": "O crossing-over ocorre durante a:", "opcoes": [
            "Anáfase II", "Prófase I da meiose", "Metáfase da mitose", "Telófase I"], "resposta": "B"},
        {"texto": "Qual evento aumenta significativamente a variabilidade genética das populações?", "opcoes": [
            "Mitose", "Reprodução assexuada", "Fissão binária", "Meiose associada ao crossing-over"], "resposta": "D"},
        {"texto": "Em um ecossistema protegido por unidades de conservação, peixes acumulam mercúrio ao longo da cadeia alimentar. Estudos indicam que a exposição excessiva à radiação pode causar alterações no DNA, enquanto a meiose contribui para a variabilidade genética das espécies. Qual alternativa relaciona corretamente esses conceitos?", "opcoes": [
            "A bioacumulação reduz a concentração de poluentes nos predadores de topo.", "A meiose produz células geneticamente idênticas.", "A bioacumulação pode concentrar contaminantes nos organismos, enquanto a meiose promove variabilidade genética e a conservação ajuda a proteger os ecossistemas.", "A radiação não apresenta aplicações benéficas para a sociedade."], "resposta": "C"},
    ]
    return criar_perguntas_por_lista(dados)


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
        "4": ("GEOGRAFIA", criar_perguntas_em_branco),
        "5": ("SOCIOLOGIA", criar_perguntas_em_branco),
        "6": ("BIOLOGIA", criar_perguntas_biologia),
        "7": ("FÍSICA", criar_perguntas_fisica),
        "8": ("QUÍMICA", criar_perguntas_em_branco),
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
            if escolha == "1":
                opcoes_visiveis = aplicar_5050(pergunta, opcoes_visiveis)
            elif escolha == "2":
                aplicar_pedir_publico(pergunta)
            elif escolha == "3":
                nova_posicao = aplicar_pular(pergunta_index, perguntas)
                if nova_posicao != pergunta_index:
                    pergunta_index = nova_posicao
                    continue
            tocar_som("lifeline")
            lifelines_usadas.append(lifelines[escolha])
            del lifelines[escolha]
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
                tocar_som("win")
                print("Parabéns! Você venceu o jogo e alcançou R$", premio_atual)
                break
        else:
            tocar_som("wrong")
            tocar_som("game_over")
            garantia = calcular_garantia(perguntas_respondidas)
            print("Resposta incorreta. GAME OVER.")
            print("Você deixa o jogo com R$", garantia)
            break
    if pergunta_index >= len(perguntas):
        print("Fim de jogo. Obrigado por jogar!")
    print("Lifelines usados:",
          "Nenhum" if not lifelines_usadas else ", ".join(lifelines_usadas))


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
                print("Ate a proxima!")
                break
            else:
                print("Opcao invalida. Digite 1, 2, 3 ou 4.")
    except (EOFError, KeyboardInterrupt):
        print("\nJogo encerrado.")
    finally:
        if not sys.stdin.isatty():
            input("Pressione Enter para sair...")


if __name__ == "__main__":
    main()
