import csv
from datetime import datetime
from time import sleep
from pathlib import Path

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

def consultar_ponto_completo(funcionario_id):
    registros = ler_pontos(funcionario_id)

    num_registros = len(registros)
    
    if num_registros < 2:
        print("Não há registros suficientes para calcular a diferença de horas.")
        return    

    dia = datetime.min
    minutos_dia = 0
    total_trabalhado = 0
    total_diferenca = 0

    for i in range(1, num_registros,2):
        if i > num_registros:
            return
        
        if dia.day != registros[i].day:            
            if minutos_dia > 0:
                diferenca_dia = calcula_diferenca(minutos_dia)
                total_diferenca += diferenca_dia
                imprime_saldo_dia(minutos_dia, diferenca_dia)
                minutos_dia = 0                

            dia = registros[i]
            print(f"Dia {registros[i].day:02}/{registros[i].month:02}/{registros[i].year}:")
            print("Horários registrados:")

        diferenca = registros[i] - registros[i - 1]        

        minutos_dia += diferenca.total_seconds() // 60

        diferenca_em_horas = diferenca.total_seconds() // 3600
        diferenca_em_minutos = (diferenca.total_seconds() % 3600) // 60
        print(f"Tempo trabalhado: {int(diferenca_em_horas):02}:{int(diferenca_em_minutos):02}")

        total_trabalhado += diferenca.total_seconds() // 60

    if minutos_dia > 0:
        diferenca_dia = calcula_diferenca(minutos_dia)
        total_diferenca += diferenca_dia
        imprime_saldo_dia(minutos_dia,diferenca_dia)
    
    print("--------- Totais ---------")
    print(f"Horas trabalhadas: {int((total_trabalhado//60)):02}:{int((total_trabalhado%60)):02}")
    if total_diferenca > 0:
        devido_extra = "devidas"
    else:
        total_diferenca *= -1
        devido_extra = "extras"

    total_diferenca = int(total_diferenca)

    print(f"Diferença final: {total_diferenca//60:02}:{total_diferenca%60:02} {devido_extra}")
    print("--------------------------")    
    print()

def calcula_diferenca(minutos_dia):
    global carga_horaria

    if carga_horaria > 0:
        return int(carga_horaria*60 - minutos_dia)
    
    return minutos_dia

