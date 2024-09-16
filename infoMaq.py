import subprocess
import os
# Pegar status do firewall
# Pegando informações do SO e quantos GB RAM:
def getSystemInfo():
    comando = "systeminfo"

    result = subprocess.run(["powershell", "-Command", comando], capture_output=True, text=True)

    with open("aux.txt", "w", encoding="utf-8") as arqInfo:
        arqInfo.write(result.stdout)

    with open("aux.txt", "r", encoding="utf-8") as arqInfo:
        linhas = arqInfo.readlines()

    # Dicionário para armazenar as variáveis
    variaveis = {}

    # Processa cada linha e salva as informações após os dois pontos
    for linha in linhas:
        if ":" in linha:
            chave, valor = linha.split(":", 1)
            variaveis[chave.strip()] = valor.strip()

    # Exemplo de acesso às variáveis as quais vão para o db
    nome_sistema_operacional = variaveis.get("Nome do sistema operacional")
    modelo_sistema = variaveis.get("Modelo do sistema")
    memoria_fisica_total = variaveis.get("Mem¢ria f¡sica total")

    # Salva as linhas desejadas em um arquivo
    linhas_desejadas = [
        f"{nome_sistema_operacional}\n",
        f"{modelo_sistema}\n",
        f"{memoria_fisica_total}\n",
    ]

    with open("infos.txt", "w", encoding="utf-8") as arqSaida:
        arqSaida.writelines(linhas_desejadas)

    arqSaida.close()

# Pegando número de série da máquina
def getSerialNumber():
    comando = "Get-WmiObject -Class Win32_BIOS | Select-Object -Property SerialNumber"

    result = subprocess.run(["powershell", "-Command", comando], capture_output=True, text=True)

    serial_number = result.stdout.split('\n')[3].strip() # Variavel que vai pro DB

    with open("infos.txt", "a", encoding="utf-8") as arqSerial:
        arqSerial.write(f'Número de série:   {serial_number}\n')
    
    arqSerial.close()

# Pegando qual DDR é a Mem Ram
def getDDR():

    comando = "Get-WmiObject -Class Win32_PhysicalMemory | Format-List *"

    result = subprocess.run(["powershell", "-Command", comando], capture_output=True, text=True)

    with open("aux.txt", "w", encoding="utf-8") as arqMemory:
        arqMemory.write(result.stdout)


    with open("aux.txt", "r", encoding="utf-8") as arqRAM:
        linhas = arqRAM.readlines()

    variaveis = {}

    for linha in linhas:
        if ":" in linha:
            chave, valor = linha.split(":", 1)
            variaveis[chave.strip()] = valor.strip()

    for chave, valor in variaveis.items():
        print(f"{chave}: {valor}")
    
    clock_speed = variaveis.get('ConfiguredClockSpeed')
    tipo = variaveis.get('SMBIOSMemoryType')

    ddr_type = {
        '20': 'DDR1',
        '21': 'DDR2',
        '24': 'DDR3',
        '26': 'DDR4',
        '27': 'DDR5',
    }

    tipo = ddr_type.get(tipo, 'Descohecido')

    # As variáveis que vão pro DB aqui são: clock speed e tipo

    print(f'Clock SPeed: {clock_speed}')
    print(f'DDR Type: {tipo}')

    linhas_desejadas = [f'{clock_speed}\n',
                        f'{tipo}\n']
    
    with open("infos.txt", "a", encoding="utf-8") as arqSaida:
        arqSaida.writelines(linhas_desejadas)

    arqMemory.close()
    arqRAM.close()
    #arqSaida.close()

# Pegando informações do processador
def getProcInfo():
    comando = "Get-WmiObject -Class Win32_Processor | Select-Object -Property Name"

    result = subprocess.run(["powershell", "-Command", comando], capture_output=True, text=True)

    with open("aux.txt", "w", encoding="utf-8") as arqProcAux:
        arqProcAux.write(result.stdout)

    arqProcAux.close()

    with open("aux.txt", "r", encoding="utf-8") as arqProcAux:
        linhas = arqProcAux.readlines()

    for linha in linhas:
        if "Gen" in linha:
            with open("infos.txt", "a", encoding="utf-8") as arqSaida:
                arqSaida.writelines(f"\nProcessador: {linha}") # Essa variavel vai para o DB

    arqSaida.close()

# Pegar o usuário da máquina
def getUser():
    comando = "Get-WmiObject -Class Win32_ComputerSystem | Select-Object -Property UserName"

    result = subprocess.run(["powershell", "-Command", comando], capture_output=True, text=True)

    user = result.stdout.split('\n')[3].strip()

    with open("infos.txt", "a", encoding="utf-8") as arqSaida:
        arqSaida.write(f'Usuario:   {user}') # Essa variavel vai para o DB

    if os.path.exists('aux.txt'):
        os.remove('aux.txt')
    
    arqSaida.close()

if __name__ == '__main__':
    getSystemInfo()
    getSerialNumber()
    getDDR()
    getProcInfo()
    getUser()