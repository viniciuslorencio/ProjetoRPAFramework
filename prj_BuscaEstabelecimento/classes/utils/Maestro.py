# Imports dos modulos  
# Carrega o InitAllSettingsSettings Precisa ser o primeiro a ser carregado
from prj_BuscaEstabelecimento.classes.framework.InitAllSettings import InitAllSettings as InitAllSettings


# Imports dos pacotes externos
import random, datetime, socket
from datetime import datetime
from enum import Enum
import csv
import os

class LogLevel(Enum):
    """
    Classe enum, usada para colocar o nível de um novo log.
    
    Parâmetros:

    Retorna:
    """

    INFO = "INFO"
    WARN = "WARN"
    ERROR = "ERROR"
    FATAL = "FATAL"

class ErrorType(Enum):
    """
    Classe enum, usada para colocar o tipo do erro.
    
    Parâmetros:
    
    Retorna:
    """
    
    NONE = ""
    APP_ERROR = "APPLICATION"
    BUSINESS_ERROR = "BUSINESS"
    
class Maestro:
    """
    Classe responsável por todas as interações com o Maestro durante a execução, estabelecendo uma conexão com o Maestro, criando logs para o projeto e armazenando dados referente a execução em variáveis dentro da classe.
    var_clssExecution (BotExecution): Execução do projeto, nulo se estiver rodando localmente.

    Parâmetros:

    
    Retorna:
    """
    # Variaveis que podem ser acessadas externamente ao importar a classe em outros modulos
    var_dictConfig = InitAllSettings.var_dictConfig
    # var_clssExecution:BotExecution = None
    var_clssMaestroInit = None
    var_strNomeProcesso:str = var_dictConfig["NomeProcesso"]
    var_clssTask = None
    var_boolIsRunningFromTask:bool = None
    var_boolIsTestTask:bool = None
    var_strRunnerId:str = None
    var_strVersaoRunner:str = 'X.X.X'
    var_boolUsingMaestro:bool = True
    var_intJobId = 0


    @classmethod
    def write_log(cls, arg_strMensagemLog: str, arg_strReferencia: str = "-", arg_enumLogLevel=LogLevel.INFO, arg_enumErrorType=ErrorType.NONE):
        # Caminho do arquivo CSV de log
        var_strArquivoLog = InitAllSettings.var_strPathRelatorioLog
        var_dictConfig = InitAllSettings.var_dictConfig

        # Verifica se o arquivo já existe para decidir se precisa escrever o cabeçalho
        file_exists = os.path.isfile(var_strArquivoLog)

        # Obtém a data e hora atual no formato desejado
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Abre o arquivo em modo append ('a') e escreve os dados
        with open(var_strArquivoLog, mode='a', newline='', encoding='utf-8-sig') as csv_file:
            writer = csv.writer(csv_file)

            # Escreve o cabeçalho apenas se for a primeira criação do arquivo
            if not file_exists:
                writer.writerow(["Data/Hora", "ProcessName", "Companhia", "LogLevel", "Message", "ErrorType"])

            # Escreve a nova linha com os dados do log
            writer.writerow([
                current_datetime,
                cls.var_strNomeProcesso,
                arg_strReferencia,
                arg_enumLogLevel.name,
                arg_strMensagemLog,
                arg_enumErrorType.name
            ])

        # Também imprime a mensagem no console
        print("- " + arg_strMensagemLog)
                
    @classmethod
    def send_error(cls, arg_excException:Exception, arg_strScreenshot:str=None):
        """
        Gera um erro no errors do maestro sobre a task da execucao atual.
        O erro será gerado somente se o projeto estiver executando via Maestro.
        
        Parâmetros:
        - arg_expException (Exception): Exceção que ocorreu na execução do projeto
        - arg_strScreenshot (str): Caminho da Screenshot do Erro

        Retorna:        
        """
        if(cls.var_boolIsRunningFromTask):
            cls.var_clssMaestroInit.error(task_id=cls.var_clssTask.id, 
                                          exception=arg_excException, 
                                          screenshot=arg_strScreenshot)

    


