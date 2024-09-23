from service import MyService

if __name__ == '__main__':
    myservice = MyService()
    myservice.initJob()
    
# Criar Serviço: sc create NomeDoServiço binPath= "Caminho do Arquivo .exe"
# Config: sc config NomeDoServiço start= auto
# Iniciar: sc start NomeDoServiço