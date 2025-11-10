# Imports dos modulos  
# Carrega o InitAllSettingsSettings Precisa ser o primeiro a ser carregado
from prj_BuscaEstabelecimento.classes.framework.CloseAllApplications import CloseAllApplications as CloseAllApplications
from prj_BuscaEstabelecimento.classes.framework.KillAllProcesses import KillAllProcesses as KillAllProcesses
from prj_BuscaEstabelecimento.classes.framework.InitAllSettings import InitAllSettings as InitAllSettings
from prj_BuscaEstabelecimento.classes.utils.Maestro import Maestro as Maestro,LogLevel
from prj_BuscaEstabelecimento.classes.relatorios.Relatorios import Relatorios as Relatorios
from prj_BuscaEstabelecimento.classes.email.SendEmail import SendEmail as SendEmail

# Imports dos pacotes externos
from datetime import datetime
from os import path
from os import remove

class EndProcess:
    """
    Classe reponsável pela organização do código da execução dos passos categorizados como finalização da execução.
    
    Parâmetros:
       
    
    Retorna:
       
    """
    
    
    @classmethod
    def execute(cls,var_IdsProcessados):
        """
        Metodo de execução dos passos da finalização da execucao
        
        Parâmetros:

        Retorna:

        """
        Maestro.write_log("End Process Started")

        InitAllSettings.var_dateDatahoraFimExec = datetime.now()
        InitAllSettings.var_strDatahoraFimExec = InitAllSettings.var_dateDatahoraFimExec.strftime("%d/%m/%Y %H:%M:%S")

        #Fechando aplicativos no final do processamento
        try:
            CloseAllApplications.execute()
        except Exception as err:
            Maestro.write_log(arg_strMensagemLog="Fechando aplicativos pelo KillAllProcesses", arg_enumLogLevel=LogLevel.WARN)
            KillAllProcesses.execute(['excel.exe','winword.exe', 'chrome.exe'])


        var_strCaminhoRelatorioAnalitico = Relatorios.preencher_analitico(var_IdsProcessados)
        var_strCaminhoRelatorioSintetico = Relatorios.preencher_sintetico(var_IdsProcessados)

        #Enviando email final com os relatórios analítico e sintético
        if(InitAllSettings.var_dictConfig["EmailFinal"].upper() == "SIM"):  
            
            SendEmail.send_email_final(arg_strEnvioPara=InitAllSettings.var_dictConfig["EmailDestinatarios"], 
                                       arg_listAnexos=[var_strCaminhoRelatorioAnalitico,var_strCaminhoRelatorioSintetico,InitAllSettings.var_strCaminhoResultadosXLSX], 
                                       arg_boolSucesso=True)

            # Deleta arquivo excel sintetico e analitico caso exista
            if path.exists(var_strCaminhoRelatorioAnalitico):
                remove(var_strCaminhoRelatorioAnalitico)
                    
        Maestro.write_log("Finalizando task.")

        
        if InitAllSettings.var_excExceptionInitialization is not None:
            Maestro.send_error(InitAllSettings.var_excExceptionInitialization)
            Maestro.write_log(arg_boolSucesso=False, arg_strMensagemLog="Task finalizada com falha na inicialização, verifique os logs de execução.")
            
            
        elif InitAllSettings.var_excExceptionProcess is not None:
            Maestro.send_error(InitAllSettings.var_excExceptionProcess)
            Maestro.write_log(arg_boolSucesso=False, arg_strMensagemLog="Task finalizada com falha na fase de processamento, verifique os logs de execução.")
        else: 
            Maestro.write_log(arg_strMensagemLog="Task finalizada com sucesso.")
            
        Maestro.write_log("End Process Finished")