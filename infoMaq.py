import subprocess
import os
import sqlite3
import psutil


class DataCollector:
    def __init__(self):
        self.conn = sqlite3.connect('C:\\Users\\iagos\\OneDrive\\Área de Trabalho\\Internship\\InfoMaq\\Data.db')
        self.cursor = self.conn.cursor()

    # Pegando informações do SO e quantos GB RAM:
    def getSystemInfo(self):

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
        fabricante_sistema = variaveis.get("Fabricante do sistema")

        return nome_sistema_operacional, modelo_sistema, memoria_fisica_total, fabricante_sistema

    # Pegando número de série da máquina
    def getSerialNumber(self):

        comando = "Get-WmiObject -Class Win32_BIOS | Select-Object -Property SerialNumber"

        result = subprocess.run(["powershell", "-Command", comando], capture_output=True, text=True)

        serial_number = result.stdout.split('\n')[3].strip() # Variavel que vai pro DB
        
        return serial_number

    # Pegando qual DDR é a Mem Ram
    def getDDR(self):

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

        arqMemory.close()
        arqRAM.close()
        
        return clock_speed, tipo

    # Pegando informações do processador
    def getProcInfo(self):

        comando = "Get-WmiObject -Class Win32_Processor | Select-Object -Property Name"

        result = subprocess.run(["powershell", "-Command", comando], capture_output=True, text=True)

        with open("aux.txt", "w", encoding="utf-8") as arqProcAux:
            arqProcAux.write(result.stdout)

        arqProcAux.close()

        with open("aux.txt", "r", encoding="utf-8") as arqProcAux:
            linhas = arqProcAux.readlines()

        for linha in linhas:
            if "Gen" in linha:
                proc = linha

        return proc

    # Pegar o usuário da máquina
    def getUser(self):
        comando = "Get-WmiObject -Class Win32_ComputerSystem | Select-Object -Property UserName"

        result = subprocess.run(["powershell", "-Command", comando], capture_output=True, text=True)

        user = result.stdout.split('\n')[3].strip()

        if os.path.exists('aux.txt'):
            os.remove('aux.txt')

        return user    

    # Pega o status do Anti Virus (Quando for colocar na produção, trocar o nome do serviço)
    def getStatusAntVirus(self):
        for service in psutil.win_service_iter():
            if service.name() == 'mpssvc':
                status = service.status()
        
        return status

    # Inicia a coleta
    def initCollect(self):

        # Criando a tabela (schema)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS infomaq (
                        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                        Proc TEXT,
                        User TEXT,
                        OpSis TEXT,
                        FabSis TEXT,
                        ModelSis TEXT,
                        RamMem TEXT,
                        Serial TEXT,
                        ClockRam TEXT,
                        DDR TEXT,
                        AntiVirus TEXT);
    """)
    
        op_sis, model_sis, mem_ram, fab_sis = self.getSystemInfo()
        serial = self.getSerialNumber()
        clock_speed, ddr = self.getDDR()
        proc = self.getProcInfo()
        user = self.getUser()
        status = self.getStatusAntVirus()

        self.cursor.execute("""INSERT INTO infomaq (OpSis, ModelSis, FabSis,RamMem, Serial, ClockRam, DDR, Proc, User, AntiVirus) VALUES (?,?,?,?,?,?,?,?,?,?)
                    """, (op_sis, model_sis, fab_sis, mem_ram, serial, clock_speed, ddr, proc, user, status))
        
        self.conn.commit()

