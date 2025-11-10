# Imports dos modulos  
# Carrega o InitAllSettingsSettings Precisa ser o primeiro a ser carregado
from prj_BuscaEstabelecimento.classes.framework.InitAllSettings import InitAllSettings as InitAllSettings
from prj_BuscaEstabelecimento.classes.utils.Maestro import Maestro as Maestro, LogLevel, ErrorType
from prj_BuscaEstabelecimento.classes.utils.Exceptions import BusinessRuleException


# Imports dos pacotes externos
import os, signal


class KillAllProcesses:
    """
    Classe para finalizar todos os processos necessários.
    Feita para ser invocada em casos de system exceptions no processamento, para resetar o processamento.
    Pode ser usado em outras partes do processo também, dependendo de como a automação for programada.

    Parâmetros:

    Retorna:
    """
    var_dictConfig = InitAllSettings.var_dictConfig
    var_botWebbot = InitAllSettings.var_botWebbot
    var_botDesktopbot = InitAllSettings.var_botDesktopbot

    @classmethod
    def execute(cls,arg_listNomeProcesso:list=[]):
        """
        Executa o método para finalizar os processos necessários, apenas com a estrutura em código.

        Parâmetros:
    
        Retorna:
        
        Raises:
            - BusinessRuleException: Se ocorrer um erro de regra de negócio durante o processamento.
            - Exception: Se ocorrer um erro não tratado durante o processamento.
        """
        
        #Edite o valor dessa variável a no arquivo Config.xlsx
        var_intMaxTentativas = cls.var_dictConfig["MaxRetryNumber"]

        for var_intTentativa in range(var_intMaxTentativas):

            try:
                Maestro.write_log("Finalizando processos, tentativa " + (var_intTentativa+1).__str__())
                
                for var_strNomeProcesso in arg_listNomeProcesso:
                    Maestro.write_log("Finalizando processo: " + var_strNomeProcesso)

                    os.system(f"taskkill /f /im  {var_strNomeProcesso}")

                Maestro.write_log("Aplicativos finalizados, continuando processamento...")
                break
            except BusinessRuleException as err:
                raise err
            except Exception as err:
                Maestro.write_log(arg_strMensagemLog="Erro, tentativa " + (var_intTentativa+1).__str__() + ": " + str(err), 
                                  arg_enumLogLevel=LogLevel.ERROR, 
                                  arg_enumErrorType=ErrorType.APP_ERROR)
                
                if(var_intTentativa+1 == var_intMaxTentativas):
                    raise err



