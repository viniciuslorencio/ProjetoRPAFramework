# Imports dos modulos  
# Carrega o InitAllSettingsSettings Precisa ser o primeiro a ser carregado
from prj_BuscaEstabelecimento.classes.framework.InitAllSettings import InitAllSettings as InitAllSetting
from prj_BuscaEstabelecimento.classes.utils.Maestro import Maestro as Maestro, LogLevel, ErrorType
from prj_BuscaEstabelecimento.classes.utils.Exceptions import BusinessRuleException
#FIXME Código Exemplo REMOVER

# Imports dos pacotes externos


class CloseAllApplications:
    """
    Classe para fechar todos os aplicativos no final da automação.

    Parâmetros:
    
    Retorna:
    """
    var_dictConfig = InitAllSetting.var_dictConfig
    var_botWebbot = InitAllSetting.var_botWebbot
    
    @classmethod
    def execute(cls):
        """
        Executa o fechamento de todos os aplicativos necessários, apenas com a estrutura em código.

        Observação:
        - Edite o valor da variável `var_intMaxTentativas` no arquivo Config.xlsx.

        Parâmetros:
        
        Retorna:

        Raises:
        - BusinessRuleException: em caso de erro de regra de negócio.
        - Exception: em caso de erro geral.
        """
        #Edite o valor dessa variável a no arquivo Config.xlsx
        var_intMaxTentativas = cls.var_dictConfig["MaxRetryNumber"]

        for var_intTentativa in range(var_intMaxTentativas):
            try:
                Maestro.write_log("Finalizando todos os processos, tentativa " + (var_intTentativa+1).__str__())
                #Insira aqui seu código para fechar os aplicativos
                             
                InitAllSetting.var_botWebbot.close()

            except BusinessRuleException as err:
                Maestro.write_log(arg_strMensagemLog="Erro de negócio: " + str(err), 
                                  arg_enumLogLevel=LogLevel.ERROR, arg_enumErrorType=ErrorType.BUSINESS_ERROR)
                raise err
            except Exception as err:
                Maestro.write_log(arg_strMensagemLog="Erro, tentativa " + (var_intTentativa+1).__str__() + ": " + str(err),
                                  arg_enumLogLevel=LogLevel.ERROR, arg_enumErrorType=ErrorType.APP_ERROR)
                
                if(var_intTentativa+1 == var_intMaxTentativas): 
                    raise err
                else: 
                    # Inclua aqui o código responsável para reiniciar ao estado indicado para iniciar as aplicações novamente
                    
                    continue
            else:
                Maestro.write_log("Aplicativos finalizados, continuando processamento...")
                break
            