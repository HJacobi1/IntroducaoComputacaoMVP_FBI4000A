import csv
from datetime import datetime
from math import e
from time import sleep
from pathlib import Path

# Dicionário para armazenar os registros de ponto
registros_ponto = {}

indFuncao = 0
nome = ""
empresa = ""
carga_horaria = 0
salario_hora = 0.0


# Função para registrar o ponto
def registrar_ponto(funcionario_id):
    agora = datetime.now()
    hora = f"{agora.hour:02}:{agora.minute:02}"
    dia = f"{agora.day:02}/{agora.month:02}/{agora.year:4}"

    nomeArquivo = f"ponto_{str(funcionario_id)}.csv"
    with open(nomeArquivo,"a",newline='') as arquivo:
        writer = csv.writer(arquivo,csv.QUOTE_NONE)
        writer.writerow([dia,hora])

def ler_pontos(funcionario_id):
    nomeArquivo = f"ponto_{str(funcionario_id)}.csv"
    registros = []

    try:
        with open(nomeArquivo, mode="r", newline='', encoding='utf-8') as arquivo:
            reader = csv.reader(arquivo)
            for row in reader:
                dia, hora = row      
                # Concatenar data e hora e converter para objeto datetime
                registro_datetime = datetime.strptime(f"{dia} {hora}", "%d/%m/%Y %H:%M")
                registros.append(registro_datetime)
        
        return registros
    
    except(FileNotFoundError):
        print("Não foi encontrado registro de ponto para o id",str(funcionario_id))

def calcular_diferenca_horas(funcionario_id):
    registros = ler_pontos(funcionario_id)
    
    if len(registros) < 2:
        print("Não há registros suficientes para calcular a diferença de horas.")
        return

    for i in range(1, len(registros)):
        diferenca = registros[i] - registros[i - 1]
        diferenca_em_horas = diferenca.total_seconds() / 3600
        print(f"Diferença entre {registros[i - 1]} e {registros[i]}: {diferenca_em_horas:.2f} horas")

def ler_todos_arquivos_ponto():
    # Caminho para a pasta raiz do programa
    folder_path = Path('.')

    # Obter a lista de arquivos que correspondem ao padrão
    files = folder_path.glob('ponto_*.csv')

    for file in files:
        if file.is_file():
            with open(file, 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    print(row)

# Função para alterar o ponto de um funcionário (apenas para gestores)
def alterar_ponto_gestor(funcionario_id):
    if funcionario_id in registros_ponto:
        print(f'Registro atual para funcionário {funcionario_id}:')
        print(f'Entrada: {registros_ponto[funcionario_id]["entrada"]}')
        print(f'Saída: {registros_ponto[funcionario_id]["saida"]}')
        opcao = input('Deseja alterar o registro? (s/n): ')
        if opcao.lower() == 's':
            nova_entrada = input('Digite a nova hora de entrada (formato HH:MM): ')
            nova_saida = input('Digite a nova hora de saída (formato HH:MM): ')
            try:
                registros_ponto[funcionario_id]['entrada'] = datetime.datetime.strptime(nova_entrada, '%H:%M')
                registros_ponto[funcionario_id]['saida'] = datetime.datetime.strptime(nova_saida, '%H:%M')
                print(f'Registro alterado com sucesso para funcionário {funcionario_id}')
            except ValueError:
                print('Formato de hora inválido. Use HH:MM.')
        else:
            print('Registro não alterado.')
    else:
        print(f'Funcionário {funcionario_id} não possui registro de ponto.')

def montaArquivoConfig():
    arqConfig = open("config.dat","w")

    print("Seja bem vindo ao controle de ponto!")
    print("Realize a configuração Inicial:")
    print("1 - Gestor (vou gerir meus funcionários)")
    print("2 - Funcionário (vou registrar meus pontos e controlar minhas hora's)")
    print("3 - Freelancer (vou registrar minhas horas e estimar meus ganhos)")
    indFuncao = int(input())

    match indFuncao:
        case 1:
            id = int(input("Informe sua matrícula:"))
            nome = input("Informe seu nome: ")
            empresa = input("Informe o nome da sua empresa: ") 
            carga_horaria = 0
            salario_hora = 0

        case 2:
            id = int(input("Informe sua matrícula:"))
            nome = input("Informe seu nome: ")
            empresa = input("Informe o nome da sua empresa: ")  
            carga_horaria = int(input("Informe sua carga horária diária (em horas): "))
            salario_hora = float(input("Informe o seu salário por hora: "))

        case 3:
            id = 1
            nome = input("Informe seu nome: ")
            empresa = nome
            salario_hora = float(input("Informe o seu salário por hora: "))
            carga_horaria = 0

    arqConfig.write(str(indFuncao)+"\n")
    arqConfig.write(str(id)+"\n")
    arqConfig.write(nome+"\n")
    arqConfig.write(empresa+"\n")
    arqConfig.write(str(carga_horaria)+"\n")
    arqConfig.write(str(salario_hora))

    arqConfig.close()

def lerArquivoConfig():
    global indFuncao
    global id
    global nome
    global empresa
    global carga_horaria
    global salario_hora

    arqConfig = open("config.dat","r")
    indFuncao = int(arqConfig.readline())
    id = int(arqConfig.readline())
    nome = arqConfig.readline()
    empresa = arqConfig.readline()
    carga_horaria = int(arqConfig.readline())
    salario_hora = float(arqConfig.readline())

    arqConfig.close()

def realiza_acao_um():
    global indFuncao
    global id

    if (indFuncao == 1): #Gestor
        print("Lendo arquivos...")

        ler_todos_arquivos_ponto()
    else: #Funcionario ou Freelancer
        agora = datetime.now()
        hora_str = f"{agora.day:02}/{agora.month:02}/{agora.year:4} - {agora.hour:02}:{agora.minute:02}"

        print("Confirma marcação de ponto ",hora_str,"?(s/n)")
        acao = input()
        if acao == "s":
            registrar_ponto(id)
            print("Ponto Registrado com sucesso!")

def realiza_acao_dois():
    global indFuncao
    global id

    if(indFuncao == 1):
        return
    else:
        registros = ler_pontos(id)
        for registro in registros:
            print(registro)

        calcular_diferenca_horas(id)


def realiza_acao_tres():
    foo = 0



# Menu principal
print("==========================")
print(" ----- HoraCerta.py ----- ")
print("==========================")
try:
    arqConfig = open("config.dat","x")
    arqConfig.close()

    montaArquivoConfig()
    lerArquivoConfig()
except(FileExistsError):
    lerArquivoConfig()

print(f"Seja bem vindo(a){nome}!")

while True:
    opcao = -1
    print('Menu de opções - Selecione a ação que deseja realizar:')
    match indFuncao:
        case 1: # gestor
            print('1 - Consultar ponto do funcionário')
        case 2: # funcionario
            print('1 - Marcar ponto')
            print('2 - Conferir pontos')
        case 3: # freelancer
            print('1 - Marcar ponto')
            print('2 - Conferir pontos')

    print('0 - Encerrar programa')
    opcao = int(input('Digite a sua opção: '))

    if opcao == 1:
        realiza_acao_um()
    elif opcao == 2:
        realiza_acao_dois()
    elif opcao == 3:
        realiza_acao_tres()
    elif opcao == 0:
        print('Encerrando programa...')
        sleep(2)
        break
    else:
        print('Opção inválida. Tente novamente.')
    print('')
    