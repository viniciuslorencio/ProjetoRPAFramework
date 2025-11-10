# Imports dos modulos  
# Carrega o InitAllSettingsSettings Precisa ser o primeiro a ser carregado
from prj_BuscaEstabelecimento.classes.framework.InitAllSettings import InitAllSettings as InitAllSettings
from prj_BuscaEstabelecimento.classes.framework.InitAllApplications import InitAllApplications as InitAllApplications
from prj_BuscaEstabelecimento.classes.framework.KillAllProcesses import KillAllProcesses as KillAllProcesses
from prj_BuscaEstabelecimento.classes.utils.Exceptions import BusinessRuleException, TerminateException
from prj_BuscaEstabelecimento.classes.framework.GetTransaction import GetTransaction as GetTransaction
from prj_BuscaEstabelecimento.classes.utils.Maestro import Maestro as Maestro,LogLevel, ErrorType
from prj_BuscaEstabelecimento.classes.fila.DadosExecucaoCSV import BancoAtualizador
from prj_BuscaEstabelecimento.classes.email.SendEmail import SendEmail as SendEmail
from prj_BuscaEstabelecimento.classes.framework.Process import Process as Process
from prj_BuscaEstabelecimento.classes.utils.PortalGoogle import Maps
from prj_BuscaEstabelecimento.classes.framework.CloseAllApplications import CloseAllApplications



# Imports dos pacotes externos
import traceback
from datetime import datetime
from os import path
import pyautogui

