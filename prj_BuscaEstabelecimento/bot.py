# Imports dos modulos  
# Carrega o InitAllSettingsSettings Precisa ser o primeiro a ser carregado
from prj_BuscaEstabelecimento.classes.framework.InitAllSettings import InitAllSettings as InitAllSettings
from prj_BuscaEstabelecimento.classes.framework.Initialization import Initialization as Initialization
from prj_BuscaEstabelecimento.classes.framework.LoopStation import LoopStation as LoopStation
from prj_BuscaEstabelecimento.classes.framework.EndProcess import EndProcess as EndProcess
from prj_BuscaEstabelecimento.classes.utils.Maestro import Maestro as Maestro
from prj_BuscaEstabelecimento.classes.utils.Exceptions import *

# Imports dos pacotes externos'
import traceback

class Bot():
    """
    Classe que utiliza as funcionalidades da classe WebBot.
    
    Parâmetros:

    Retorna:
    """

    def action(self, execution=None):
        """
        Método principal para execução do bot.

        Parâmetros:
        - execution (objeto): objeto de execução (opcional, default=None).

        Retorna:
        """
        try:
            
            Maestro.write_log("Iniciando execução do processo: " + Maestro.var_strNomeProcesso)

            Initialization.execute()

            var_IdsProcessados = LoopStation.execute()
          
        except TerminateException as err:
            var_strTracebackErro = traceback.format_exc()
            print(var_strTracebackErro)
        
        
        except Exception as err:
            var_strTracebackErro = traceback.format_exc()
            if InitAllSettings.var_excExceptionInitialization is None:
                InitAllSettings.var_excExceptionProcess = err
            print(var_strTracebackErro)

        try:
            EndProcess.execute(var_IdsProcessados)
                                                
        except Exception as err:
            var_strTracebackErro = traceback.format_exc()
            print(var_strTracebackErro)
            Maestro.send_error(err)
           
            
if __name__ == '__main__':
    bot_instance = Bot()
    bot_instance.action()

