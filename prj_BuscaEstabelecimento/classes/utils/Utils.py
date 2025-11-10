from selenium.webdriver.common.by import By
from prj_BuscaEstabelecimento.classes.framework.GetTransaction import GetTransaction as GetTransaction
from prj_BuscaEstabelecimento.classes.framework.InitAllSettings import InitAllSettings as InitAllSetting
from prj_BuscaEstabelecimento.classes.utils.Maestro import Maestro as Maestro, LogLevel, ErrorType
from pathlib import Path
import re

# Para durante a execução conseguir capturar um arquivo no resources é necessário usar dessa maneira 
ROOT_DIR = Path(__file__).parent.parent.parent

class Auxiliar:
    """
    Classe responsável pelo download de documentos no Ariba.

    Parâmetros:
    
    Retorna:
    """

    # Variáveis de classe
    var_dictConfig = InitAllSetting.var_dictConfig
    var_botWebbot = InitAllSetting.var_botWebbot

    def extrai_dados(arg_strTextoElemento):

        str_Texto = re.sub(r'[\uE000-\uF8FF]', '', arg_strTextoElemento)                 
        var_List = [l.strip() for l in str_Texto.splitlines() if l.strip()]
        var_RegexCEP = re.compile(r'\d{5}-\d{3}')
        var_RegexTelefone = re.compile(r'\(?\d{2}\)?\s*\d{4,5}[-\s]?\d{4}')

        var_strSite = var_strTelefone = None
        addr_parts = []

        for l in var_List:
            if var_RegexTelefone.search(l):
                var_strTelefone = re.sub(r'\D', '', var_RegexTelefone.search(l).group(0))  # só dígitos
                continue

            if '.' in l and ' ' not in l:                              
                var_strSite = l if l.startswith('http') else 'http://' + l
                continue

            # se tem CEP ou palavras típicas de endereço, consideramos parte do endereço
            if var_RegexCEP.search(l) or any(k in l for k in ('Av.', 'Rua', 'R.', 'Trav', 'Praça', 'Rod.')):
                addr_parts.append(l)
                continue

            # linhas extras também viram parte do endereço
            addr_parts.append(l)

        address = ' '.join(addr_parts) if addr_parts else None
        
        # Pega até o CEP (inclusive)
        var_RegexEnd = re.search(r'^(.*?\d{5}-\d{3})', address)   

        if var_RegexEnd:
            var_strEndereco = var_RegexEnd.group(1).strip()
        else:
            # fallback: corta antes de palavras que aparecem depois do endereço
            var_strEndereco = re.split(r'\bLocalizado\b|\bAberto\b', address, maxsplit=1)[0].strip()

        return var_strEndereco, var_strTelefone, var_strSite