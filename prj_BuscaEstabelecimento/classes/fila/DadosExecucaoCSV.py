import pandas as pd
import openpyxl  # Para manipulação do Excel
from prj_BuscaEstabelecimento.classes.utils.Maestro import Maestro as Maestro, LogLevel, ErrorType
from prj_BuscaEstabelecimento.classes.framework.InitAllSettings import InitAllSettings as InitAllSettings
from datetime import datetime

class BancoAtualizador:
    
    var_dictConfig:dict = InitAllSettings.var_dictConfig
    var_strArquivoLog = InitAllSettings.var_strPathRelatorioLog
    
    
    def __init__(self, caminho_arquivo):
        self.caminho_arquivo = caminho_arquivo
        self.planilha = self.carregar_planilha()


    def carregar_planilha(self):
        return pd.read_csv(self.caminho_arquivo)


    def salvar_planilha(self):
        """Salva as atualizações no arquivo CSV."""
        self.planilha.to_csv(self.caminho_arquivo, index=False)


    def obter_ultimo_id(self):
        """Retorna o último ID existente na planilha."""
        if self.planilha.empty:
            return 0  # Começa com ID 1 se não houver entradas
        else:
            return self.planilha['ID'].max()

    def insert(self, dados_df):
        """Insere novas linhas com IDs incrementais a partir da 'filtered_df'."""
        novas_linhas = []
        ultimo_id = self.obter_ultimo_id()
        
        for _, linha in dados_df.iterrows():
            ultimo_id += 1  # Incrementa o ID para cada nova linha
            nova_linha = {
                'ID': ultimo_id,
                'Tipo': linha['tipo_estabelecimento'],
                'Cidade': linha['cidade'],
                'Quantidade': linha['quantidade'],
                'Data criacao': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                'Status': 'NEW',
            }
            novas_linhas.append(nova_linha)
        
        self.planilha = pd.concat([self.planilha, pd.DataFrame(novas_linhas)], ignore_index=True)
        self.salvar_planilha()
        Maestro.write_log("Dados da fila inseridos com sucesso.")


    def update(self, id_referencia, novos_dados):
        """
        Atualiza a linha com o ID especificado.
        'novos_dados' deve ser um dicionário com todas as colunas a serem atualizadas.
        """
        # Verifica se o ID existe
        if id_referencia in self.planilha['ID'].values:
            # Atualiza apenas as colunas especificadas
            
            self.planilha.loc[self.planilha['ID'] == id_referencia, novos_dados.keys()] = [", ".join(map(str, v)) if isinstance(v, list) else v for v in novos_dados.values()]

            self.salvar_planilha()
            Maestro.write_log(f"Linha com ID {id_referencia} atualizada com sucesso.")
        else:
            Maestro.write_log(f"ID {id_referencia} não encontrado.")
            
    def contar_itens_status_new(self):
        
        """Conta o número de itens na planilha com Status 'New'."""
        if 'Status' in self.planilha.columns:
            var_intQuantidadeFila = self.planilha[self.planilha['Status'] == 'NEW'].shape[0]
            Maestro.write_log(f"A quantidade de itens da fila para ser processados: {var_intQuantidadeFila}")
            return var_intQuantidadeFila
        else:
            Maestro.write_log("A coluna 'Status' não existe na planilha.")
            return 0
        

    def obter_proximo_item_status_new(self):
        # Retorna a primeira linha com Status 'New' como um dicionário, ou None se não houver mais itens.
        if 'Status' in self.planilha.columns:
            # Filtra as linhas com status 'New'
            item_new = self.planilha[self.planilha['Status'] == 'NEW']
            if not item_new.empty:
                # Seleciona a primeira linha e converte para dicionário
                primeira_linha = item_new.iloc[0].to_dict()
                return primeira_linha
            else:
                Maestro.write_log("Não há mais itens com status 'New'.")
                return None
        else:
            Maestro.write_log("A coluna 'Status' não existe na planilha.")
            return None
        
    def atualiza_item_em_processamento(self,var_strIdProcessamento):
        """Retorna a primeira linha com Status 'New' como um dicionário, ou None se não houver mais itens."""
        if 'ID' in self.planilha.columns:
            # Filtra as linhas com status 'New'
            item_new = self.planilha[self.planilha['ID'] == var_strIdProcessamento]
            if not item_new.empty:
                # Seleciona a primeira linha e converte para dicionário
                primeira_linha = item_new.iloc[0].to_dict()
                return primeira_linha
            else:
                Maestro.write_log("Não há mais itens com status 'New'.")
                return None
        else:
            Maestro.write_log("A coluna 'Status' não existe na planilha.")
            return None
        
        
    def update_fim(self, id_item, data_inicio, data_fim,caminho_pasta ,novo_status, observacao):
        """
        Atualiza as colunas de início e fim do processamento, status e observação na linha correspondente ao ID.

        Parâmetros:
        - id_item: ID do item que será atualizado.
        - data_inicio: Data de início do processamento.
        - data_fim: Data de finalização do processamento.
        - novo_status: Novo status do item.
        - observacao: Observação a ser adicionada.
        """
        
        # Localiza a linha com o ID fornecido
        index_item = self.planilha[self.planilha['ID'] == id_item].index

        if not index_item.empty:
            # Garante que as colunas têm dtype compatível (texto)
            cols_texto = ['Data iniciado', 'Data finalizado', 'Caminho da Pasta', 'Status', 'Obs']
            for col in cols_texto:
                self.planilha[col] = self.planilha[col].astype('object')

            idx = index_item[0]

            # Atualiza os valores das colunas
            self.planilha.at[idx, 'Data iniciado'] = data_inicio
            self.planilha.at[idx, 'Data finalizado'] = data_fim
            self.planilha.at[idx, 'Caminho da Pasta'] = caminho_pasta
            self.planilha.at[idx, 'Status'] = novo_status
            self.planilha.at[idx, 'Obs'] = observacao

            # Salva a planilha atualizada
            self.salvar_planilha()
            Maestro.write_log(f"Item com ID {id_item} atualizado com sucesso.")
            return True  # Indica sucesso na atualização
        else:
            Maestro.write_log(f"Item com ID {id_item} não encontrado na planilha.")
            return False  # Indica falha na atualização



