# Imports dos modulos  
# Carrega o InitAllSettingsSettings Precisa ser o primeiro a ser carregado
# Imports dos pacotes externos
from webdriver_manager import chrome, firefox, microsoft
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from datetime import datetime
from pathlib import Path
from tkinter import *
import shutil, os
import uuid
import re


# Para durante a execução do maestro conseguir capturar um arquivo no resources é necessário usar dessa maneira 
ROOT_DIR = Path(__file__).parent.parent.parent

class InitAllSettings:
    """
    Classe para carregar todas as configurações necessárias.

    Parâmetros:
    
    Retorna:
    """
    var_dictConfig:dict = None
    
    @staticmethod
    def load_config() -> dict:
        """
        Carrega o arquivo de configuração Config.xlsx e retorna um dicionário com as configurações.

        Parâmetros:

        Retorna:
        - dict: dicionário com as configurações lidas do arquivo Config.xlsx.
        """
        
        # Caminho absoluto do arquivo .txt
        caminho_config = os.path.join(ROOT_DIR.__str__(), r"resources\config\Config.txt")

        # Inicializa o dicionário de configurações
        arg_dictConfig = dict()

        
        with open(caminho_config, 'r', encoding='utf-8') as f:
            for linha in f:
                linha = linha.strip()
                if linha and '=' in linha:
                    chave, valor = linha.split('=', 1)
                    chave = chave.strip()
                    valor = valor.strip()
                    # Converte para int se for um número inteiro
                    if valor.isdigit():
                        arg_dictConfig[chave] = int(valor)
                    else:
                        arg_dictConfig[chave] = valor

        return arg_dictConfig


    @classmethod
    def build(cls):
        """
        Realiza a inicialização e verificação de variaveis de configuração.
        
        Parâmetros:
           
        Retorna:
        """
        cls.var_dateDatahoraInicioExec:datetime = datetime.now()
        cls.var_strDatahoraInicioExec:str = cls.var_dateDatahoraInicioExec.strftime("%d/%m/%Y %H:%M:%S")
        cls.var_dateDatahoraFimExec:datetime = None
        cls.var_strDatahoraFimExec:str = ''
        cls.var_strGuidExecucao = str(uuid.uuid4())
        # cls.var_brwBrowserEscolhido:Browser = None
        cls.var_boolHeadless:bool = None

        # Caminhos hardcode utilizados em templates de email
        cls.var_strCaminhoTemplateEmailInicio = os.path.join(ROOT_DIR , "resources\\templates\\Email_Inicio.txt")
        cls.var_strCaminhoTemplateEmailFinal = os.path.join(ROOT_DIR , "resources\\templates\\Email_Final.txt")
        cls.var_strCaminhoTemplateEmailErroEncontrado = os.path.join(ROOT_DIR , "resources\\templates\\Email_ErroEncontrado.txt")

        # Caminho hardcode utilizados em templates e scripts para relatorio final
        cls.var_strSQLiteCaminhoBDAnalitSint = cls.var_dictConfig["CaminhoBancoSqlite"] if(cls.var_dictConfig.__contains__("CaminhoBancoSqlite")) else os.path.join(ROOT_DIR, "resources\\sqlite\\banco_dados.db")
        cls.var_strCaminhoTemplateExcelAnalitico = os.path.join(ROOT_DIR, "resources\\templates\\Relatorio_Analitico.xlsx")
        cls.var_strCaminhoTemplateExcelSintetico = os.path.join(ROOT_DIR, "resources\\templates\\Relatorio_Sintetico.xlsx")
        cls.var_strCaminhoTemplateLog = os.path.join(ROOT_DIR, "resources\\templates\\Relatorio_Log.csv")
        cls.var_strCaminhoTemplateResult = os.path.join(ROOT_DIR, "resources\\templates\\Resultados.xlsx")
        cls.var_strCaminhoPastaSaidaRelSintAnali = cls.var_dictConfig["CaminhoPastaRelatorios"] if(cls.var_dictConfig.__contains__("CaminhoPastaRelatorios")) else os.path.join(ROOT_DIR,r'classes_\relatorios\output')
        
        #Variáveis contadores já levadas em conta no framework
        cls.var_intQtdeItensProcessados:int = 0
        cls.var_intQtdeItensAppException:int = 0
        cls.var_intQtdeItensConsecutiveExceptions:int = 0
        cls.var_intQtdeItensBusinessException:int = 0
        cls.var_intQtdeItensSucesso:int = 0
        
        # Atribui as classes de manipulação de aplicações 
        cls.var_botWebbot = None
        cls.var_botDesktopbot = None

        # Variaveis de controle de excecao
        cls.var_excExceptionInitialization = None
        cls.var_excExceptionProcess = None
        cls.var_strCaminhoScreenshotErroInit = None

        # Verifica se foi preenchido no arquivo config sobre a fila de processamento, caso não, preenche com o nome padrao   
        cls.var_dictConfig["FilaProcessamento"] = cls.var_dictConfig["FilaProcessamento"] if(cls.var_dictConfig.__contains__("FilaProcessamento")) else "tbl_Fila_Processamento"
        
    @classmethod
    def initiate_web_manipulator(cls, arg_boolHeadless, arg_brwBrowserEscolhido):
        # Inicializa o bot Web com Selenium
        options = Options()
        """
        Metodo que inicia a instância do objeto que utiliza para manipular os seletores web.

        NECESSARIO SER CHAMADO APÓS UM CLOSE_PAGE()
        
        Parâmetros:
            - arg_boolHeadless (bool): indica se quer que execute o bot em modo background ou não
            - arg_brwBrowserEscolhido (Browser): indica qual browser que será utilizado
        Retorna:
        """

        # cls.var_botWebbot = WebBot(headless=arg_boolHeadless)
        # cls.var_botWebbot.browser = arg_brwBrowserEscolhido

        if arg_brwBrowserEscolhido == "CHROME":

            # Define as opções baseadas no argumento para headless
            if arg_boolHeadless:
                options.add_argument("--headless")

            var_cmChromeDriver = os.path.join(os.path.dirname(chrome.ChromeDriverManager().install()), "chromedriver.exe")

            chrome_paths = [
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                os.path.join(os.getenv('LOCALAPPDATA'), r"Google\Chrome\Application\chrome.exe"),
            ]
            for path in chrome_paths:
                if os.path.exists(path):
                    chrome_path = path
                    break

            options.binary_location = chrome_path  # <- Apontando para o chrome.exe agora, corretamente

            prefs = {
                "plugins.always_open_pdf_externally": True,
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "intl.accept_languages": "pt-BR"
            }
            options.add_experimental_option("prefs", prefs)
            options.add_argument('--force-device-scale-factor=0.67')

            service = Service(var_cmChromeDriver)

            cls.options = options
            cls.service = service
            cls.var_botWebbot = webdriver.Chrome(service=service, options=options)
            # cls.var_botWebbot.close()
                
            # elif arg_brwBrowserEscolhido == Browser.EDGE:
            #     cls.var_botWebbot.browser = arg_brwBrowserEscolhido
            #     cls.var_botWebbot.driver_path = microsoft.EdgeChromiumDriverManager().install()

            # elif arg_brwBrowserEscolhido == Browser.FIREFOX:
            #     cls.var_botWebbot.browser = arg_brwBrowserEscolhido
            #     cls.var_botWebbot.driver_path = firefox.GeckoDriverManager().install()


        
    @classmethod
    def criar_file_log(cls) :
        """
        Realiza a criação do arquivo de log.
        
        Parâmetros:
            
        Retorna:
            - str: Caminho do arquivo preenchido.
        """
        cls.var_strPathRelatorioLog:str = os.path.join(cls.var_strCaminhoPastaSaidaRelSintAnali , "Relatorio_Log_" + re.sub(string=str(cls.var_dictConfig["NomeProcesso"]),pattern=r'[\@\$%&\\\/\:\*\?\"\'<>\|~`#\^\+=\{\}\[\];\!]',repl='') + "___datetime__" + ".csv")
        cls.var_strPathRelatorioLog = cls.var_strPathRelatorioLog.replace("__datetime__",datetime.now().strftime("%m%Y"))

        #Copiando apenas se não existir
        if(not os.path.exists(cls.var_strPathRelatorioLog)):
            shutil.copy(src=InitAllSettings.var_strCaminhoTemplateLog, dst=cls.var_strPathRelatorioLog)
        

    @classmethod
    def criar_bd_csv(cls) :
        hoje = datetime.now()
        arquivo = f"Banco_dados_{hoje.strftime('%Y%m%d')}.csv"
        caminho_destino = os.path.join(ROOT_DIR, 'resources', 'fila', arquivo)
        caminho_template = os.path.join(ROOT_DIR, 'resources', 'templates', 'Banco_dados.csv')

        if not os.path.exists(caminho_destino):
            # Copia o template pronto para o caminho destino
            shutil.copyfile(caminho_template, caminho_destino)

        cls.var_strCaminhoBancoCSV = caminho_destino

    @classmethod
    def criar_resultado_xlsx(cls) :

        hoje = datetime.now()
        arquivo = f"Resultado_{hoje.strftime('%Y%m%d%H%M%S')}.xlsx"
        caminho_destino = os.path.join(ROOT_DIR, 'resources', 'relatorios', arquivo)

        if not os.path.exists(caminho_destino):
            # Copia o template pronto para o caminho destino
            shutil.copyfile(cls.var_strCaminhoTemplateResult, caminho_destino)

        cls.var_strCaminhoResultadosXLSX = caminho_destino

# Execute a função load_config para atribuir os valores do Config.xlsx ao atributo var_dictConfig
InitAllSettings.var_dictConfig = InitAllSettings.load_config()

InitAllSettings.build()

# Executa a função create_file_log para realizar a criação do arquivo de log
InitAllSettings.criar_file_log()

# Executa a função create_bd_csv para realizar a criação do arquivo de Banco em csv
InitAllSettings.criar_bd_csv()

# Executa a função criar_resultado_xlsx para realizar a criação do arquivo Resultados em XLSX
InitAllSettings.criar_resultado_xlsx()

# Inicializa manipulador web *A inicialização foi movida para o InitAllApplications*
InitAllSettings.initiate_web_manipulator(arg_boolHeadless=False,arg_brwBrowserEscolhido= 'CHROME')