def imprime_saldo_dia(minutos_dia, diferenca_minutos):
    global indFuncao
    global carga_horaria
    global salario_hora

    horas_trabalhadas = int(minutos_dia // 60)
    minutos_trabalhados = int(minutos_dia % 60)

    print()
    print("------ Saldo do dia ------")
    print(f"Horas trabalhadas: {horas_trabalhadas:02}:{minutos_trabalhados:02}")
    if indFuncao == 3: #Se for freela, mostra valor a receber
        print(f"Valor a receber: ${salario_hora*minutos_dia/60:.2f}")
    else:
        print(f"Carga horária normal: {carga_horaria:02}h")        
        if diferenca_minutos == 0:
            print("Carga horária cumprida.")
        elif diferenca_minutos > 0:
            print(f"São devidas {(diferenca_minutos//60):02}:{(diferenca_minutos%60):02}!")
        else:
            diferenca_minutos *= -1
            print(f"Foram feitas {(diferenca_minutos//60):02}:{(diferenca_minutos%60):02} extras!")
    print()

def consultar_ponto_completo_dia(funcionario_id):
    registros = ler_pontos(funcionario_id)
    dia_hist = 0

    print("Dias para consulta:")

    for i in range(0,len(registros)):        
        dia = registros[i]

        if dia.day != dia_hist:
            dia_hist = dia.day
            print(f"{i}: {dia.day:02}/{dia.month:02}/{dia.year}")
    
    index_dia = int(input("Informe o dia para consulta: "))

    consultar_dia(registros,index_dia)

def consultar_dia(registros, index):
    instancia = registros[index]
    minutos_dia = 0

    print()
    print(f"Dia {instancia.day:02}/{instancia.month:02}/{instancia.year}")
    print("Horários registrados:")
    for i in range(1,len(registros),2):
        dia = registros[i].day
        if dia != instancia.day:        
            continue
        else:
            diferenca = registros[i] - registros[i - 1]        

            minutos_dia += diferenca.total_seconds() // 60

            diferenca_em_horas = diferenca.total_seconds() // 3600
            diferenca_em_minutos = (diferenca.total_seconds() % 3600) // 60
            print(f"Tempo trabalhado: {int(diferenca_em_horas):02}:{int(diferenca_em_minutos):02}")

    if minutos_dia > 0:
        diferenca_dia = calcula_diferenca(minutos_dia)
        imprime_saldo_dia(minutos_dia,diferenca_dia)

def ler_todos_arquivos_ponto():
    # Caminho para a pasta raiz do programa
    folder_path = Path('.')

    # Obter a lista de arquivos que correspondem ao padrão
    files = folder_path.glob('ponto_*.csv')

    for file in files:
        if file.is_file():
            id = extrair_id(file.name)
            print(f"Colaborador Matrícula {id}:")
            consultar_ponto_completo(id)
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~")            

def extrair_id(nome_arquivo):
    aux = nome_arquivo.split('_')
    return aux[1].split('.')[0]

# Função para alterar o ponto de um funcionário (apenas para gestores)
def ajustar_ponto_funcionario(id):
    registros = ler_pontos(id)
    print("Escolha o registro que deseja alterar:")
    for i in range(0,len(registros)):
        print(f"{i}: {registros[i].day:02}/{registros[i].month:02}/{registros[i].year} {registros[i].hour:02}:{registros[i].minute:02}")
    print(f"{i+1}: Adicionar novo registro")
    index = int(input())

    nova_data = input("Infome a nova data (dd/mm/yyyy): ")
    nova_hora = input("Infome a nova hora (hh:mm): ")

    confirma = input("Confirma alteração? (s/n) ")

    if confirma.lower() == 's':
        data_split = nova_data.split('/')
        hora_split = nova_hora.split(':')
        nova_data = datetime(int(data_split[2]),int(data_split[1]),int(data_split[0]),int(hora_split[0]),int(hora_split[1]))
        modificar_ponto(id, index, nova_data)

# Função para modificar uma linha específica
def modificar_ponto(funcionario_id, index, nova_data):
    nomeArquivo = f"ponto_{str(funcionario_id)}.csv"
    registros = ler_pontos(funcionario_id)
    if index >= len(registros):
        registros.append(nova_data)
    else:
        registros[index] = nova_data

    with open(nomeArquivo, mode="w", newline='', encoding='utf-8') as arquivo:
        writer = csv.writer(arquivo, quoting=csv.QUOTE_NONE)
        for registro in registros:
            hora = f"{registro.hour:02}:{registro.minute:02}"
            dia = f"{registro.day:02}/{registro.month:02}/{registro.year}"
            writer.writerow([dia,hora])

    print(f"Linha {index} modificada com sucesso.")

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
        acao = input().lower()
        if acao == "s":
            registrar_ponto(id)
            print("Ponto Registrado com sucesso!")

def realiza_acao_dois():
    global indFuncao
    global id

    if(indFuncao == 1):
        id = int(input("Informe a matrícula do colaborador que deseja alterar: "))
        ajustar_ponto_funcionario(id)
    else:
        consultar_ponto_completo(id)


def realiza_acao_tres():
    global indFuncao
    global id

    if(indFuncao == 1):
        return
    else:
        consultar_ponto_completo_dia(id)

# Menu principal
print()
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

print(f"Seja bem vindo(a) {nome}")

while True:
    opcao = -1
    print('Menu de opções - Selecione a ação que deseja realizar:')
    match indFuncao:
        case 1: # gestor
            print('1 - Consultar todos os pontos')
            print('2 - Ajustar ponto')
        case 2: # funcionario
            print('1 - Marcar ponto')
            print('2 - Consultar pontos')
            print('3 - Consultar dia específico')
        case 3: # freelancer
            print('1 - Marcar ponto')
            print('2 - Consultar pontos')
            print('3 - Consultar dia específico')

    print('0 - Encerrar programa')
    opcao = int(input('Digite a sua opção: '))
    print()

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