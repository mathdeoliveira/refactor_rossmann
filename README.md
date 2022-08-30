# Predição de vendas de cada loja Rossmann

A Rossmann opera mais de 3.000 drogarias em 7 países europeus. Atualmente, os gerentes de loja da Rossmann têm a tarefa de prever suas vendas diárias com até seis semanas de antecedência. As vendas da loja são influenciadas por muitos fatores, incluindo promoções, competição, feriados escolares e estaduais, sazonalidade e localidade. Com milhares de gerentes individuais prevendo vendas com base em suas circunstâncias únicas, a precisão dos resultados pode ser bastante variada.

## Planejamento

Dado a introdução temos aqui um problema para tratar: prever com seis semanas de antecedência as vendas diárias de cada loja para minimizar a falta de precisão dos resultados pois diversos gerentes realizam essa tarefa e cada um tem resultados discrepantes a serem compartilhados com a matriz.

Atualmente a matriz recebe de forma os resultados das previsões de forma manual enviado pelo meio digital de cada uma loja espalhadas pelos países europeus, temos aqui então a segunda dor do cliente, devemos planejar a unificação desses resultados em um lugar, facilitando o acesso e resultados para cada loja.


## Solução

O desejo do cliente é que seja feito o desenvolvimento de uma solução para prever vendas usando dados de loja, promoção e concorrentes.

Para tal será utilizado algoritmos de machine learning para que seja possível o aprendizado desses dados de entrada e que para cada dia as pessoas designadas farão a utilização de uma tecnologia para visualizar e interagir com as previsões e assim tomar as decisões.

### Arquitetura

<p align="center" width="100%">
    <img width="60%" src="https://i.imgur.com/ScBroqG.png">
</p>

## Estrutura do projeto

- **refactor_rossmann:** código fonte do projeto
- **config:** arquivos de configurações
- **models:** arquivos serializados dos modelos utilizados no projeto
- **docs:** documentação
- **tests:** arquivos de testes dos códigos do projeto

## Como rodar esse projeto

Para executar esse projeto e visualizar ele em execução, devemos:
- Etapa de ambiente
1. Possuir o Python instalado na versão 3.9.12 **``` conda create -n venv python=3.9.12 ```**
2. Clonar o repositório do [(GitHub)](https://github.com/mathdeoliveira/refactor_rossmann)
3. Realizar o download dos arquivos do Google Drive [(clique aqui)](https://drive.google.com/drive/folders/1X0V7RcjYuSkyv4UJnGPdzBjcx2XRzwXU?usp=sharing) e insira na pasta **```data/raw```**, ficando de acordo com a foto abaixo:
<p align="center" width="100%">
    <img width="30%" src="https://i.imgur.com/9F9526l.png">
</p>

1. Entrar no diretório raiz **```/refactor_rossmann```**
2. Instalar o arquivo requirements.txt **```pip install -r requirements.txt```**
   
- Treinamento do modelo
1. Em um novo terminal com o ambiente virtual ativado executar: **```make mlflow```** para iniciar o MLFlow
2. Para iniciar o treinamento, em um novo terminal executar: **```make train```**
3. Para acompanhar e monitorar o treinamento, abrir em um navegador o MLFlow UI no endereço: **```http://127.0.0.1:5000/```**

- Predição do modelo
1. Em um novo terminal com o ambiente virtual ativado executar: **```make firefly```** para iniciar o servidor de predição
2. Para executar uma predição em um novo terminal executar o comando: **```make predict STORE=ID_STORE```**, onde ID_STORE deve ser passado como valor obrigatório inteiro
