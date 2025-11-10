# Imports dos modulos  
# Carrega o InitAllSettingsSettings Precisa ser o primeiro a ser carregado
from prj_BuscaEstabelecimento.classes.framework.InitAllSettings import InitAllSettings as InitAllSettings
from prj_BuscaEstabelecimento.classes.framework.GetTransaction import GetTransaction as GetTransaction
from prj_BuscaEstabelecimento.classes.utils.Maestro import Maestro as Maestro
from prj_BuscaEstabelecimento.classes.utils.PortalGoogle import Maps


# Classe responsável pelo processamento principal, necessário preencher com o seu código no método execute
class Process:
    """
    Classe responsável pelo processamento principal.

    Parâmetros:
    
    Retorna:
    """
    var_dictConfig = InitAllSettings.var_dictConfig
    var_botWebbot = InitAllSettings.var_botWebbot
    var_botDesktopbot = InitAllSettings.var_botDesktopbot
    
    
    #Parte principal do código, deve ser preenchida pelo desenvolvedor
    #Acesse o item a ser processado pelo arg_tplQueueItem
    @classmethod
    def execute(cls):
        """
        Método principal para execução do código.

        Parâmetros:

        Retorna:
        """

        """
        Implemente aqui o seu código de execução.
        Acesse o item a ser processado usando GetTransaction.var_dictQueueItem

        GetTransaction.var_dictQueueItem['referencia'] -> referencia do item da fila (seu identificador)
        GetTransaction.var_dictQueueItem['info_adicionais'] -> Informacoes adicionais do item da fila

        Este é apenas um código exemplo 
        """             
        Maestro.write_log('Process Started')
        
        var_strStatus = ""
        var_strObservacao = ""

        var_auxiliar = Maps.pesquisar_item()
        
        if var_auxiliar == True:
            var_Status,var_Observacao = Maps.percorre_lista()
        
        return var_Status, var_Observacao     
            
            
            
        
        

        
