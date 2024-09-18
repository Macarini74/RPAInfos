from service import MyService
import win32serviceutil
import logging

# Configuração do logging
logging.basicConfig(filename='service_log.txt', level=logging.DEBUG, 
                    format='%(asctime)s %(levelname)s %(message)s')

logging.debug("Iniciando o script main.py")

if __name__ == '__main__':
    try:
        logging.debug("Tentando instalar o servico.")
        win32serviceutil.HandleCommandLine(MyService)
    except Exception as e:
        logging.error(f'Erro ao instalar o serviço: {e}')
