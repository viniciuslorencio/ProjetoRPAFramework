# Imports dos modulos  
# Carrega o InitAllSettingsSettings Precisa ser o primeiro a ser carregado
from prj_BuscaEstabelecimento.classes.framework.InitAllSettings import InitAllSettings as InitAllSettings
from prj_BuscaEstabelecimento.classes.utils.Maestro import Maestro as Maestro,LogLevel, ErrorType
from prj_BuscaEstabelecimento.classes.fila.DadosExecucaoCSV import BancoAtualizador

# Imports dos pacotes externos


class GetTransaction:
    """
    Classe Reponsavel pela organização do código da execução dos passos categorizados como itens de fila
    
    Parâmetros:
  
    Retorna:
    """
    var_dictQueueItem:dict = None

    @classmethod
    def execute(cls):
        """
        Metodo de execução da captura de itens da fila.
        
        Parâmetros:

        Retorna:

        """
        #Verifica a quantidade itens NEW
        var_ItensFila = BancoAtualizador(InitAllSettings.var_strCaminhoBancoCSV)
        var_intQtdItensAProcessarIniExec = var_ItensFila.contar_itens_status_new()
        cls.var_dictQueueItem = var_ItensFila.obter_proximo_item_status_new()
            

        #Processamento continua até a classe informar que não existe itens novos para processar
        if(cls.var_dictQueueItem is not None): 
            Maestro.write_log(f"{str(InitAllSettings.var_intQtdeItensProcessados)} itens processados de {var_intQtdItensAProcessarIniExec} totais para serem processados.")
            Maestro.write_log(arg_strMensagemLog="Executando item, Tipo: " + cls.var_dictQueueItem['Tipo'] + "," + " Cidade: " + cls.var_dictQueueItem['Cidade']+ ".")

        else: 
            Maestro.write_log("Não existem itens a serem processados.")
            cls.var_dictQueueItem = None
            
    @classmethod
    def atualizador(cls):
        
        var_ItensFila = BancoAtualizador(InitAllSettings.var_strCaminhoBancoCSV)
        cls.var_dictQueueItem = var_ItensFila.atualiza_item_em_processamento(cls.var_dictQueueItem['ID'])
        
        
    
