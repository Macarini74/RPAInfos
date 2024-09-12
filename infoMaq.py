import subprocess
import os

# Pegando informações do SO e quantos GB RAM:
def getSystemInfo():
    comando = "systeminfo"

    result = subprocess.run(["powershell", "-Command", comando], capture_output=True, text=True)

    with open("aux.txt", "w", encoding="utf-8") as arqInfo:
        arqInfo.write(result.stdout)

    arqInfo.close()

    with open("aux.txt", "r", encoding="utf-8") as arqInfo:
        linhas = arqInfo.readlines()

    linhas_desejadas = []

    for linha in linhas:
        if "Nome do sistema operacional" in linha or \
        "Fabricante do sistema" in linha or \
        "Modelo do sistema" in linha or \
        "Mem¢ria f¡sica total" in linha:
            linhas_desejadas.append(linha)

    with open("infos.txt", "w", encoding="utf-8") as arqSaida:
        arqSaida.writelines(linhas_desejadas)

    arqSaida.close()

# Pegando número de série da máquina
def getSerialNumber():
    comando = "Get-WmiObject -Class Win32_BIOS | Select-Object -Property SerialNumber"

    result = subprocess.run(["powershell", "-Command", comando], capture_output=True, text=True)

    with open("infos.txt", "a", encoding="utf-8") as arqSerial:
        arqSerial.write(result.stdout)
    
    arqSerial.close()

# Pegando qual DDR é a Mem Ram
def getDDR():
    comando = "Get-WmiObject -Class Win32_PhysicalMemory | Format-List *"

    result = subprocess.run(["powershell", "-Command", comando], capture_output=True, text=True)

    with open("aux.txt", "w", encoding="utf-8") as arqMemory:
        arqMemory.write(result.stdout)


    with open("aux.txt", "r", encoding="utf-8") as arqRAM:
        linhas = arqRAM.readlines()

    linhas_desejadas = []

    for linha in linhas:
        if "ConfiguredClockSpeed" in linha:
            linhas_desejadas.append(linha)
        elif "SMBIOSMemoryType" in linha:
            if "20" in linha:
                tipo = 'Tipo DDR1\n'
            if "21" in linha:
                tipo = 'Tipo DDR2\n'
            if "24" in linha:
                tipo = 'Tipo DDR3\n'
            if "26" in linha:
                tipo = 'Tipo DDR4\n'
            if "27" in linha:
                tipo = 'Tipo DDR5\n'
            linhas_desejadas.append(tipo)

    with open("infos.txt", "a", encoding="utf-8") as arqSaida:
        arqSaida.writelines(linhas_desejadas)

    arqMemory.close()
    arqRAM.close()
    arqSaida.close()

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
                arqSaida.writelines(f"\nProcessador: {linha}")

    arqSaida.close()

# Pegar o usuário da máquina
def getUser():
    comando = "Get-WmiObject -Class Win32_ComputerSystem | Select-Object -Property UserName"

    result = subprocess.run(["powershell", "-Command", comando], capture_output=True, text=True)

    with open("infos.txt", "a", encoding="utf-8") as arqSaida:
        arqSaida.write(result.stdout)

    if os.path.exists('aux.txt'):
        os.remove('aux.txt')
    
    arqSaida.close()

if __name__ == '__main__':
    getSystemInfo()
    getSerialNumber()
    getDDR()
    getProcInfo()
    getUser()