from calendar import month
import csv
import datetime
from sqlite3 import Date
from time import sleep

from matplotlib.hatch import HorizontalHatch
from numpy import block

# Dicionário para armazenar os registros de ponto
registros_ponto = {}

indFuncao = 0
nome = ""
empresa = ""
carga_horaria = 0
salario_hora = 0.0


# Função para registrar o ponto
def registrar_ponto(funcionario_id):
    agora = datetime.datetime.now()
    hora = agora.hour.__str__() + ":" + agora.minute.__str__() 
    dia = agora.day.__str__() + "/" + agora.month.__str__() + "/" + agora.year.__str__()

    nomeArquivo = "ponto_" + str(funcionario_id) + ".csv"
    arquivo = open(nomeArquivo,"a")
    arquivo.write(dia+","+hora+"\n")

    arquivo.close()

# Função para gerar o relatório CSV
def gerar_relatorio_csv():
    with open('relatorio_ponto.csv', 'w', newline='') as arquivo_csv:
        cabecalho = ['Funcionário', 'Entrada', 'Saída']
        writer = csv.DictWriter(arquivo_csv, fieldnames=cabecalho)
        writer.writeheader()
        for funcionario_id, registro in registros_ponto.items():
            writer.writerow({'Funcionário': funcionario_id, 'Entrada': registro['entrada'], 'Saída': registro['saida']})
    print('Relatório gerado com sucesso (relatorio_ponto.csv)')

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

    if (indFuncao == 1):
        print("Lendo arquivos...")
    else:
        agora = datetime.datetime.now()
        hora_str = agora.day.__str__() + "/" + agora.month.__str__() + "/" + agora.year.__str__() + " - " + agora.hour.__str__() + ":" + agora.minute.__str__()  

        print("Confirma marcação de ponto ",hora_str,"?(s/n)")
        acao = input()
        if acao == "s":
            registrar_ponto(id)



# Menu principal
print("=========================")
try:
    arqConfig = open("config.dat","x")
    arqConfig.close()

    montaArquivoConfig()
    lerArquivoConfig()
except:
    lerArquivoConfig()

while True:
    print('Menu de opções - Selecione a ação que deseja realizar:')
    match indFuncao:
        case 1: # gestor
            print('1 - Consultar ponto do funcionário')
        case 2: # funcionario
            print('1 - marcar ponto')
        case 3: # freelancer
            print('1 - marcar ponto')

    print('0 - encerrar programa')
    opcao = int(input('Digite a sua opção:'))

    if opcao == 1:
        realiza_acao_um()
        print('Gestor')
        funcionario_id = input('Digite o ID do funcionário: ')
        alterar_ponto_gestor(funcionario_id)
    elif opcao == 2:
        print('Funcionário')
        funcionario_id = input('Digite o seu ID: ')
        registrar_ponto(funcionario_id)
    elif opcao == 3:
        gerar_relatorio_csv()
        break
    elif opcao == 0:
        print('Adeus...')
        sleep(2)
        print('Encerrando programa...')
        sleep(2)
        break
    else:
        print('Opção inválida. Tente novamente.')
    print('')