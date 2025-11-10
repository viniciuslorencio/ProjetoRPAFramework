# Imports dos modulos  
# Carrega o InitAllSettingsSettings Precisa ser o primeiro a ser carregado
from prj_BuscaEstabelecimento.classes.framework.InitAllSettings import InitAllSettings as InitAllSettings 
from prj_BuscaEstabelecimento.classes.utils.Maestro import Maestro as Maestro, LogLevel, ErrorType

# Imports dos pacotes externos
from email.message import EmailMessage
import mimetypes
import smtplib

class SendEmail:
    """
    Classe responsável pelo envio de email, enviando usuario, senha e qual servidor vai ser usado
    
    Parâmetros:

    Retorna:

    """

    @classmethod
    def configure_email(cls):
        """
        Realiza as configuracoes de email que fica atrelada a classe
        
        Parâmetros:
            - arg_strEmailServerSmtp (str): endereço do servidor SMTP.
            - arg_intEmailPortaSmtp (int): porta do servidor SMTP.
            - arg_strUsuario (str): nome de usuário para autenticação.
            - arg_strSenha (str): senha para autenticação.
            - arg_clssMaestro (Maestro): instância de Maestro.
        Retorna:
           
        """
        cls.var_strEmailServerSmtp = InitAllSettings.var_dictConfig['SmtpServer']
        cls.var_intEmailPortaSmtp = InitAllSettings.var_dictConfig['SmtpPort']
        cls.var_strUsuario = InitAllSettings.var_dictConfig['EmailUser']
        cls.var_strSenha = InitAllSettings.var_dictConfig['EmailSenha']
        cls.var_strNomeProcesso = InitAllSettings.var_dictConfig['NomeProcesso']
        
    @classmethod
    def send_email_inicial(cls, arg_strEnvioPara:str, arg_strCC:str=None, arg_strBCC:str=None):
        """
        Envia o email inicial do robô, apenas precisando informar quem deve receber (separado por ;) e o nome do robô

        Parâmetros:
        - arg_strEnvioPara (str): destinatários separados por ';'.
        - arg_strCC (str): destinatários em cópia separados por ';'. (opcional, default=None)
        - arg_strBCC (str): destinatários em cópia oculta separados por ';'. (opcional, default=None)

        Retorna:

        """

        #Lendo template
        var_fileTemplate = open(InitAllSettings.var_strCaminhoTemplateEmailInicio, mode="r",encoding="utf-8")
        var_strEmailTexto = var_fileTemplate.read()
        var_fileTemplate.close()

        var_strEmailTexto = var_strEmailTexto.replace("*NOME_ROBO*", cls.var_strNomeProcesso)
        var_strEmailAssunto = "Inicio execução: " + cls.var_strNomeProcesso
        
        var_listEnvioPara = arg_strEnvioPara.split(";") if(arg_strEnvioPara is not None) else []
        var_listCC = arg_strCC.split(";") if(arg_strCC is not None) else []
        var_listBCC = arg_strBCC.split(";") if(arg_strBCC is not None) else []

        smtp = None

        # Configurando SMTP (Gmail) e fazendo login
        try:
            Maestro.write_log("Configurando SMTP do Gmail para envio")

            smtp = smtplib.SMTP(cls.var_strEmailServerSmtp, cls.var_intEmailPortaSmtp)
            smtp.starttls()  
            smtp.login(cls.var_strUsuario, cls.var_strSenha)

            Maestro.write_log("SMTP do Gmail configurado com sucesso")
        except Exception as err:
            Maestro.write_log(
                arg_strMensagemLog="Erro configurando SMTP do Gmail: " + str(err),
                arg_enumLogLevel=LogLevel.ERROR,
                arg_enumErrorType=ErrorType.APP_ERROR
            )
            raise err

        # Monta e envia o e-mail inicial
        try:
            Maestro.write_log("Montando e enviando e-mail inicial via Gmail")

            var_Mensagem = EmailMessage()
            var_Mensagem["From"] = cls.var_strUsuario
            var_Mensagem["To"] = ", ".join(var_listEnvioPara) if var_listEnvioPara else ""
            if var_listCC:
                var_Mensagem["Cc"] = ", ".join(var_listCC)
            var_Mensagem["Subject"] = var_strEmailAssunto

            var_Mensagem.add_alternative(var_strEmailTexto, subtype="html")

            var_strDestinatarios = (var_listEnvioPara or []) + (var_listCC or []) + (var_listBCC or [])

            smtp.send_message(var_Mensagem, from_addr=cls.var_strUsuario, to_addrs=var_strDestinatarios)

            Maestro.write_log("E-mail inicial enviado com sucesso via Gmail")

        except Exception as err:
            Maestro.write_log(
                arg_strMensagemLog="Erro enviando e-mail inicial via Gmail: " + str(err),
                arg_enumLogLevel=LogLevel.ERROR,
                arg_enumErrorType=ErrorType.APP_ERROR
            )
            raise err
        
        finally:
            if smtp is not None:
                try:
                    smtp.quit()
                except:
                    pass
   
    
    @classmethod
    def send_email_final(cls, arg_strEnvioPara:str, arg_strCC:str=None, arg_strBCC:str=None, arg_listAnexos:list=None, arg_boolSucesso:bool=True):
        """
        Envio do e-mail de finalização do robô.
        Recebendo o horário do início da execução, o horário final, para quem é necessário enviar (separado por ;) e os relatórios finais
        
        Parâmetros:
        - arg_strEnvioPara (str): destinatários separados por ';'.
        - arg_strCC (str): destinatários em cópia separados por ';'. (opcional, default=None)
        - arg_strBCC (str): destinatários em cópia oculta separados por ';'. (opcional, default=None)
        - arg_listAnexos (list): lista de anexos (opcional, default=None).
        - arg_boolSucesso (bool): indica se a execução foi bem-sucedida (opcional, default=True).
        
        Retorna:

        """
        
            
        """
        Envia o e-mail de finalização utilizando a API de e-mail da empresa.
        """


        smtp = None

        # Configurando SMTP (Gmail) e fazendo login
        try:
            Maestro.write_log("Configurando SMTP do Gmail para envio")

            smtp = smtplib.SMTP(cls.var_strEmailServerSmtp, cls.var_intEmailPortaSmtp)
            smtp.starttls()  
            smtp.login(cls.var_strUsuario, cls.var_strSenha)

            Maestro.write_log("SMTP do Gmail configurado com sucesso")
        except Exception as err:
            Maestro.write_log(
                arg_strMensagemLog="Erro configurando SMTP do Gmail: " + str(err),
                arg_enumLogLevel=LogLevel.ERROR,
                arg_enumErrorType=ErrorType.APP_ERROR
            )
            raise err
        
        # Monta e envia o e-mail inicial
        try:
            # Lógica antiga: Construção do corpo e título do e-mail
            var_strHorarioInicio = InitAllSettings.var_strDatahoraInicioExec
            var_strHorarioFim = InitAllSettings.var_strDatahoraFimExec
            var_strStatusFinalizacao = "com sucesso" if arg_boolSucesso else "com erros"

            # Lendo template e preenchendo
            with open(InitAllSettings.var_strCaminhoTemplateEmailFinal, mode="r", encoding="utf-8") as var_fileTemplate:
                var_strEmailTexto = var_fileTemplate.read()
            var_strEmailTexto = (
                var_strEmailTexto.replace("*NOME_ROBO*", InitAllSettings.var_dictConfig['NomeProcesso'])
                .replace("*DATAHORA_INI*", var_strHorarioInicio)
                .replace("*DATAHORA_FIM*", var_strHorarioFim)
                .replace("*FINALIZACAO*", var_strStatusFinalizacao)
            )
            var_strEmailAssunto = "Finalização da execução: " + InitAllSettings.var_dictConfig['NomeProcesso']

            var_listEnvioPara = arg_strEnvioPara.split(";") if(arg_strEnvioPara is not None) else []
            var_listCC = arg_strCC.split(";") if(arg_strCC is not None) else []
            var_listBCC = arg_strBCC.split(";") if(arg_strBCC is not None) else []

            var_Mensagem = EmailMessage()
            var_Mensagem["From"] = cls.var_strUsuario
            var_Mensagem["To"] = ", ".join(var_listEnvioPara) if var_listEnvioPara else ""
            if var_listCC:
                var_Mensagem["Cc"] = ", ".join(var_listCC)
            var_Mensagem["Subject"] = var_strEmailAssunto

            # Corpo (HTML)
            var_Mensagem.add_alternative(var_strEmailTexto, subtype="html")

            for var_CaminhoArquivo in (arg_listAnexos or []):
                ctype, encoding = mimetypes.guess_type(var_CaminhoArquivo)
                if ctype is None or encoding is not None:
                    ctype = "application/octet-stream"
                maintype, subtype = ctype.split("/", 1)

                with open(var_CaminhoArquivo, "rb") as f:
                    var_Mensagem.add_attachment(
                        f.read(),
                        maintype=maintype,
                        subtype=subtype,
                        filename=var_CaminhoArquivo.split("\\")[-1]  # só o nome do arquivo
                    )

            var_strDestinatarios = (var_listEnvioPara or []) + (var_listCC or []) + (var_listBCC or [])

            smtp.send_message(var_Mensagem, from_addr=cls.var_strUsuario, to_addrs=var_strDestinatarios)

            Maestro.write_log("E-mail final com sucesso via Gmail")

        except Exception as err:
            Maestro.write_log(
                arg_strMensagemLog="Erro enviando e-mail inicial via Gmail: " + str(err),
                arg_enumLogLevel=LogLevel.ERROR,
                arg_enumErrorType=ErrorType.APP_ERROR
            )
            raise err
        
        finally:
            if smtp is not None:
                try:
                    smtp.quit()
                except:
                    pass
   

        