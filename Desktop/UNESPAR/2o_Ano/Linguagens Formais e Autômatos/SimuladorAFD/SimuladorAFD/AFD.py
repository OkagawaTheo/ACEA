# Estruturas
estados = []  # Criando uma lista de estados
simbolos = []  # Criando uma lista de símbolos
funcao_Transicao = {} # Criando um dicionário

estado_inicial = ""
estados_finais = []

def executar_AFD(estados, simbolos, funcao_Transicao, estado_inicial, estados_finais):
    while True:
        print("Insira a palavra a ser verificada: ", end="")
        entrada_usuario = input()

        # Validação de cada caractere da palavra
        if not all(char in simbolos for char in entrada_usuario):
            print("Palavra não aceita! Símbolos inválidos.")
            continue

        estado_atual = estado_inicial
        palavra_aceita = True  # Flag para verificar se a palavra foi aceita

        for char in entrada_usuario:
            # Acessando a função de transição
            proximo_estado = funcao_Transicao.get((estado_atual, char))

            if proximo_estado is None:  # Transição inválida
                print("Palavra não aceita! Transição inválida.")
                palavra_aceita = False
                break

            estado_atual = proximo_estado

        # Verificando se o estado final foi alcançado
        if palavra_aceita:
            if estado_atual in estados_finais:
                print("Palavra aceita!")
            else:
                print("Palavra não aceita!")

# Recebendo os dados do AFD

print("Informe o estado inicial: ", end="")
estado_inicial = input().strip()

print("Informe os estados finais (separados por espaço): ", end="")
estados_finais = input().split()  # A função split separa strings em substrings, retornando listas

print("Informe o conjunto de estados (separados por espaço): ", end="")
estados = input().split()
qtdEstados = len(estados)  # Registra a quantidade de estados listados

print("Informe os símbolos de entrada (separados por espaço): ", end="")
simbolos = input().split()
qtdSimbolos = len(simbolos)  # Registra a quantidade de símbolos listados

print("Preencha as transições:")  # Preenche as transições
for estado in estados:
    for simbolo in simbolos:
        print(f" δ ({estado},{simbolo}): ", end="")
        proximo_estado = input().strip() # A função strip é utilizada para remover espaços em branco no início e no final de uma string

        if proximo_estado.upper() == "X":
            funcao_Transicao[(estado, simbolo)] = None
        else:
            funcao_Transicao[(estado, simbolo)] = proximo_estado

executar_AFD(estados, simbolos, funcao_Transicao, estado_inicial, estados_finais)