class LoopStation:
    """
    Classe reponsável pela organização do código da execução dos passos categorizados como repetição para processar os itens da fila.
    
    Parâmetros:
       
    
    Retorna:
       
    """
    
    @classmethod
    def execute(cls):
        """
        Metodo de execução do loop dos itens da fila.
        
        Parâmetros:

        Retorna:

        """
        Maestro.write_log("Loop Station Started")

        GetTransaction.execute(arg_boolFirstRun=True) 
               
        ids_processados = []  # Lista para armazenar os IDs processados
        
        while GetTransaction.var_dictQueueItem is not None:
            for var_intTentativa in range(InitAllSettings.var_dictConfig["MaxRetryNumber"]):
                try:
                    
                    var_expTypeException = None
                        
                    var_dateDatahoraInicio_Item = datetime.now()
                    var_strDatahoraInicio_Item = var_dateDatahoraInicio_Item.strftime("%d/%m/%Y %H:%M:%S")

                    Maestro.write_log(arg_strMensagemLog="Tentativa: " + (var_intTentativa+1).__str__(), 
                                        arg_strReferencia=GetTransaction.var_dictQueueItem['Tipo'] )
                    
                    # Atualiza o item em processamento
                    GetTransaction.atualizador() 
                    
                    # Executando o process
                    var_strStatus,var_strObservacao = Process.execute()

                    var_dateDatahoraFim_Item = datetime.now()
                    var_strDatahoraFim_Item = var_dateDatahoraFim_Item.strftime("%d/%m/%Y %H:%M:%S")
                    
                    var_DadosXLSX = BancoAtualizador(InitAllSettings.var_strCaminhoBancoCSV)
                    var_DadosXLSX.update_fim(GetTransaction.var_dictQueueItem['ID'],var_strDatahoraInicio_Item,var_strDatahoraFim_Item,InitAllSettings.var_strCaminhoResultadosXLSX,var_strStatus,var_strObservacao)
                                        
                    # Reinicia a quantidade de tentativas consecutivas
                    InitAllSettings.var_intQtdeItensConsecutiveExceptions = 0
                    InitAllSettings.var_intQtdeItensProcessados += 1
                    
                except BusinessRuleException as err:
                    var_strTracebackErro = traceback.format_exc()

                    InitAllSettings.var_intQtdeItensConsecutiveExceptions = 0
                                        
                    var_dateDatahoraFim_Item = datetime.now()
                    var_strDatahoraFim_Item = var_dateDatahoraFim_Item.strftime("%d/%m/%Y %H:%M:%S")
                    
                    var_expTypeException = err
                    var_strCaminhoScreenshot = path.join(InitAllSettings.var_dictConfig["CaminhoExceptionScreenshots"], 
                                                         "ProcessBusExceptionScreenshot_" + var_dateDatahoraFim_Item.strftime("%d%m%Y_%H%M%S%f") + ".png")
                   
                    
                    Maestro.write_log(arg_strMensagemLog="Erro de negócio: " + var_strTracebackErro, 
                                        arg_strReferencia=GetTransaction.var_dictQueueItem['Tipo'], 
                                        arg_enumLogLevel=LogLevel.ERROR, 
                                        arg_enumErrorType=ErrorType.BUSINESS_ERROR)
                    
                    # Captura screenshot de erro Business Exception
                    pyautogui.screenshot(var_strCaminhoScreenshot)

                    CloseAllApplications.execute()
                    InitAllSettings.initiate_web_manipulator(arg_boolHeadless=False,arg_brwBrowserEscolhido= 'CHROME')                    
                    Maps.abertura_portal()

                    # Atualiza Banco CSV 
                    var_strStatus = "EXCEÇÃO DE NEGOCIO"
                    var_strObservacao = err.args[0] 
                    var_DadosXLSX = BancoAtualizador(InitAllSettings.var_strCaminhoBancoCSV)
                    var_DadosXLSX.update_fim(GetTransaction.var_dictQueueItem['ID'],var_strDatahoraInicio_Item,var_strDatahoraFim_Item,var_strCaminhoScreenshot,var_strStatus,var_strObservacao)
                    break

                except TerminateException as err:
                    # Caso seja direcionado para esse tipoe de excecao significa que o processo nao precisou seguir até o final para resultar em sucesso, preciso ser parado previamente               

                    # Realiza update na tabela de dados do item e insere que ocorreu 
                    var_DadosXLSX.update_fim(GetTransaction.var_dictQueueItem['ID'],var_strDatahoraInicio_Item,var_strDatahoraFim_Item,var_strStatus,var_strObservacao)
                    
                    # Reinicia a quantidade de tentativas consecutivas
                    InitAllSettings.var_intQtdeItensConsecutiveExceptions = 0
                    
                except Exception as err:
                    var_strTracebackErro = traceback.format_exc()

                    var_expTypeException = err
                    var_dateDatahoraFim_Item = datetime.now()
                    var_strDatahoraFim_Item = var_dateDatahoraFim_Item.strftime("%d/%m/%Y %H:%M:%S")

                    
                    Maestro.write_log(arg_strMensagemLog="Erro, tentativa " + (var_intTentativa+1).__str__() + ": " + var_strTracebackErro, 
                                      arg_strReferencia=GetTransaction.var_dictQueueItem['Tipo'], 
                                      arg_enumLogLevel=LogLevel.ERROR, arg_enumErrorType=ErrorType.APP_ERROR)
                    
                    #Tirando print de erro                 
                    var_strCaminhoScreenshot = path.join(InitAllSettings.var_dictConfig["CaminhoExceptionScreenshots"] , 
                                                            "ProcesAppExceptionScreenshot_" + var_dateDatahoraFim_Item.strftime("%d%m%Y_%H%M%S%f") + ".png")
                    
                    # Captura a tela e salva no caminho especificado
                    pyautogui.screenshot(var_strCaminhoScreenshot)
                                                                   
                    #Chamando a classe KillAllProcesses em caso de erro de aplicação
                    KillAllProcesses.execute(['excel.exe','winword.exe'])

                    CloseAllApplications.execute()
                    InitAllSettings.initiate_web_manipulator(arg_boolHeadless=False,arg_brwBrowserEscolhido= 'CHROME')                    
                    Maps.abertura_portal()

                    if not(var_intTentativa+1 == InitAllSettings.var_dictConfig["MaxRetryNumber"]):
                        continue
                    else:
                        # Marcando item como erro
                        var_strStatus = "EXCEÇÃO DE SISTEMICA"
                        var_strObservacao = "Houve um erro no processamento do item, segue caminho do print: " + var_strCaminhoScreenshot + " - Detalhes do erro: " + str(err)
                        var_DadosXLSX = BancoAtualizador(InitAllSettings.var_strCaminhoBancoCSV)
                        var_DadosXLSX.update_fim(GetTransaction.var_dictQueueItem['ID'],var_strDatahoraInicio_Item,var_strDatahoraFim_Item,var_strCaminhoScreenshot,var_strStatus,var_strObservacao)
                        InitAllSettings.var_intQtdeItensProcessados += 1
                        ids_processados.append(GetTransaction.var_dictQueueItem['ID'])
                        GetTransaction.execute() 
                        
                else:
                    #Insira aqui qualquer código necessário para voltar ao estado inicial em caso de sucesso, para executar um possivel próximo item
                    ids_processados.append(GetTransaction.var_dictQueueItem['ID'])  # Armazena o ID processado
                    GetTransaction.execute() 
                    break
            
            #Verifica se o item processado saiu do loop for com Exceção
            if type(var_expTypeException) == Exception:
                #Incrementa +1 devido a exceção do Item do Processado
                InitAllSettings.var_intQtdeItensConsecutiveExceptions += 1

                # Verifica se a quantidade maxima de erro de sistema de itens consecutivos foi atingida
                if(InitAllSettings.var_intQtdeItensConsecutiveExceptions >= InitAllSettings.var_dictConfig['MaxConsecutiveSystemExceptions']): 
                    break

        Maestro.write_log("Loop Station Finished")
        return ids_processados