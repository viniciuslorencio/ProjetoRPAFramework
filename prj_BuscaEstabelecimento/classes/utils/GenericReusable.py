# Imports dos modulos  
# Carrega o InitAllSettingsSettings Precisa ser o primeiro a ser carregado
from prj_BuscaEstabelecimento.classes.utils.Maestro import Maestro as Maestro, LogLevel, ErrorType


# Imports dos pacotes externos
import base64
import psutil


def get_computer_usage() -> str:
   """
   Retorna a quantidade de Memoria Ram, CPU e Disco Utilizada no momento do processamento
   
   Parâmetros:

   Retorna:
      - str: texto contendo a quantidade de Memoria Ram, CPU e Disco Utilizada no momento do processamento
   """
   var_strPorcentagemMemUtilizada = f"A porcentagem de Memória RAM utilizada é de {str(psutil.virtual_memory().percent)}"
   var_strPorcentagemCPUUtilizada = f"A porcentagem de CPU utilizada é de {str(psutil.cpu_percent())}"
   var_strPorcentagemDiscoUtilizada = f"A porcentagem de Disco utilizada é de {str(psutil.disk_usage('/').percent)}"


   var_strComputerUsage = '\n'.join([var_strPorcentagemMemUtilizada,var_strPorcentagemCPUUtilizada,var_strPorcentagemDiscoUtilizada])
   Maestro.write_log(var_strPorcentagemMemUtilizada)
   Maestro.write_log(var_strPorcentagemCPUUtilizada)
   Maestro.write_log(var_strPorcentagemDiscoUtilizada)

   return var_strComputerUsage

