# prj_BuscaEstabelecimento

## Descrição do Projeto

Robô desenvolvido em **Python**, inspirado no **ReFramework**, para realizar buscas de estabelecimentos no **Google Maps**, gerenciar uma fila de itens a partir de um arquivo **JSON** (armazenada em **CSV**) e gerar relatórios + e-mail de resultado ao final da execução.

## Arquitetura do Projeto
- **Ferramenta de RPA Utilizada**: Python RPA

## Releases

### [v0.0.0] - 10/11/2025
- **AUTOR(A)**: Vinicius Lorencio
---

## 1. Pré-requisitos

- Python 3.10+ instalado
- `pip` configurado
- Acesso à internet (para o Google Maps)
- IDE ou terminal (VS Code, PyCharm, etc.)

---

## 2. Como configurar

1. Faça o **download** ou **clone** deste repositório.
2. Localize o arquivo de configuração:

   ```text
   resources/config/config.txt

3. Edite o config.txt e informe:
Caminho do arquivo JSON de entrada;
Caminhos de saída (planilhas, relatórios, logs, etc.);
Demais parâmetros necessários para a automação (URLs, pastas, e-mail de destino, etc.).
É obrigatório ajustar este arquivo antes de rodar o robô.

4. Instalação das dependências:
Na raiz do projeto, execute no terminal:

   ```text
   pip install -e .

   Esse comando instala todas as dependências do projeto em modo “editável”, permitindo que você altere o código sem precisar reinstalar o pacote.


5. Como executar o robô:
Ainda na raiz do projeto, execute:
python bot.py
O arquivo bot.py é o ponto de entrada da automação e inicia todo o fluxo (Init → Loop → Process → End).

6. Agendamento:
Para executar o robô de forma agendada, crie uma tarefa no Agendador de Tarefas do Windows com o horário desejado. O arquivo que deve ser executado é o run.bat, localizado dentro da pasta prj_BuscaEstabelecimento.


## 3. Visão geral da arquitetura:

Este robô foi desenvolvido em Python seguindo um padrão de ReFramework, adaptado para a estrutura do projeto.

Ao ser iniciado, o robô realiza a leitura das configurações básicas presentes nos arquivos da pasta resources/config, carregando parâmetros essenciais para a execução (caminhos de arquivos, URLs, credenciais, etc.). Em seguida, são instanciados os componentes necessários para a automação, como classes de utilidades, gerenciamento de fila e controle de exceções.

Fase de Inicialização (Init)
O fluxo de inicialização é centralizado na classe InitAllApplications.py, localizada em classes/framework.
Nessa etapa, o robô:
Realiza a leitura do arquivo JSON de entrada, contendo os tipos de estabelecimentos, cidades e quantidades desejadas;
Converte essas informações em uma espécie de banco de dados em CSV, onde cada linha representa um item de processamento e possui um status de controle (por exemplo, NEW, PROCESSING, SUCCESS, SYSTEM_EXCEPTION, etc.);
Efetua a abertura inicial do site do Google Maps, por meio da classe PortalGoogle.py, no método abertura_portal, localizada em utils/PortalGoogle.py.
Essa abordagem permite que todo o gerenciamento da fila de itens seja feito sobre o CSV, facilitando controle, reprocessamento e auditoria da automação.

Fase de Processamento (LoopStation + Process)
Após a inicialização, o robô entra no fluxo de repetição controlado pela classe LoopStation.py (classes/framework/LoopStation.py).
O LoopStation é responsável por:
Consultar o “banco CSV” em busca de itens com status NEW;
Selecionar o próximo item elegível e alterá-lo para o estado de processamento;
Encaminhar esse item para o fluxo de Processamento, implementado em classes/framework/Process.py.

Dentro do Process, são realizadas:

A consulta detalhada no Google Maps, com base nos parâmetros do item (tipo de estabelecimento, cidade, quantidade de resultados, etc.);

A captura dos dados relevantes (nome, avaliação, número de reviews, endereço, telefone, link, etc.);

O registro dos resultados na planilha final de saída da automação.

Caso ocorra qualquer interferência ou erro durante o processamento (ex.: falha de conexão, mudança de layout, elemento não encontrado), o fluxo aciona a camada de tratamento de exceções. O item é então reprocessado de acordo com a política de tentativas definida (até 3 tentativas). Se, após o número máximo de tentativas, o erro persistir, o item é marcado com status de exceção sistêmica e o robô segue para o próximo registro. Em caso de sucesso, o status do item é atualizado para refletir a conclusão correta do processamento.

Fase de Finalização (EndProcess)
Após o processamento de todos os itens da fila, o robô entra na etapa de finalização, coordenada pela classe EndProcess.py (classes/framework/EndProcess.py).
Nessa fase são executadas as seguintes ações:
Geração e preenchimento do relatório sintético e analítico da automação, por meio das rotinas de relatório em classes/relatorios/Relatorios.py;
Preparação das informações consolidadas de execução (quantidade de itens processados, sucessos, falhas, exceções, etc.);
Chamada da classe de envio de e-mail (classes/email/SendEmail.py) para encaminhar o e-mail final com os resultados da automação e anexos necessários;
Fechamento ordenado dos portais e aplicações utilizados durante o processo, garantindo que nenhum recurso fique aberto desnecessariamente.
Essa arquitetura em camadas (Init → Loop/Process → End) permite que o robô seja facilmente mantido, ampliado e reutilizado, mantendo a organização e a previsibilidade típicas de um ReFramework, porém totalmente implementado em Python.







