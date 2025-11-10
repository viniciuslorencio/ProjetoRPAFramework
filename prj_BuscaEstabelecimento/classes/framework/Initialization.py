# Imports dos modulos  
# Carrega o InitAllSettingsSettings Precisa ser o primeiro a ser carregado
from prj_BuscaEstabelecimento.classes.framework.InitAllApplications import InitAllApplications as InitAllApplications
from prj_BuscaEstabelecimento.classes.framework.KillAllProcesses import KillAllProcesses as KillAllProcesses
from prj_BuscaEstabelecimento.classes.framework.InitAllSettings import InitAllSettings as InitAllSettings
from prj_BuscaEstabelecimento.classes.fila.DadosExecucaoCSV import BancoAtualizador
from prj_BuscaEstabelecimento.classes.utils.Exceptions import BusinessRuleException
from prj_BuscaEstabelecimento.classes.email.SendEmail import SendEmail as SendEmail
import prj_BuscaEstabelecimento.classes.utils.GenericReusable as GenericReusable
from prj_BuscaEstabelecimento.classes.utils.Maestro import Maestro as Maestro

# Imports dos pacotes externos
from datetime import datetime
from os import path
import traceback
import pyautogui


class Initialization:
    """
    Classe Reponsavel pela organização do código da execução dos passos categorizados como inicialização
    
    Parâmetros:
    
    Retorna:
       
    """

    @staticmethod
    def execute():
        """
        Funcao de execução da inicialização.
        
        Parâmetros:

        Retorna:

        """
        try:
            Maestro.write_log("Initialization Started")
            
            #Verifica estado de operação da maquina 
            GenericReusable.get_computer_usage()  

            var_BancoXlsx = BancoAtualizador(InitAllSettings.var_strCaminhoBancoCSV)
            var_intQtdItensAProcessar = var_BancoXlsx.contar_itens_status_new()
            Maestro.write_log("Itens encontrados na fila antes de adicionar novos itens a fila: " + var_intQtdItensAProcessar.__str__())
            
            # Enviando email de inicialização
            if(InitAllSettings.var_dictConfig["EmailInicial"].upper() == "SIM"):
                SendEmail.configure_email()
                
                SendEmail.send_email_inicial(arg_strEnvioPara=InitAllSettings.var_dictConfig["EmailDestinatarios"])

            # Finaliza os aplicativos antes de iniciar as novas aplicações
            KillAllProcesses.execute(['excel.exe','winword.exe'])

            # Realiza a inicialização das aplicações
            InitAllApplications.execute(arg_boolFirstRun=True)
            
            # Atualiza no InitAllSettings a quantidade de itens que estão a serem processados
            InitAllSettings.var_intQtdItensAProcessarIniExec = var_intQtdItensAProcessar = var_BancoXlsx.contar_itens_status_new()

            Maestro.write_log("Initialization Finished")

        except BusinessRuleException as err:

            # Captura todo detalhe do erro
            var_strTracebackErro = traceback.format_exc()
            InitAllSettings.var_excExceptionInitialization = err

            #Tirando print do erro antes de fechar
            var_strCaminhoScreenshot = path.join(InitAllSettings.var_dictConfig["CaminhoExceptionScreenshots"] , "InitBusExceptionScreenshot_" + datetime.now().strftime("%d%m%Y_%H%M%S%f") + ".png")
            pyautogui.screenshot(path=var_strCaminhoScreenshot)
            InitAllSettings.var_strCaminhoScreenshotErroInit = var_strCaminhoScreenshot

            Maestro.send_error(err,var_strCaminhoScreenshot)

            raise err
        except Exception as err:
            
            # Captura todo detalhe do erro
            var_strTracebackErro = traceback.format_exc()
            InitAllSettings.var_excExceptionInitialization = err

            #Tirando print do erro antes de fechar
            var_strCaminhoScreenshot = path.join(InitAllSettings.var_dictConfig["CaminhoExceptionScreenshots"] , "InitAppExceptionScreenshot_" + datetime.now().strftime("%d%m%Y_%H%M%S%f") + ".png")
            pyautogui.screenshot(path=var_strCaminhoScreenshot)
            InitAllSettings.var_strCaminhoScreenshotErroInit = var_strCaminhoScreenshot
                       
            Maestro.send_error(err,var_strCaminhoScreenshot)
            
            raise err
            