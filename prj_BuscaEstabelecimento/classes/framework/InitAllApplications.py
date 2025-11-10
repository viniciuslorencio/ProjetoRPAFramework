# Imports dos modulos  
# Carrega o InitAllSettingsSettings Precisa ser o primeiro a ser carregado
from prj_BuscaEstabelecimento.classes.framework.InitAllSettings import InitAllSettings as InitAllSettings
from prj_BuscaEstabelecimento.classes.utils.Maestro import Maestro as Maestro, LogLevel, ErrorType
from prj_BuscaEstabelecimento.classes.fila.DadosExecucaoCSV import BancoAtualizador
from prj_BuscaEstabelecimento.classes.utils.Exceptions import BusinessRuleException
from prj_BuscaEstabelecimento.classes.utils.PortalGoogle import Maps
from prj_BuscaEstabelecimento.classes.framework.CloseAllApplications import CloseAllApplications


#FIXME Código Exemplo REMOVER

# Imports dos pacotes externos

import pandas as pd
import time
import os


class InitAllApplications:
    """
    Classe feita para Iniciar as aplicações de inicio de processo e também preencher a fila caso seja um processo simples para capturar
    itens que vão para a fila.
        
    Parâmetros:

    Retorna:
    """
    var_botWebbot = InitAllSettings.var_botWebbot
    var_dictConfig:dict = InitAllSettings.var_dictConfig

    @classmethod
    def add_to_queue(cls):
        """
        Adiciona itens à fila no início do processo, se necessário.

        Observação:
        - Código placeholder.
        - Se o seu projeto precisa de mais do que um método simples para subir a sua fila, considere fazer um projeto dispatcher.

        Parâmetros:
        """
        #FIXME Código Exemplo REMOVER

    
    @classmethod
    def execute(cls, arg_boolFirstRun):
        
        
        """
        Executa a inicialização dos aplicativos necessários.

        
        Parâmetros:
        - arg_boolFirstRun (bool): indica se é a primeira execução (default=False).
        
        Observação:
        - Edite o valor da variável `var_intMaxTentativas` no arquivo Config.xlsx.
        
        Retorna:
        """
        # Caminho absoluto base do projeto
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

        # Caminho completo até o novo arquivo JSON
        var_strCaminhoArquivoJson = os.path.join(base_dir, cls.var_dictConfig["NomeArquivoJson"])

        # Leitura do JSON
        var_dtFilaFinal = pd.read_json(var_strCaminhoArquivoJson, orient='records')        

        arg_boolFirstRun=True

        #Chama o método para subir a fila, apenas se for a primeira vez
        if(arg_boolFirstRun):
            # Realiza insert na planilha de gerenciamento fila              
            atualizador = BancoAtualizador(InitAllSettings.var_strCaminhoBancoCSV)
            atualizador.insert(var_dtFilaFinal)
            cls.add_to_queue()

        Maestro.write_log("InitAllApplications Started")

        #Edite o valor dessa variável a no arquivo Config.xlsx
        var_intMaxTentativas = cls.var_dictConfig["MaxRetryNumber"]
        
        for var_intTentativa in range(var_intMaxTentativas):
            try:

                Maestro.write_log("Iniciando aplicativos, tentativa " + (var_intTentativa+1).__str__())

                # Realiza login no portal
                Maps.abertura_portal()
                
                time.sleep(5)


            except BusinessRuleException as err:
                raise err
            
            except Exception as err:
                Maestro.write_log(arg_strMensagemLog="Erro, tentativa " + (var_intTentativa+1).__str__() + ": " + str(err), arg_enumLogLevel=LogLevel.ERROR, arg_enumErrorType=ErrorType.APP_ERROR)                              
                
                if(var_intTentativa+1 == var_intMaxTentativas): 
                    raise err
                
                else: 

                    CloseAllApplications.execute()

                    InitAllSettings.initiate_web_manipulator(arg_boolHeadless=False,arg_brwBrowserEscolhido= 'CHROME')
                    continue
            else:
                Maestro.write_log("InitAllApplications Finished")
                break
            
